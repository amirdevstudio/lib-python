from dataclasses import dataclass

from amir_dev_studio.computer_vision.models.base import Base
from amir_dev_studio.computer_vision.models.rectangle import Rectangle


@dataclass
class DrawableBoundingBox(Base):
    class_name: str
    class_id: int
    confidence: float
    rect: Rectangle

    def __copy__(self):
        return DrawableBoundingBox(
            self.class_name,
            self.class_id,
            self.confidence,
            self.rect
        )

