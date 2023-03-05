from amir_dev_studio.computer_vision.models.base import Base
from amir_dev_studio.computer_vision.models.image import Image


class ImageGrid(Base):
    def __init__(self, images: list[Image]):
        self.images = images

    def __copy__(self):
        return ImageGrid([image.copy() for image in self.images])

    def concat_to_image(self, grid_shape: tuple[int, int] = None) -> Image:
        columns, rows = grid_shape

        if not self.images:
            raise Exception('No images to render')

        if len(self.images) > columns * rows:
            raise Exception(f'Too many images. Images: {len(self.images)}, Grid: {grid_shape[0]}x{grid_shape[1]}')

        image_grid = []
        images = self.images.copy()
        blank_image_width = images[0].width
        blank_image_height = images[0].height

        for i in range(rows):
            image_grid.append([])
            for j in range(columns):
                image_grid[i].append(
                    self.images.pop(0) if self.images else Image.create_blank(
                        blank_image_width,
                        blank_image_height
                    )
                )

        concat_grid = None
        for images in image_grid:
            concat_row = None
            for image in images:
                concat_row = (
                    image
                    if concat_row is None
                    else concat_row.concat_horizontal(image)
                )

            concat_grid = (
                concat_row if
                concat_grid is None
                else concat_grid.concat_vertical(concat_row)
            )

        return concat_grid
