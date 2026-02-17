
from PySide6.QtWidgets import QFrame


class LineFrame(QFrame):
    Shape = QFrame.Shape
    Shadow = QFrame.Shadow

    def __init__(self, shape: QFrame.Shape, shadow: QFrame.Shadow):
        super().__init__()
        self.setFrameShape(shape)
        self.setFrameShadow(shadow)


class HLineFrame(LineFrame):
    def __init__(self, shadow: QFrame.Shadow = LineFrame.Shadow.Sunken):
        super().__init__(shape=self.Shape.HLine, shadow=shadow)


class VLineFrame(LineFrame):
    def __init__(self, shadow: QFrame.Shadow = LineFrame.Shadow.Sunken):
        super().__init__(shape=self.Shape.VLine, shadow=shadow)


__all__ = [
    "HLineFrame",
    "VLineFrame",
]
