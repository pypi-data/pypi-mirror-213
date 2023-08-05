import cv2
import numpy as np
from openvino.runtime import Core
from ..utils import sigmoid


def preprocess(image, input_size, mean, std, swap=(2, 0, 1)):
    resized_img = cv2.resize(image, (input_size[1], input_size[0]), interpolation=cv2.INTER_LINEAR)
    resized_img = resized_img[:, :, ::-1].astype(np.float32)
    resized_img /= 255.0
    if mean is not None:
        resized_img -= np.array(mean)
    if std is not None:
        resized_img /= np.array(std)
    resized_img = resized_img.transpose(swap)
    resized_img = np.ascontiguousarray(resized_img, dtype=np.float32)
    return resized_img


class SaliencySegmentVino:
    def __init__(self, xml_file="models/model.xml"):
        self.xml_file = xml_file
        ie = Core()
        self.model = ie.read_model(model=self.xml_file)
        self.compiled_model = ie.compile_model(model=self.model, device_name="CPU")
        self.input_layer = self.compiled_model.input(0)
        self.output_layer = self.compiled_model.output(0)
        self.mean = [0.485, 0.456, 0.406]
        self.std = [0.229, 0.224, 0.225]

    def predict(self, image, class_names):
        h, w = image.shape[:2]
        _, _, size_h, size_w = self.input_layer.shape
        img = preprocess(image, (size_h, size_w), self.mean, self.std)
        pred = self.compiled_model([np.expand_dims(img, 0)])[self.output_layer]
        # request = self.compiled_model.create_infer_request()
        # request.infer(inputs={self.input_layer.any_name: input_data})
        # pred = request.get_output_tensor(self.output_layer.index).data

        pred = sigmoid(pred[0, 0])
        pred = np.asarray(pred * 255).astype(np.uint8)
        pred = cv2.resize(pred, (w, h), interpolation=cv2.INTER_LINEAR)
        return pred

    @staticmethod
    def show(image, mask):
        result = image * (mask[:, :, np.newaxis] / 255)
        return result.astype(np.uint8)
