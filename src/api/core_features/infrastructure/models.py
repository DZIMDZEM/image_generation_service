import os

from injector import Module, singleton, provider

from src.api.domain_features.dcgan.dcgan import Generator
from src.api.domain_features.dcgan.load import load_dcgan_model


# from ultralytics import YOLO


class ModelModule(Module):
    # yolov8_model = None
    #
    # @singleton
    # @provider
    # def provide_yolov8_model(self) -> YOLO:
    #     if self.yolov8_model is None:
    #         path = os.path.join(os.path.dirname(__file__), "../../../model_weights/yolov8n.pt")
    #         self.yolov8_model = YOLO(path)
    #     return self.yolov8_model

    dcgan_model = None

    @singleton
    @provider
    def provide_dcgan_model(self) -> Generator:
        if self.dcgan_model is None:
            path = r"src/model_weights/dcgan_cat_299_cpu.pth"
            self.dcgan_model = load_dcgan_model(path)

        return self.dcgan_model
