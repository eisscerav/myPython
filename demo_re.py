import re

# more demo: https://www.cnblogs.com/CYHISTW/p/11363209.html
def demo():
    result = re.match('it', 'itcastle.con')
    g = result.group()

    m1 = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
    g0 = m1.group(0)
    g1 = m1.group(1)
    g12 = m1.group(1, 2)
    gs = m1.groups()
    m1_span = m1.span()
    m1_end = m1.end()

    m2 = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcolm Reynolds")
    g_dict = m2.groupdict()
    email = r"tony@tiremove_thisger.net"
    m = re.search("remove_this", email)
    email = email[:m.start()] + email[m.end():]

    re.match("c", "abcdef")  # No match
    re.search("c", "abcdef")  # Match
    re.search('^X', 'A\nB\nX', re.MULTILINE)  # Match

    m_fdall = re.findall(pattern='\d+', string='abafa 124ddwa56')
    print("done demo")


def demo_split():
    text = """Ross McFluff: 834.345.1254 155 Elm Street

    Ronald Heathmore: 892.345.3428 436 Finley Avenue
    Frank Burger: 925.541.7625 662 South Dogwood Way

    Heather Albrecht: 548.326.4584 919 Park Place"""
    entries = re.split("\n+", text)
    lst = [re.split(":? ", entry, 3) for entry in entries]


def demo_tmp():
    text = '__global__ void __launch_bounds__(256) memcpyWithTypeConversion(const int64_t size, T_IN const* src, T_OUT* dst) {     const int64_t index = (int64_t)blockIdx.x * blockDim.x + threadIdx.x;'
    # text = '__launch_bounds__(THREADS, 1) __global__ void softmax_fw_kernel_resident(struct cudnnTensorStruct g_imgIn,'
    # text = ':__launch_bounds__(THREADS) __global__ void softmax_fw_kernel(struct cudnnTensorStruct g_imgIn,'
    # p = r'\bsoftmax_fw_kernel\b'
    m = re.search("void (.*)\(", text)
    # m = re.search(p, text)
    kernel_name = m.group(1)
    span = m.span()
    kernel = text[span[0]:span[1]]
    print('done demo_tmp')


if __name__ == '__main__':
    demo_tmp()
