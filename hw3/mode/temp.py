from PIL import Image
from Crypto.Cipher import AES
from Padding import unpad, pad, convert_to_RGB, byt_XOR


class CBC(object):
    def __init__(self):
        self.bs = AES.block_size
        self.key = b'Sixteen byte key'
        self.iv = b'aaaaaaabbbbbb123'

    def CBC_encrypt(self, pl_byt):
        pl_byt = pad(pl_byt, self.bs)

        # pick 16 bytes per loop and encrypt
        ct_byt = b''
        pos = 0
        previous = self.iv
        while pos < len(pl_byt):
            block_text = pl_byt[pos: pos + 16]

            # encrypt part
            cipher = AES.new(self.key, AES.MODE_CBC, iv=previous)
            previous = cipher.encrypt(block_text)
            ct_byt += previous
            pos += 16

        # change back arr1d to arr3d
        return ct_byt

    def CBC_decrypt(self, ct_byt):
        # pick 16 bytes per loop and encrypt
        pl_byt = b''
        pos = 0
        previous = self.iv
        while pos < len(ct_byt):
            block_text = ct_byt[pos: pos + 16]
            # encrypt part
            cipher = AES.new(self.key, AES.MODE_CBC, iv=previous)
            pl_byt += cipher.decrypt(block_text)
            previous = block_text
            pos += 16

        # change back arr1d to arr3d
        return unpad(pl_byt, self.bs)


if __name__ == '__main__':
    ecb = CBC()
    data = b'testing123testing1234589vu489j8gtjdor4wef4g4g!!!!!!'
    en = ecb.CBC_encrypt(data)
    print("Encrypt value is: ", en)
    de = ecb.CBC_decrypt(en)
    print("Decrypt value is: ", de)

