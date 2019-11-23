from Crypto.Cipher import AES
from PIL import Image
from mode.Helper import pad, convert_to_RGB


class ECB(object):
    def __init__(self):
        self.bs = AES.block_size

    def ECB_encrypt(self, source, key):
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
            cipher = AES.new(key, AES.MODE_ECB)
            ct_byt += cipher.encrypt(block_text)
            pos += 16

        # change back arr1d to arr3d
        ct_arr3d = convert_to_RGB(ct_byt[:orig_len])

        # save back the image
        img = Image.new(im.mode, im.size)
        img.putdata(ct_arr3d)

        return img

    def ECB_decrypt(self, source, key):
        im = Image.open(source)

        # generate bytes form of image
        ct_byt = im.convert("RGB").tobytes()
        orig_len = len(ct_byt)
        ct_byt = pad(ct_byt, self.bs)

        # pick 16 bytes per loop and encrypt
        pl_byt = b''
        pos = 0
        while pos < len(ct_byt):
            block_text = ct_byt[pos: pos + 16]
            # encrypt part
            cipher = AES.new(key, AES.MODE_ECB)
            pl_byt += cipher.decrypt(block_text)
            pos += 16

        # change back arr1d to arr3d
        pl_arr3d = convert_to_RGB(pl_byt[:orig_len])

        # save back the image
        img = Image.new(im.mode, im.size)
        img.putdata(pl_arr3d)

        # img.save('C:\\Users\\User\\Desktop\\hw3\\asset\\tempResult_de.ppm')
        return img


if __name__ == '__main__':
    ecb = ECB()
    key1 = b'Sixteen byte key'
    img1 = ecb.ECB_encrypt('C:\\Users\\User\\Desktop\\hw3\\asset\\test3.bmp', b'ECB0000000000000')
    img1.save('C:\\Users\\User\\Desktop\\hw3\\asset\\tempResult_en.ppm')

    img2 = ecb.ECB_decrypt('C:\\Users\\User\\Desktop\\hw3\\asset\\tempResult_en.ppm', b'ECB0000000000000')
    img2.save('C:\\Users\\User\\Desktop\\hw3\\asset\\tempResult_de.ppm')
