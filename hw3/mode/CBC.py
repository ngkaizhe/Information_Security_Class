from Crypto.Cipher import AES
from PIL import Image
from .Helper import pad, convert_to_RGB


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
        orig_len = len(ct_byt)
        ct_byt = pad(ct_byt, self.bs)

        # pick 16 bytes per loop and encrypt
        pl_byt = b''
        pos = 0
        previous = iv
        while pos < len(ct_byt):
            block_text = ct_byt[pos: pos + 16]
            # encrypt part
            cipher = AES.new(key, AES.MODE_CBC, iv=previous)
            pl_byt += cipher.decrypt(block_text)
            previous = block_text
            pos += 16

        # change back arr1d to arr3d
        pl_arr3d = convert_to_RGB(pl_byt[:orig_len])

        # save back the image
        img = Image.new(im.mode, im.size)
        img.putdata(pl_arr3d)

        return img


if __name__ == '__main__':
    ecb = CBC()
    key1 = b'Sixteen byte key'
    iv1 = b'aaaaaaabbbbbb123'
    ecb.CBC_encrypt('../asset/bmp/test3.bmp', key1, iv1)
    ecb.CBC_decrypt('../asset/bmp/test3_en.bmp', key1, iv1)