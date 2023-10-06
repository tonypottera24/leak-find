#!/usr/bin/env python

import argparse
from pathlib import Path
import cv2

from util import filename_add_suffix


class Decoder:
    def __init__(self, image):
        self.image = image
        self.rows, self.cols, _ = self.image.shape
        # print(f"self.image.shape {self.image.shape}")
        self.debug = True

    def decode(self, masked_image, gamma=1):
        masked_image = cv2.resize(masked_image, (self.rows, self.cols))
        diff_image = cv2.absdiff(self.image, masked_image)

        (b, g, r) = cv2.split(diff_image)
        _, b = cv2.threshold(b, gamma, 255, cv2.THRESH_BINARY_INV)
        # cv2.imwrite(filename_add_suffix(self.filename, "b"), b)

        _, g = cv2.threshold(g, gamma, 255, cv2.THRESH_BINARY_INV)
        # cv2.imwrite(filename_add_suffix(self.filename, "g"), g)

        _, r = cv2.threshold(r, gamma, 255, cv2.THRESH_BINARY_INV)
        # cv2.imwrite(filename_add_suffix(self.filename, "r"), r)

        diff_image = cv2.min(b, g)
        self.diff_image = cv2.min(diff_image, r)
        # diff_image = cv2.adaptiveThreshold(diff_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    def save(self, filename):
        filename = Path(filename)
        diff_filename = filename_add_suffix(filename, "qr")
        cv2.imwrite(diff_filename, self.diff_image)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("masked_filename")
    args = parser.parse_args()

    image = cv2.imread(args.filename)
    d = Decoder(image)
    masked_image = cv2.imread(args.masked_filename)
    d.decode(masked_image)
    d.save(args.filename)
