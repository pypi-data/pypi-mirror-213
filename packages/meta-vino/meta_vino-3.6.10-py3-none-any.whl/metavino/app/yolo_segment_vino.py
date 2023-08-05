import cv2
import numpy as np
from openvino.runtime import Core
from ..utils import preproc, postprocess, sigmoid, fast_dot


class YoloSegmentVino:
    def __init__(self, xml_file="models/model.xml"):
        self.xml_file = xml_file
        ie = Core()
        self.model = ie.read_model(model=self.xml_file)
        self.compiled_model = ie.compile_model(model=self.model, device_name="CPU")
        self.input_layer = self.compiled_model.input(0)
        self.mask_layer = self.compiled_model.output(4)
        self.output_layer = self.compiled_model.output(0)
        self.mean = None
        self.std = None

    @staticmethod
    def get_rect(mask):
        h, w = mask.shape[:2]
        _, pred = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(pred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) < 1:
            return [[0, 0], [0, w - 1], [h - 1, w - 1], [h - 1, 0]]

        area = [cv2.contourArea(c) for c in contours]
        max_idx = np.argmax(area)
        min_rect = cv2.minAreaRect(contours[max_idx])
        min_rect = cv2.boxPoints(min_rect)

        return min_rect

    def predict(self, image, conf=0.25, iou=0.6, use_mask=False, use_cupy=False):
        dets = []
        size_h, size_w = self.input_layer.shape[2], self.input_layer.shape[3]
        img, ratio = preproc(image, (size_h, size_w), self.mean, self.std)
        outputs = self.compiled_model([img[np.newaxis, :]])

        pred = outputs[self.output_layer][0]
        boxes = postprocess(pred, ratio=1., score_thr=conf, nms_thr=iou)
        if boxes is None: return dets

        if use_mask:
            proto = outputs[self.mask_layer]

            if use_cupy:
                import cupy as cp

                gpu_data0 = cp.asarray(proto)
                gpu_proto = cp.reshape(gpu_data0, (1, 32, -1))[0]
                gpu_boxes = cp.asarray(boxes[:, 6:])
                gpu_dot = cp.dot(gpu_boxes, gpu_proto)
                gpu_sigmoid_dot = 1 / (1 + cp.exp(-gpu_dot))
                gpu_masks = cp.reshape(gpu_sigmoid_dot, (-1, 160, 160))
                masks = cp.asnumpy(gpu_masks)
                ih, iw = 160 / size_h, 160 / size_w
            else:
                proto = np.reshape(proto, (1, 32, -1))[0]
                masks = np.reshape(sigmoid(fast_dot(boxes[:, 6:], proto)), (-1, 160, 160))
                ih, iw = 160 / size_h, 160 / size_w

            for mask, box, score, label in zip(masks, boxes[:, :4], boxes[:, 4], boxes[:, 5]):
                x1, y1, x2, y2 = box[0] * iw, box[1] * ih, box[2] * iw, box[3] * ih
                crop = mask[int(y1):int(y2) + 1, int(x1):int(x2) + 1] * 255
                min_rect = self.get_rect(crop.astype(np.uint8))
                rect = [[(r[0] + x1) / ih / ratio, (r[1] + y1) / iw / ratio] for r in min_rect]
                dets.append([max(int(rect[0][0]), 0), max(int(rect[0][1]), 0),
                             max(int(rect[1][0]), 0), max(int(rect[1][1]), 0),
                             max(int(rect[2][0]), 0), max(int(rect[2][1]), 0),
                             max(int(rect[3][0]), 0), max(int(rect[3][1]), 0),
                             float(score), int(label)])
        else:
            for box, score, label in zip(boxes[:, :4], boxes[:, 4], boxes[:, 5]):
                x1, y1, x2, y2 = box[0] / ratio, box[1] / ratio, box[2] / ratio, box[3] / ratio
                dets.append([max(int(x1), 0), max(int(y1), 0),
                             max(int(x2), 0), max(int(y1), 0),
                             max(int(x2), 0), max(int(y2), 0),
                             max(int(x1), 0), max(int(y2), 0),
                             float(score), int(label)])

        return dets

    @staticmethod
    def show(image, results):
        if results is None or len(results) == 0:
            return image
        for i, result in enumerate(results):
            x1, y1, x2, y2, x3, y3, x4, y4, score, label = result
            cv2.line(image, pt1=(x1, y1), pt2=(x2, y2), color=(255, 255, 0), thickness=10)
            cv2.line(image, pt1=(x2, y2), pt2=(x3, y3), color=(255, 255, 0), thickness=10)
            cv2.line(image, pt1=(x3, y3), pt2=(x4, y4), color=(255, 255, 0), thickness=10)
            cv2.line(image, pt1=(x4, y4), pt2=(x1, y1), color=(255, 255, 0), thickness=10)
            cv2.putText(image, '%d-%.2f' % (label, score),
                        (x1, y1 - 4), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), thickness=2)
        return image
