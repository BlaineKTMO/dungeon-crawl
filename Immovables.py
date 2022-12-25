import ImagePlugin


class Immovable(ImagePlugin.Image):
    def __init__(self, image, pos, group):
        super().__init__(group)
        self.image, self.rect = self.load_image(image)
        self.rect.x, self.rect.y = pos

    def update(self):
        pass
