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
        rows, cols, _ = masked_image.shape
        # print(f"masked_image.shape {masked_image.shape}")
        qr_image = np.zeros((rows, cols, 3), np.uint8)
        # print(f"qr_image.shape {qr_image.shape}")
        for x in range(self.rows):
            for y in range(self.cols):
                op = self.image[x, y]
                mp = masked_image[x, y]
                # print(f"op {op}")
                # print(f"mp {mp}")
                qr_image[x, y] = [255, 255, 255]
                for i in range(len(op)):
                    if abs(int(op[i]) - int(mp[i])) >= self.gamma:
                        qr_image[x, y] = [0, 0, 0]
        fname = filename_add_suffix(self.filename, "qr")
        cv2.imwrite(fname, qr_image)
        # value = pyzbar.decode(qr_image)

        # print(f"value {value}")
        # return value


parser = argparse.ArgumentParser()
parser.add_argument("filename")
parser.add_argument("masked_filename")
args = parser.parse_args()

d = Decoder(args.filename)
d.decode(args.masked_filename)
