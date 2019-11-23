from Crypto.Cipher import AES
import numpy


# Maps the RGB
def convert_to_RGB(data):
    r, g, b = tuple(map(lambda d: [data[i] for i in range(0, len(data)) if i % 3 == d], [0, 1, 2]))
    pixels = tuple(zip(r, g, b))
    return pixels


def pad(data, block_size):
    data = data
    padding_size = (block_size - (len(data) % block_size))
    padding = (chr(padding_size) * padding_size).encode('utf-8')
    return data + padding


def unpad(data, block_size):
    padding = data[-1]
    if padding > block_size:
        raise Exception("Something wrong, are you trying to hack? The value of padding is:", padding,
                        "The value of block size is: ", block_size)

    return data[:-padding]


def encrypt(data):
    key = b'Sixteen byte key'
    cipher = AES.new(key, AES.MODE_ECB)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    return ct_bytes


def decrypt(data):
    key = b'Sixteen byte key'
    cipher = AES.new(key, AES.MODE_ECB)
    plain_bytes = unpad(cipher.decrypt(data), AES.block_size)
    return plain_bytes


if __name__ == '__main__':
    key = b'Sixteen byte key'
    bs = AES.block_size

    arr1d = numpy.arange(201)
    print("arr1d is : ", arr1d)
    arr1d_str = ''.join([chr(i) for i in arr1d])
    print("arr1d_str is: ", arr1d_str)
    arr1d_byt = pad(arr1d_str.encode(), bs)

    # pick 16 bytes per loop and encrypt
    ct_byt = b''
    pos = 0
    while pos < len(arr1d_byt):
        block_text = arr1d_byt[pos: pos+16]
        # encrypt part
        cipher = AES.new(key, AES.MODE_ECB)
        ct_byt += cipher.encrypt(block_text)
        pos += 16

    print("ciphertext is: ", ct_byt, "\nArray form: ", [i for i in ct_byt])

    # pick 16 bytes per loop and encrypt
    pl = b''
    pos = 0
    while pos < len(ct_byt):
        block_text = ct_byt[pos: pos + 16]
        # encrypt part
        cipher = AES.new(key, AES.MODE_ECB)
        pl += cipher.decrypt(block_text)
        pos += 16

    pl = unpad(pl, bs)
    pl_arr = [ord(i) for i in pl]
    print("plaintext is: ", pl)
    print("Array is: ", numpy.array(pl_arr))

