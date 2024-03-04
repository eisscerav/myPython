import base64
import os


def demo():
    sample = b'We love nvidia'
    encode = base64.b64encode(sample)
    decode = base64.b64decode(encode).decode()
    # decode = base64.b64decode(encode)

    print(f"Encoded string: {decode}")


if __name__ == '__main__':
    demo()
