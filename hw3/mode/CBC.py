from Crypto.Cipher import AES
from PIL import Image
from .Helper import pad, convert_to_RGB
import os


class CBC(object):
    def __init__(self):
        self.bs = AES.block_size

    def CBC_encrypt(self, source, key, iv):
        im = Image.open(source)

        # generate bytes form of image
        pl_byt = im.convert("RGB").tobytes()
        orig_len = len(pl_byt)
        pl_byt = pad(pl_byt, self.bs)

        # pick 16 bytes per loop and encrypt
        ct_byt = b''
        pos = 0
        previous = iv
        while pos < len(pl_byt):
            block_text = pl_byt[pos: pos + 16]
            # encrypt part
            cipher = AES.new(key, AES.MODE_CBC, iv=previous)
            previous = cipher.encrypt(block_text)
            ct_byt += previous
            pos += 16

        # change back arr1d to arr3d
        ct_arr3d = convert_to_RGB(ct_byt[:orig_len])

        # save back the image
        img = Image.new(im.mode, im.size)
        img.putdata(ct_arr3d)

        return img

    def CBC_decrypt(self, source, key, iv):
        im = Image.open(source)

        # generate bytes form of image
        ct_byt = im.convert("RGB").tobytes()

        # drop bytes without padding.
        ct_dec_len = len(ct_byt) - len(ct_byt) % 16

        # pick 16 bytes per loop and decrypt
        pl_byt = b''
        pos = 0
        previous = iv
        # decrypt part
        while pos+16 <= ct_dec_len:
            block_text = ct_byt[pos: pos + 16]
            plain = AES.new(key, AES.MODE_CBC, iv=previous)
            previous = block_text
            pl_byt += plain.decrypt(block_text)
            pos += 16

        img = Image.frombytes("RGB", im.size, pl_byt)
        return img


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    ecb = CBC()
    key1 = b'Sixteen byte key'
    iv1 = b'aaaaaaabbbbbb123'
    ecb.CBC_encrypt('../asset/bmp/test3.bmp', key1, iv1)
    ecb.CBC_decrypt('../asset/bmp/test3_en.bmp', key1, iv1)
