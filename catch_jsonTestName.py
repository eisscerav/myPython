import re

text = """
&&&& FAILED cudnnTest -RgraphRunner -backendEngine-1 -jsonTestName=LLM_no_dropout_abstract -kv=dim_b:2 -kv=dim_qh:2 -kv=dim_qs:512 -kv=dim_d:80 -kv=dim_kvh:2 -kv=dim_kvs:512 -kv=Tin:fp16 -kv=Tout:fp16 -kv=rtol:2.5e-3 -kv=atol:2.5e-3 -b -serialization1
"""


def demo():
    p = re.compile("jsonTestName=(\w+)")
    json_test_name = []
    # with open(filename, 'r') as f:
    contents = text.split("\n")
    for line in contents:
        m = re.search(p, line)
        if m:
            json_test_name.append(m.groups()[0])
    json_test_name = list(dict.fromkeys(json_test_name))
    for name in json_test_name:
        print(name)
    return


if __name__ == "__main__":
    demo()
