# Leak Find

* Demo: https://leak-find.streamlit.app/

This is a demo for how to embed (encode) a QR code into an image and decode it back.


## Usage:

### Encode

```
./encoder.py
usage: encoder.py [-h] [-m MESSAGE] [-g GAMMA] filename
```
* `filename`: the original image file
* `-m`: the message to be encoded in the image
* `-g`: how much do you want to distort the image

### Decode

```
./decoder.py
usage: decoder.py [-h] [-g GAMMA] filename masked_filename
```

* `filename`: the original image file
* `masked_filename`: the encoded image file
* `-g`: the threshold used to find the difference

## Contributions

If you have any questions or want to learn more about this research, please open an issue or send a mail to the following address.

* Po-Chu Hsu: tonypottera[at]gmail.com

## License

This project is licensed under the MIT License - see the LICENSE.txt file for details