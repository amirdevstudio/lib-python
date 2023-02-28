from dataclasses import dataclass, field


@dataclass
class BaseModel:
    extra_data: dict = field(init=False, default_factory=dict, repr=False)
