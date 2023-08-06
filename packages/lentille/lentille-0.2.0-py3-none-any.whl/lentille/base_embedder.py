from abc import ABC
import onnxruntime


class BaseEmbedder(ABC):
    """
    Base Embedder class. For now this class is instantiated using an onnx session, this might be abstracted higher or lower later on.
    """

    def __init__(self, session):
        self.session = session

    @classmethod
    def from_file(cls, file):
        return cls(onnxruntime.InferenceSession(file))
