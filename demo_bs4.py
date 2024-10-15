import os.path

from bs4 import BeautifulSoup
import bs4
import re
from mako.template import Template

# refer to https://beautiful-soup-4.readthedocs.io/en/latest/
html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class
"""


###################################################
# soup = BeautifulSoup(open("index.html"))
# soup = BeautifulSoup("<html>data</html>")
# apt-get install Python-lxml
# pip install lxml
###################################################
def quick_start():
    soup = BeautifulSoup(html_doc, 'lxml')
    title = soup.title
    title_name = soup.title.name
    title_string = soup.title.string
    parent_name = soup.title.parent.name
    p = soup.p
    a = soup.a
    id_link3 = soup.find(id="link3")

    for link in soup.find_all('a'):
        ref = link.get('href')
        print(link.get('href'))

    text = soup.get_text()
    print(text)


def demo():
    # soup = BeautifulSoup('<p><b class="boldest">Extremely bold</b><p>')
    soup = BeautifulSoup('<p><b class="boldest">Extremely bold</b></p>')
    p = soup.p
    for sub_p in p.children:
        print(sub_p)
    tmp = p.b
    non = p.a
    tag = soup.b
    name = tag.name
    tag.name = "blockquote"

    class_ = tag['class']
    class_1 = tag.get('class')
    attrs = tag.attrs

    # add, modify and delete attribute of tag
    tag['class'] = 'verybold'
    tag['id'] = 1

    del tag['class']
    del tag['id']
    print("Done")


def demo_search_tree():
    # Multi-valued attributes
    css_soup = BeautifulSoup('<p class="body strikeout"></p>')
    # cls = css_soup.p['class']
    cls = css_soup.p.get('class')
    # more than one value, but it’s not a multi-valued attribute as defined by any version of the HTML standard
    id_soup = BeautifulSoup('<p id="my id"></p>')
    ids = id_soup.p['id']
    print(css_soup)

    # multiple attribute values are consolidated
    rel_soup = BeautifulSoup('<p>Back to the <a rel="index">homepage</a></p>')
    rel_soup.a['rel'] = ['index', 'contents']
    tag_p = rel_soup.p

    # Navigable string
    soup = BeautifulSoup('<b class="boldest">Extremely bold</b>')
    tag = soup.b
    str = tag.string
    # todo: tag.string = "No longer bold" ??
    tag.string.replace_with("No longer bold")

    # insert a soup
    doc = BeautifulSoup("<document><content/>INSERT FOOTER HERE</document", "lxml")
    footer = BeautifulSoup("<footer>Here's the footer</footer>", "xml")
    doc.find(text="INSERT FOOTER HERE").replace_with(footer)

    # Searching tree: A regular expression
    # https://beautiful-soup-4.readthedocs.io/en/latest/#a-regular-expression
    html_soup = BeautifulSoup(html_doc, 'lxml')
    for tag in html_soup.find_all(re.compile("^b")):
        print(tag.name)

    # https://beautiful-soup-4.readthedocs.io/en/latest/#a-list
    all_a_b = soup.find_all(["a", "b"])

    # find_all: https://beautiful-soup-4.readthedocs.io/en/latest/#find-all
    all_p_title = soup.find_all("p", "title")
    soup.find_all(id="link2")
    soup.find(string=re.compile("sisters"))
    soup.find_all(href=re.compile("elsie"), id='link1')

    data_soup = BeautifulSoup('<div data-foo="value">foo!</div>')
    # like the data-* attributes in HTML 5, have names that can’t be used as the names of keyword arguments
    # data_soup.find_all(data-foo = "value")
    data_soup.find_all(attrs={"data-foo": "value"})

    # Searching by CSS class
    # https://beautiful-soup-4.readthedocs.io/en/latest/#searching-by-css-class
    soup.find_all("a", class_="sister")
    soup.find_all(class_=re.compile("itl"))

    css_soup.select("p.strikeout.body")

    # going down https://beautiful-soup-4.readthedocs.io/en/latest/#going-down
    for child in soup.descendants:
        print(child)

    # going up: https://beautiful-soup-4.readthedocs.io/en/latest/#going-up
    # going sideways: https://beautiful-soup-4.readthedocs.io/en/latest/#going-sideways
    # https://beautiful-soup-4.readthedocs.io/en/latest/#going-back-and-forth

    # https://beautiful-soup-4.readthedocs.io/en/latest/#searching-the-tree
    soup.find_all(["a", "b"])

    print(rel_soup.p)


def demo_update_tags():
    # https://beautiful-soup-4.readthedocs.io/en/latest/#modifying-the-tree
    soup = BeautifulSoup('<b class="boldest">Extremely bold</b>')
    tag = soup.b
    tag.name = "blockquote"
    tag['class'] = 'verybold'
    tag['id'] = 1
    del tag['class']
    del tag['id']

    markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
    soup = BeautifulSoup(markup)
    tag = soup.a
    tag.string = "New link text."

    soup = BeautifulSoup("<a>Foo</a>")
    soup.a.append("Bar")

    soup = BeautifulSoup("<a>Soup</a>")
    soup.a.extend(["'s", " ", "on"])

    soup = BeautifulSoup("<b></b>")
    tag = soup.b
    tag.append("Hello")
    new_string = bs4.NavigableString(" there")
    tag.append(new_string)

    # new tag
    soup = BeautifulSoup("<b></b>")
    original_tag = soup.b
    new_tag = soup.new_tag("a", href="http://www.example.com")
    original_tag.append(new_tag)
    new_tag.string = "Link text."

    markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
    soup = BeautifulSoup(markup)
    tag = soup.a
    tag.insert(1, "but did not endorse ")

    soup = BeautifulSoup("<b>stop</b>")
    tag = soup.new_tag("i")
    tag.string = "Don't"
    soup.b.string.insert_before(tag)

    markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
    soup = BeautifulSoup(markup)
    tag = soup.a
    tag.clear()

    markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
    soup = BeautifulSoup(markup)
    a_tag = soup.a
    i_tag = soup.i.extract()

    markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
    soup = BeautifulSoup(markup)
    a_tag = soup.a
    new_tag = soup.new_tag("b")
    new_tag.string = "example.net"
    a_tag.i.replace_with(new_tag)

    soup = BeautifulSoup("<p>I wish I was bold.</p>")
    soup.p.string.wrap(soup.new_tag("b"))
    soup.p.wrap(soup.new_tag("div"))

    markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
    soup = BeautifulSoup(markup)
    a_tag = soup.a
    a_tag.i.unwrap()

    markup = '<a href="http://example.com/">\nI linked to <i>example.com</i>\n</a>'
    soup = BeautifulSoup(markup)
    txt = soup.get_text()
    txt1 = soup.i.get_text()

    print(soup.prettify())


def generate_html_report(project_name="coverity_nccl", td_items=[]):
    report_name = f"{project_name}.html"

    t = Template(filename='data/coverity_report.mako')
    data = {
        "project_name": project_name,
        "td_items": td_items,
    }
    r = t.render(**data)
    with open(report_name, "w") as fp:
        fp.write(r)
    return report_name


def remove_similar_items(td_list):
    ret = [td_list[0]]
    del td_list[0]
    b_similar = False
    for td in td_list:
        for each_ret in ret:
            if each_ret.get("Checker") == td.get("Checker") and each_ret.get("file") == td.get("file") and \
                    each_ret.get("Line") == td.get("Line") and each_ret.get("Classification") == td.get("Classification"):
                b_similar = True
                break
        if b_similar:
            b_similar = False
        else:
            ret.append(td)
            b_similar = False
    return ret


def coverity_report():
    original_td_elements = []
    # soup = BeautifulSoup(open("index.html"), 'lxml')
    soup = BeautifulSoup(open(os.path.join("html", "index.html")), 'lxml')
    all_trs = soup.find_all(attrs={"bgcolor": "#F8F8F2"})
    for tr in all_trs:
        td_dict = {}
        tr_tds = tr.find_all('td')
        for i, tr_td in enumerate(tr_tds):
            td_val = tr_td.get_text()
            if i == 0:
                td_dict['ID'] = td_val
            elif i == 1:
                td_dict['Checker'] = td_val
            elif i == 2:
                td_dict['tag_File'] = tr_td
                td_dict['file_href'] = tr_td.find('a').get('href')
                td_dict['File'] = td_val
            elif i == 3:
                td_dict['Line'] = td_val
            elif i == 4:
                td_val = td_val.replace("<", "&lt;")
                td_val = td_val.replace(">", "&gt;")
                td_dict['Function'] = td_val
            elif i == 5:
                td_dict['Classification'] = td_val
        if td_dict:
            original_td_elements.append(td_dict)
    no_similar_tds = remove_similar_items(original_td_elements)
    report_name = generate_html_report(td_items=no_similar_tds)
    return report_name


def update_html():
    soup = BeautifulSoup(open(os.path.join("html", "set_value.html")), 'lxml')
    tag_id_test1 = soup.find(id="test1")
    if tag_id_test1:
        tag_id_test1["class"] = "ffan_v2"
    with open('html/updated.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))
    return


def disable_negative_statements():
    disabled_lines = 0
    soup = BeautifulSoup(open(os.path.join("report", "bootstrap.cc.html")), 'lxml')
    all_no_cvg_tags = soup.find_all(class_="no-cvg fail-marker")
    num_no_cvg = len(all_no_cvg_tags)
    for no_cvg_tag in all_no_cvg_tags:
        print(no_cvg_tag)
        text = no_cvg_tag.text
        nccl_check_p1 = re.compile(r".*if \(RES != ncclSuccess && RES != ncclInProgress\) {")
        nccl_check_p2 = re.compile(r".*if \(ncclDebugNoWarn == 0\)")
        nccl_check_p3 = re.compile(r".*ncclDebugLog\(NCCL_LOG_([a-zA-Z]+),*")
        nccl_check_p4 = re.compile(r".*return RES;")
        common_err_p1 = re.compile(r".*return nccl([a-zA-Z]+);")
        common_err_p2 = re.compile(r"\s+(\d+) (\d+) (\d+)\s+;")
        common_err_p3 = re.compile(r".*while (0);")
        nccl_check_m1 = re.search(nccl_check_p1, text)
        nccl_check_m2 = re.search(nccl_check_p2, text)
        nccl_check_m3 = re.search(nccl_check_p3, text)
        nccl_check_m4 = re.search(nccl_check_p4, text)
        common_m1 = re.search(common_err_p1, text)
        common_m2 = re.search(common_err_p2, text)
        common_m3 = re.search(common_err_p3, text)
        if common_m1 and common_m1.group(1) != "Success":
            no_cvg_tag["class"] = "na-cvg"
            disabled_lines += 1
        elif common_m2 or common_m3:
            no_cvg_tag["class"] = "na-cvg"
            disabled_lines += 1
        elif nccl_check_m1 or nccl_check_m2 or nccl_check_m3 or nccl_check_m4:
            no_cvg_tag["class"] = "na-cvg"
            disabled_lines += 1
    with open('report/mod_bootstrap.cc.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))
    return


def main():
    # demo()
    disable_negative_statements()
    # coverity_report()
    # quick_start()
    # demo_search_tree()
    # demo2()


if __name__ == '__main__':
    main()
