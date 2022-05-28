from mako.template import Template
from mako.lookup import TemplateLookup

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

def demo_mako_template():
    t = Template(filename='data/demo.tmpl')
    my_dict = {
        'company': 'nvidia',
        'value': 300
    }
    # r1 = t.render(name='mako', x=5, y=2, my_company=my_dict)
    person = Person('fancy', 40)
    data = {
        'name': 'mako',
        'x': 5,
        'y': 2,
        'my_company': my_dict,
        'person': person
    }
    r2 = t.render(**data)
    print(r2)

    # refer to https://docs.makotemplates.org/en/latest/usage.html#using-templatelookup
    # mylookup = TemplateLookup(directories=['data'])
    # mytemplate = Template("""<%include file="demo.tmpl"/> hello world!""", lookup=mylookup)
    # r2 = mytemplate.render(name='TemplateLookup')
    # print(r2)


if __name__ == '__main__':
    demo_mako_template()