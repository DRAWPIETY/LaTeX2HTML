from  latex_parse import yacc
import re

def clear_text(text):
    lines=[]
    for line in text.split('\n'):
        line=line.strip()
        if len(line)>0:
            lines.append(line)
    return ' '.join(lines)

def getitem(t):
    item = ''
    if t.getdata()=='[ITEM]':
        item  = '<li>%s</li>\n'%t.getchildren()[0].getdata()
    return item


def getitemize(t):
    itemize =''
    for node in t.getchildren():
        if node.getdata() == '[ITEM]':
            itemize += getitem(node)
        elif node.getdata() == '[ITEMS]':
            itemize += getitemize(node)
    return itemize

def gettxt(t):
    txt = ''
    for node in t.getchildren():
        if node.getdata() == '[ITEMIZE]':
            txt += '<ul>\n%s</ul>\n' % getitemize(node)
        else:
            txt += '<p>%s</p>\n' % node.getdata()
    return txt


def getsubsection(t):
    subsection =''
    for node in t.getchildren():
        if '[SUBSECTION]' in node.getdata():
            subsection += '<h4><li>%s</li></h4>\n' % p.findall(node.getdata())[0]
            for i in node.getchildren():
                if i.getdata()=='[TXT]':
                    subsection += gettxt(i)
        elif node.getdata() == '[SUBSECTIONS]':
            subsection += getsubsection(node)
    return subsection

def getsection(t):
    section =''
    for node in t.getchildren():
        if '[SECTION]' in node.getdata():
            section += '<h3><li>%s</li></h3>\n' % p.findall(node.getdata())[0]
            for i in node.getchildren():
                if i.getdata()=='[TXT]':
                    section += gettxt(i)
                elif i.getdata()=='[SUBSECTIONS]':
                    section += '<ol>\n%s</ol>\n' % getsubsection(i)
        elif node.getdata() == '[SECTIONS]':
            section += getsection(node)
    return section

def getcontent(t):
    content = ''
    for i in t.getchildren():
        if i.getdata() == '[TITLE]':
            content += '<h1 align="center">%s</h1>\n' % i.getchildren()[0].getdata()

        elif i.getdata() == '[AUTHOR]':
            content += '<h3 align="center">%s</h3>\n' % i.getchildren()[0].getdata()

        elif i.getdata() == '[ABSTRACT]':
            content += '<h3 align="center">abstract</h3>\n<p>%s</p>\n' % i.getchildren()[0].getdata()

        elif i.getdata() == '[SECTIONS]':
            content += '<ol>\n%s</ol>'% getsection(i)

    return content

def latex2html(t):
    if t.getchildren()[0].getdata()=='[CONTENT]':
        html = getcontent(t.getchildren()[0])
    return html

data=clear_text(open('example2.tex').read())
root=yacc.parse(data)
p = re.compile(r'SECTION]\((.+?)\)')
html_txt = latex2html(root)
print html_txt
