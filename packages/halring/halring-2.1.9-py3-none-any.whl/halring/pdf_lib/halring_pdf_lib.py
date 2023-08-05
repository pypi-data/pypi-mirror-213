# -*- coding:utf-8 -*-
import os
import pdfkit  # 需安装 pdfkit 第三方包 "pip install pdfkit" 以及第三方依赖 "wkhtmltopdf"
import pypandoc


# with open('README.md', encoding='utf-8') as f:
#     content = f.read()
#     pypandoc.convert_text(content, 'html', format='md', outputfile="test.html" )
#
# def write_raw_index(path, text):
#     # 在csv文件中第一行添加索引字段
#     with open(path, 'r+', encoding='utf-8') as f:
#         content = f.read()
#         f.seek(0, 0)
#         f.write(text + '\n' + content)
#
# write_raw_index("test.html", """<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> """)
#
# pdfkit.from_file("test.html", "test.pdf")
# # os.remove("test.html")
# pxd = 1

class PdfTransform(object):
    def __init__(self):
        pass

    def html_to_docx(self, html_path=None, outputfile=None):
        # 将当前目录下html目录中的1.html网页文件 读取出来，然后转换成.docx文件，文件名为file2.docx，并保存在当前目录下的doc文件夹中
        with open(html_path, encoding='utf-8') as f:
            html_content = f.read()
        pypandoc.convert_text(html_content, 'docx', 'html', outputfile=outputfile)

    def markdown_to_html(self, markdown_path=None, outputfile=None):
        with open('README.md') as f:
            content = f.read()
        out_put = pypandoc.convert_text(content, to='html', format='md', outputfile='test22.html', extra_args=["+RTS", "-K64m", "-RTS"])
        print(out_put)

    # def doc_to


if __name__ == '__main__':
    ...
    # PdfTransform().markdown_to_html('README2.md', "test.html")
    # PdfTransform().html_to_docx("test.html", "file2.docx")


# word2pdf("./", "./")
# pdfkit.from_url('https://www.hao123.com/', 'out.pdf')
# pdfkit.from_url('https://www.163.com', 'test1.pdf')
# pdfkit.from_url('https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf', 'test2.pdf')
# pdfkit.from_string('Hello!', 'out.pdf')
# pdfkit.from_file("简历.docx", "out2.pdf")

    # pdfkit.from_file('test.html', 'out.pdf')
# import pdfkit  # pip install pdfkit
# from pydocx import PyDocX  # pip install pydocx

# html = PyDocX.to_html('简历.docx')
# print(html)
# f = open('简1.html', 'w')
# f.write(html)
# f.close()

#pdfkit.from_file('html1.html', 'test3.pdf')
# pdfkit.from_string(html, '简历1.pdf')




# html = """
# <html>
# <head>
# <meta charset="utf-8" />
# </head>
# <body>
#   <p>你好，这是一个html字符串转为pdf的测试文件</p>
# </body>
# </html>
# """
#
# pdfkit.from_string(html, 'html_string_test.pdf')


# https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf
# 需安装 pdfkit 第三方包 "pip install pdfkit" 以及第三方依赖 "wkhtmltopdf"
# import pdfkit
# html = PyDocX.to_html('1.docx')
# with open('test.html', "w+") as f:
#     f.write(html)
#     f.close()
# pdfkit.from_file('test.html', 'result.pdf')


# import pypandoc
#
# with open('README2.md') as f:
#     content = f.read()
# output = pypandoc.convert_text(content, 'html', format='md')
# print(output)
# with open('test.html', "w+") as f:
#     f.write(output)
#     print(output)
# pdfkit.from_file('test.html', 'result33333.pdf')
"""
    转化文件的格式。
    convert(source, to, format=None, extra_args=(), encoding='utf-8', outputfile=None, filters=None)
    parameter-
        source：源文件
        to：目标文件的格式，比如html、rst、md等
        format：源文件的格式，比如html、rst、md等。默认为None，则会自动检测
        encoding：指定编码集
    outputfile：目标文件，比如test.html（注意outputfile的后缀要和to一致）
"""
# output = pypandoc.convert_text(input, 'rst', format='md')  # html -> markdown

# import pdflatex
#
# # 定义输入和输出文件的路径
# input_file = 'README2.md'
# output_file = 'README2.docx'
#
# print(pypandoc.get_pandoc_version())
# # 调用pypandoc库进行转换
# pypandoc.convert_file(input_file, 'docx', outputfile=output_file,)

"""
 1039  brew install Caskroom/cask/wkhtmltopdf
 1046  brew install pandoc
"""
