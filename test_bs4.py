from bs4 import BeautifulSoup


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
###################################################


def QuickStart():
    soup = BeautifulSoup(html_doc, 'lxml')
    title = soup.title
    title_name = soup.title.name
    title_string = soup.title.string
    parent_name = soup.title.parent.name
    p = soup.p
    a = soup.a
    id_link3 = soup.find(id="link3")

    for link in soup.find_all('a'):
        print(link.get('href'))

    text = soup.get_text()
    print(text)


def demo():
    soup = BeautifulSoup('<b class="boldest">Extremely bold</b>')
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


def demo1():
    # Multi-valued attributes
    css_soup = BeautifulSoup('<p class="body strikeout"></p>')
    cls = css_soup.p['class']

    # more than one value, but it’s not a multi-valued attribute as defined by any version of the HTML standard
    id_soup = BeautifulSoup('<p id="my id"></p>')
    ids = id_soup.p['id']
    print(css_soup)

    # multiple attribute values are consolidated
    rel_soup = BeautifulSoup('<p>Back to the <a rel="index">homepage</a></p>')
    rel_soup.a['rel'] = ['index', 'contents']
    print(rel_soup.p)


if __name__ == '__main__':
    demo1()
