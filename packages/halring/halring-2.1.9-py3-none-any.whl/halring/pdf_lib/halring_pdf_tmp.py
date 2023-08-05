# -*- coding:utf-8 -*-
import pdfkit  # 需安装 pdfkit 第三方包 "pip install pdfkit" 以及第三方依赖 "wkhtmltopdf"




# word2pdf("./", "./")
# pdfkit.from_url('https://www.hao123.com/', 'out.pdf')
# pdfkit.from_url('https://www.163.com', 'test1.pdf')
# pdfkit.from_url('https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf', 'test2.pdf')
# pdfkit.from_string('Hello!', 'out.pdf')
# pdfkit.from_file("简历.docx", "out2.pdf")

# pdfkit.from_file('test.html', 'out.pdf')
import pdfkit  # pip install pdfkit
from pydocx import PyDocX  # pip install pydocx

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


import pypandoc

# with open('README2.md') as f:
#     content = f.read()
# output = pypandoc.convert_text(content, 'html', format='md')
# print(output)
# with open('test.html', "w+") as f:
#     f.write(output)
#     print(output)
pdfkit.from_file('test.html', 'result33333.pdf')
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
