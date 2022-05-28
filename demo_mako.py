from mako.template import Template
from mako.lookup import TemplateLookup


def demo_mako_template():
    t = Template(filename='data/demo.tmpl')
    r = t.render(name='mako',x=1, y=2)
    print(r)

    # refer to https://docs.makotemplates.org/en/latest/usage.html#using-templatelookup
    # mylookup = TemplateLookup(directories=['data'])
    # mytemplate = Template("""<%include file="demo.tmpl"/> hello world!""", lookup=mylookup)
    # r2 = mytemplate.render(name='TemplateLookup')
    # print(r2)


if __name__ == '__main__':
    demo_mako_template()