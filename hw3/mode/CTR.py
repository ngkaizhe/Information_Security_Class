from Crypto.Cipher import AES
from PIL import Image
from .Helper import pad, convert_to_RGB
import os


class CTR(object):
    def __init__(self):
        self.bs = AES.block_size

    def CTR_encrypt(self, source, key, nonce, initial_value):
        im = Image.open(source)

        # generate bytes form of image
        pl_byt = im.convert("RGB").tobytes()
        orig_len = len(pl_byt)
        pl_byt = pad(pl_byt, self.bs)

        # pick 16 bytes per loop and encrypt
        ct_byt = b''
        pos = 0
        while pos < len(pl_byt):
            block_text = pl_byt[pos: pos + 16]
            # encrypt part
            cipher = AES.new(key, AES.MODE_CTR, nonce=nonce,
                             initial_value=initial_value)
            ct_byt += cipher.encrypt(block_text)

            initial_value += 1
            pos += 16

        # change back arr1d to arr3d
        ct_arr3d = convert_to_RGB(ct_byt[:orig_len])

        # save back the image
        img = Image.new(im.mode, im.size)
        img.putdata(ct_arr3d)

        return img

    def CTR_decrypt(self, source, key, nonce, initial_value):
        im = Image.open(source)

        # generate bytes form of image
        ct_byt = im.convert("RGB").tobytes()

        # drop bytes without padding.
        ct_dec_len = len(ct_byt) - len(ct_byt) % 16

        # pick 16 bytes per loop and decrypt
        pl_byt = b''
        pos = 0
        # decrypt part
        while pos+16 <= ct_dec_len:
            block_text = ct_byt[pos: pos + 16]
            plain = AES.new(key, AES.MODE_CTR, nonce=nonce,
                            initial_value=initial_value)
            pl_byt += plain.decrypt(block_text)

            initial_value += 1
            pos += 16

        # save back the image
        img = Image.frombytes("RGB", im.size, pl_byt)

        return img


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    ctr = CTR()
    key1 = b'Sixteen byte key'
    nonce1 = b'ngkaizhe'
    initial_value1 = 123
    ctr.CTR_encrypt('../asset/bmp/test6.bmp', key1, nonce1, initial_value1)
    ctr.CTR_decrypt('../asset/bmp/test6_en.bmp', key1, nonce1, initial_value1)
