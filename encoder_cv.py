#!/usr/bin/env python

import argparse
from pathlib import Path
import cv2
import numpy as np
import qrcode
import uuid

from util import filename_add_suffix


class Encoder:
    def __init__(self, image):
        self.image = image
        self.rows, self.cols, _ = self.image.shape
        self.debug = False

    def __gen_qr(self, message):
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(message)
        qr.make(fit=True)
        # img = qr.make_image(back_color="transparent", fill_color=(0, 0, 0, self.gamma))
        qr_img = qr.make_image()
        # print(list(qr_img.getdata()))
        cv_img = np.array(qr_img.getdata(), dtype=np.float32)
        cv_img = 255 - cv_img
        cv_img = np.reshape(cv_img, qr_img.size)

        cr = min(self.cols, self.rows)
        cv_img = cv2.resize(cv_img, (cr, cr))
        blank_img = np.zeros((self.rows, self.cols), dtype=np.uint8)

        # Place the resized image in the center of the canvas
        r_offset = (self.rows - cv_img.shape[0]) // 2
        c_offset = (self.cols - cv_img.shape[1]) // 2
        blank_img[r_offset : r_offset + cv_img.shape[0], c_offset : c_offset + cv_img.shape[1]] = cv_img
        return blank_img

    def __add_qr(self, qr, gamma):
        # print(self.image.shape)
        deltas = np.random.randint(gamma, gamma + 5, size=qr.shape)
        deltas = cv2.bitwise_and(deltas, deltas, mask=qr)
        # cv2.imwrite("test2.png", deltas)
        min_is = np.argmin(self.image, axis=2)

        for c in range(self.cols):
            for r in range(self.rows):
                min_i = min_is[r, c]
                if deltas[r, c] > 0:
                    if self.image[r, c, min_i] >= deltas[r, c]:
                        self.image[r, c, min_i] -= deltas[r, c]
                    else:
                        self.image[r, c, min_i] += deltas[r, c]

    def save(self, filename):
        filename = Path(filename)
        out_filename = filename_add_suffix(filename, suffix="out")
        cv2.imwrite(out_filename, self.image)

    def encode(self, message=str(uuid.uuid4()), gamma=1):
        print(f"encode message {message}")
        qr = self.__gen_qr(message)
        self.__add_qr(qr, gamma)
        # img.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    image = cv2.imread(args.filename)
    e = Encoder(image)
    e.encode()
    e.save(args.filename)
