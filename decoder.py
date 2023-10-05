#!/usr/bin/env python

import argparse
from pathlib import Path
import cv2
import numpy as np

# from pyzbar import pyzbar

from util import filename_add_suffix


class Decoder:
    def __init__(self, filename):
        self.image = cv2.imread(filename)
        self.rows, self.cols, _ = self.image.shape
        # print(f"self.image.shape {self.image.shape}")
        self.filename = Path(filename)
        self.debug = True
        self.gamma = 3

    def decode(self, masked_filename):
        masked_image = cv2.imread(masked_filename)
        diff_image = cv2.absdiff(self.image, masked_image)

        (b, g, r) = cv2.split(diff_image)
        _, b = cv2.threshold(b, self.gamma, 255, cv2.THRESH_BINARY_INV)
        # cv2.imwrite(filename_add_suffix(self.filename, "b"), b)

        _, g = cv2.threshold(g, self.gamma, 255, cv2.THRESH_BINARY_INV)
        # cv2.imwrite(filename_add_suffix(self.filename, "g"), g)

        _, r = cv2.threshold(r, self.gamma, 255, cv2.THRESH_BINARY_INV)
        # cv2.imwrite(filename_add_suffix(self.filename, "r"), r)

        diff_image = cv2.min(b, g)
        diff_image = cv2.min(diff_image, r)

        # diff_image = cv2.adaptiveThreshold(diff_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        fname = filename_add_suffix(self.filename, "qr")
        cv2.imwrite(fname, diff_image)
        # value = pyzbar.decode(qr_image)

        # print(f"value {value}")
        # return value


parser = argparse.ArgumentParser()
parser.add_argument("filename")
parser.add_argument("masked_filename")
args = parser.parse_args()

d = Decoder(args.filename)
d.decode(args.masked_filename)
