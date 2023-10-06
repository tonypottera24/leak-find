import hashlib
import numpy as np
import streamlit as st
from decoder import Decoder
from encoder_cv import Encoder
from PIL import Image, ImageOps


@st.cache_data
def get_hash(upload):
    return hashlib.md5(upload.getvalue()).hexdigest()


@st.cache_data
def encode_image(upload, message, gamma):
    ori_img = Image.open(upload)
    ori_img = ImageOps.exif_transpose(ori_img)
    e = Encoder(np.array(ori_img))
    e.encode(message=message, gamma=gamma)
    return e.image


@st.cache_data
def decode_image(ori_upload, masked_upload, gamma):
    ori_img = Image.open(ori_upload)
    ori_img = ImageOps.exif_transpose(ori_img)
    d = Decoder(np.array(ori_img))
    if type(masked_upload) is np.ndarray:
        masked_img = masked_upload
    else:
        masked_img = Image.open(masked_upload)
        masked_upload = ImageOps.exif_transpose(masked_upload)
        masked_img = np.array(masked_img)
    d.decode(masked_img, gamma=gamma)
    return d.diff_image


st.title("Leak Find")

st.header("Original Image")

original_upload = st.file_uploader("Choose a file", type=["png", "jpg", "jpeg"], key="original_upload")

if original_upload:
    if "encoded" not in st.session_state:
        st.session_state.encoded = False
    if "from_encoded" not in st.session_state:
        st.session_state.from_encoded = False

    col1, col2 = st.columns(2)
    with col1:
        st.header("Encode")
        message = st.text_input("message", value=get_hash(original_upload), key="encode_message")
        gamma = st.number_input("gamma", value=1, min_value=0, max_value=255, key="encode_gamma")
        encode_bt = st.button("Encode")
        print(st.session_state)
        if encode_bt:
            st.session_state.encoded = True
        if st.session_state.encoded:
            encoded_image = encode_image(original_upload, message, gamma)
            st.image(encoded_image, caption="Encoded Image")

    with col2:
        st.header("Decode")
        decoder_upload = None
        if st.session_state.encoded:
            from_encoded_bt = st.button("From Encoded", key="from_encoded_bt")
            upload_new_bt = st.button("Upload Image")
            if upload_new_bt:
                st.session_state.from_encoded = False
                st.session_state.encoded = False
                st.rerun()
            gamma = st.number_input("gamma", value=1, min_value=0, max_value=255)
            if from_encoded_bt:
                st.session_state.from_encoded = True
            if st.session_state.from_encoded:
                encoded_image = encode_image(
                    original_upload, st.session_state.encode_message, st.session_state.encode_gamma
                )
                decoded_image = decode_image(original_upload, encoded_image, gamma)
                st.image(decoded_image, caption="Decoded Image")
        else:
            decoder_upload = st.file_uploader("Choose a file", type=["png", "jpg", "jpeg"], key="decoder_upload")
            gamma = st.number_input("gamma", value=1, min_value=0, max_value=255)
            if decoder_upload:
                decoded_image = decode_image(original_upload, decoder_upload, gamma)
                st.image(decoded_image, caption="Decoded Image")
