#!/usr/bin/env python

import argparse
from pathlib import Path
from random import randrange
from PIL import Image, ImageFilter, ImageOps
import cv2
import numpy as np
import qrcode
import uuid

from util import filename_add_suffix


class Encoder:
    def __init__(self, filename):
        self.image = cv2.imread(filename)
        self.rows, self.cols, _ = self.image.shape
        self.filename = Path(filename)
        self.debug = False
        self.gamma = 100

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

        # self.__save(img)
        return blank_img

    def __add_qr(self, qr):
        # print(self.image.shape)
        deltas = np.random.randint(self.gamma, self.gamma + 5, size=qr.shape)
        deltas = cv2.bitwise_and(deltas, deltas, mask=qr)
        # cv2.imwrite("test2.png", deltas)
        min_is = np.argmin(self.image, axis=2)

        for c in range(self.cols):
            for r in range(self.rows):
                min_i = min_is[r, c]
                self.image[r, c, min_i] += deltas[r, c]

    def __save(self, img):
        out_filename = filename_add_suffix(self.filename, suffix="out")
        cv2.imwrite(out_filename, img)

    def encode(self, message=str(uuid.uuid4())):
        print(f"encode message {message}")
        qr = self.__gen_qr(message)
        self.__add_qr(qr)
        self.__save(self.image)
        # img.show()


parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()

e = Encoder(args.filename)
e.encode()
