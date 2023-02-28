from dataclasses import dataclass, field


@dataclass
class Model:
    extra_data: dict = field(init=False, default_factory=dict, repr=False)


@dataclass
class RenderableShape(Model):
    render_args: dict = field(init=False, default_factory=dict, repr=False)
