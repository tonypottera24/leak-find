#!/usr/bin/env python

import argparse
from pathlib import Path
from PIL import Image, ImageFilter, ImageOps
import qrcode
import uuid

from util import filename_add_suffix


class Encoder:
    def __init__(self, image):
        self.image = image
        self.w, self.h = self.image.size
        self.debug = False

    def __gen_qr(self, message):
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(message)
        qr.make(fit=True)
        # img = qr.make_image(back_color="transparent", fill_color=(0, 0, 0, self.gamma))
        img = qr.make_image()
        wh = min(self.w, self.h)
        new_img = Image.new("L", (self.w, self.h))
        img = img.resize((wh, wh))
        new_img.paste(img, ((self.w - wh) // 2, (self.h - wh) // 2))
        return new_img

    def __add_qr(self, qr):
        for x in range(self.w):
            for y in range(self.h):
                if qr.getpixel((x, y)) == 0:
                    p = list(self.image.getpixel((x, y)))
                    min_i = 0
                    mm = 255
                    for i in range(len(p)):
                        if p[i] < mm:
                            mm = p[i]
                            min_i = i

                    if p[min_i] >= self.gamma:
                        p[min_i] -= self.gamma
                    else:
                        p[min_i] += self.gamma
                    self.image.putpixel((x, y), tuple(p))

    def save(self, filename):
        filename = Path(filename)
        img = self.image.convert("RGB")
        img.save(filename_add_suffix(filename, suffix="out"))

    def encode(self, message=str(uuid.uuid4()), gamma=5):
        print(f"encode message {message}")
        self.gamma = gamma
        qr = self.__gen_qr(message)
        self.__add_qr(qr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    image = Image.open(args.filename).convert("RGB")
    e = Encoder(image)
    e.encode()
    e.save(args.filename)
