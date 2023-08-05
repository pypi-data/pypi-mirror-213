import os
from openvino.runtime import Core
from openvino.runtime import serialize


class Onnx2Vino:
    def __init__(self,
                 onnx_file="models/model.onnx",
                 output_dir="models",
                 image_width=224,
                 image_height=224):
        self.onnx_file = onnx_file
        self.output_dir = output_dir
        self.image_width = image_width
        self.image_height = image_height
        self.xml_path = os.path.join(self.output_dir, os.path.basename(onnx_file).replace('.onnx', '.xml'))
        self.bin_path = os.path.join(self.output_dir, os.path.basename(onnx_file).replace('.onnx', '.bin'))
        ie = Core()
        self.model_onnx = ie.read_model(model=self.onnx_file)
        self.compiled_model_onnx = ie.compile_model(model=self.model_onnx, device_name="CPU")

    def convert(self):
        serialize(model=self.model_onnx, xml_path=self.xml_path, bin_path=self.bin_path)
        print("Exported ONNX model to IR succeed!")
