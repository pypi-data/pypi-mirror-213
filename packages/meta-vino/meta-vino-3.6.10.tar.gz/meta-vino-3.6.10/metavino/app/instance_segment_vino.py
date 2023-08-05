import cv2
import numpy as np
from openvino.runtime import Core
from ..utils import sigmoid


def preprocess(image, input_size, mean, std, swap=(2, 0, 1)):
    resized_img = cv2.resize(image, (input_size[1], input_size[0]), interpolation=cv2.INTER_LINEAR)
    resized_img = resized_img[:, :, ::-1].astype(np.float32)
    # resized_img /= 255.0
    # if mean is not None:
    #     resized_img -= np.array(mean)
    # if std is not None:
    #     resized_img /= np.array(std)
    resized_img = resized_img.transpose(swap)
    resized_img = np.ascontiguousarray(resized_img, dtype=np.float32)
    return resized_img


class InstanceSegmentVino:
    def __init__(self, xml_file="models/model.xml"):
        self.xml_file = xml_file
        ie = Core()
        self.model = ie.read_model(model=self.xml_file)
        self.compiled_model = ie.compile_model(model=self.model, device_name="CPU")
        self.input_layer = self.compiled_model.input(0)
        self.output_box_layer = self.compiled_model.output(0)
        self.output_class_layer = self.compiled_model.output(1)
        self.output_mask_layer = self.compiled_model.output(2)
        self.output_score_layer = self.compiled_model.output(3)
        self.mean = None
        self.std = None

    def predict(self, image, class_names):
        h, w = image.shape[:2]
        _, size_h, size_w = self.input_layer.shape
        scale_h, scale_w = size_h / h, size_w / w
        img = preprocess(image, (size_h, size_w), self.mean, self.std)
        outputs = self.compiled_model([img])
        boxes = outputs[self.output_box_layer]
        labels = outputs[self.output_class_layer]
        masks = outputs[self.output_mask_layer]
        scores = outputs[self.output_score_layer]
        dets = []

        for box, score, label, mask in zip(boxes, scores, labels, masks):
            xmin, ymin, xmax, ymax = box
            xmin, ymin, xmax, ymax = int(xmin / scale_w), int(ymin / scale_h), int(xmax / scale_w), int(ymax / scale_h)
            dets.append([xmin, ymin, xmax, ymax, round(float(score), 2), int(label)])

        return dets

    @staticmethod
    def show(image, results):
        if results is None or len(results) == 0:
            return image
        for xmin, ymin, xmax, ymax, score, label in results:
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 0, 255), 2)
            cv2.putText(image, 'label: %d, score: %.2f' % (label, score),
                        (xmin, ymin - 4), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), thickness=2)
        return image
