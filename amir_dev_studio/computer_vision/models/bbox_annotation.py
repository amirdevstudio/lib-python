from dataclasses import dataclass

from amir_dev_studio.computer_vision.models.rectangle import Rectangle


@dataclass
class BoundingBoxAnnotation:
    class_name: str
    class_id: int
    confidence: float
    rect: Rectangle
