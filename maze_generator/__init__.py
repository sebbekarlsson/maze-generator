import random

import numpy
from PIL import Image


class StructType:
    INTERSECTION = 0
    HORIZONTAL = 1
    VERTICAL = 2
    EMPTY = 3


class Canvas(object):
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.data = numpy.zeros((self.height, self.width, 3),
                                dtype=numpy.uint8)
        self.image = Image.fromarray(self.data)
        self.block_size = 16
        self.struct_type = None
        self.locations = {}
        self.path = self.generate_path()
        self.iterate(self.generate)

    def set_location_data(self, x, y, struct_type):
        if x not in self.locations:
            self.locations[x] = {}

        if y not in self.locations[x]:
            self.locations[x][y] = None

        self.locations[x][y] = struct_type

    def get_location_data(self, x, y):
        if x not in self.locations:
            return None

        if y not in self.locations[x]:
            return None

        return self.locations[x][y]

    def draw_pixel(self, x, y, r, g, b):
        px = max(0, (min(self.width - 1, x)))
        py = max(0, (min(self.height - 1, y)))
        self.image.putpixel((px, py), (r, g, b, 255))

    def iterate(self, callback):
        x = 0
        y = 0

        for row in self.data:
            for pixel in row:
                callback(x, y, pixel)
                x += 1

            y += 1
            x = 0

    def render(self):
        self.iterate(self.fragment_shader)

    def render_wall_h(self, x, y, r, g, b):
        # top
        for i in range(self.block_size):
            self.draw_pixel(x + i, y, r, g, b)

        # bottom
        for i in range(self.block_size):
            self.draw_pixel(x + i, y + self.block_size, r, g, b)

    def render_wall_v(self, x, y, r, g, b):
        # left
        for i in range(self.block_size):
            self.draw_pixel(x, y + i, r, g, b)

        # right
        for i in range(self.block_size):
            self.draw_pixel(x + self.block_size, y + i, r, g, b)

    def render_intersection(self, x, y, r, g, b):
        margin = 6

        # left
        for i in range(self.block_size):
            if i < (self.block_size / 2) - margin or i > (
                    self.block_size / 2) + margin:
                self.draw_pixel(x, y + i, r, g, b)
        # right
        for i in range(self.block_size):
            if i < (self.block_size / 2) - margin or i > (
                    self.block_size / 2) + margin:
                self.draw_pixel(x + self.block_size, y + i, r, g, b)

        # top
        for i in range(self.block_size):
            if i < (self.block_size / 2) - margin or i > (
                    self.block_size / 2) + margin:
                self.draw_pixel(x + i, y, r, g, b)

        # bottom
        for i in range(self.block_size):
            if i < (self.block_size / 2) - margin or i > (
                    self.block_size / 2) + margin:
                self.draw_pixel(x + i, y + self.block_size, r, g, b)

    def render_struct(self, struct_type, x, y, r=255, g=255, b=255):
        if struct_type == StructType.INTERSECTION:
            return
        if struct_type == StructType.HORIZONTAL:
            return self.render_wall_h(x, y, r=r, g=g, b=b)
        if struct_type == StructType.VERTICAL:
            return self.render_wall_v(x, y, r=r, g=g, b=b)
        elif struct_type == StructType.EMPTY:
            return self.draw_pixel(
                int(x + self.block_size / 2), int(y + self.block_size / 2), r,
                g, b)

    def get_new_struct_type(self):
        return random.randint(0, 2)

    def generate_path(self):
        path = []

        left = random.randint(0, 1)

        if left:
            startx = 0
            starty = random.randint(0, self.height / self.block_size)
        else:
            starty = 0
            startx = random.randint(0, self.width / self.block_size)

        x = startx
        y = starty

        while True:
            path.append((x, y))

            if x >= (self.width / self.block_size):
                break

            if random.randint(0, 3) == 0:
                x += 1
                continue

            if y < (self.height / self.block_size):
                if random.randint(0, 3) == 0:
                    y += 1

        return path

    def fragment_shader(self, x, y, pixel):
        if x % self.block_size == 0 and y % self.block_size == 0:
            data = self.get_location_data(x, y)

            if data:
                self.render_struct(data, x, y)

    def generate(self, x, y, pixel):
        if x % self.block_size == 0 and y % self.block_size == 0:
            if self.struct_type is None:
                self.struct_type = self.get_new_struct_type()

            x_n = int(x / self.block_size)
            y_n = int(y / self.block_size)

            for p in self.path:
                if p[0] == x_n and p[1] == y_n:
                    self.render_struct(StructType.EMPTY, x, y, r=255, g=0, b=0)
                    return

            # intersection to the left or right
            if self.get_location_data(x - self.block_size, y) == StructType.INTERSECTION\
                or self.get_location_data(x + self.block_size, y) == StructType.INTERSECTION:
                self.struct_type = StructType.HORIZONTAL
            # intersection above or below
            elif self.get_location_data(x, y - self.block_size) == StructType.INTERSECTION\
                or self.get_location_data(x, y + self.block_size) == StructType.INTERSECTION:
                self.struct_type = StructType.VERTICAL
            else:
                self.struct_type = self.get_new_struct_type()

            self.set_location_data(x, y, self.struct_type)

    def show(self):
        return self.image.show()
