def demo():
    d1 = {
        "name": "fancy",
        "age": 42
    }
    d2 = { "age": 42 }
    d2.update(d1)
    print('done demo')


if __name__ == '__main__':
    demo()
