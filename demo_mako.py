from mako.template import Template
from mako.lookup import TemplateLookup


class Person:
    def __init__(self, name, age, link):
        self.name = name
        self.age = age
        self.link = link


def demo_mako_template():
    t = Template(filename='data/demo.mako')
    my_dict = {
        'company': 'nvidia',
        'value': 300
    }
    # r1 = t.render(name='mako', x=5, y=2, my_company=my_dict)
    p1 = Person('fancy', 40, "http://fancy.com")
    p2 = Person('dili', 39, "http://dili/com")
    persons = [p1, p2]
    mylist = [
        # {'comp': 'nv', 'val': 200},
        # {'comp': 'google', 'val': 400}
    ]
    data = {
        'name': 'mako',
        'x': 5,
        'y': 2,
        'my_company': my_dict,
        'person': p1,
        # 'persons': persons,
        # 'mylist': ['fancy', 'ffan', 'ffan_local']
        'mylist': mylist
    }
    r2 = t.render(**data)
    with open("demo_mako.html", "w") as fp:
        fp.write(r2)
    print(r2)

    # refer to https://docs.makotemplates.org/en/latest/usage.html#using-templatelookup
    # mylookup = TemplateLookup(directories=['data'])
    # mytemplate = Template("""<%include file="demo.tmpl"/> hello world!""", lookup=mylookup)
    # r2 = mytemplate.render(name='TemplateLookup')
    # print(r2)


def demo_generate_report():
    t = Template(filename='data/report.mako')
    td_items = []
    td_item= {'ID': 1, 'File': "file1.txt", 'file_href': "www.abc.com"}
    td_items.append(td_item)
    td_item['ID'] = 2
    td_item['File'] = "file2.txt"
    td_item['file_href'] = "www.xyc.com"
    td_items.append(td_item)

    data = {
        'project_name': 'demo_project',
        'td_items': td_items,
        'original_link': "www.old.com"
    }

    r2 = t.render(**data)
    with open("demo_report.html", "w") as fp:
        fp.write(r2)

    print('done')
    return


if __name__ == '__main__':
    demo_generate_report()
