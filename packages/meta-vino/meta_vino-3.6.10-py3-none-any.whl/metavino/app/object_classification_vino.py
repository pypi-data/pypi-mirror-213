import cv2
import numpy as np
from ..utils import softmax
from openvino.runtime import Core


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


class ObjectClassificationVino:
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
        n_classes = len(class_names)
        _, _, size_h, size_w = self.input_layer.shape
        img = preprocess(image, (size_h, size_w), self.mean, self.std)
        data = self.compiled_model([np.expand_dims(img, 0)])[self.output_layer]
        predictions = np.reshape(data, (1, -1, n_classes))[0][0]
        out = softmax(predictions) * 100
        output_class = np.argmax(out)

        return {'category_id': int(output_class),
                'category': class_names[int(output_class)],
                'score': float(out[int(output_class)])}
