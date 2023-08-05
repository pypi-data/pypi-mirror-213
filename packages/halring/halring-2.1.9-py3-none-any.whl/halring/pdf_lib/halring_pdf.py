# -*- coding:utf-8 -*-
import os
import pypandoc  # 需安装 pypandoc 第三方包 "pip install pypandoc" 以及第三方依赖 "pandoc"
import pdfkit    # 需安装 pdfkit 第三方包 "pip install pdfkit" 以及第三方依赖 "wkhtmltopdf"


class PdfUtil(object):

    def __init__(self):
        self.markdonw_file = None
        self.output_pdf = None

    def write_raw_index(self, path, text):
        # 在csv文件中第一行添加索引字段
        with open(path, 'r+', encoding='utf-8') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(text + '\n' + content)

    def markdown_to_pdf(self, markdonw_file, output_pdf):
        """
        markdown 文件转为 pdf
        """
        with open(markdonw_file, encoding='utf-8') as f:
            content = f.read()
            pypandoc.convert_text(content, 'html', format='md', outputfile="test.html")
        self.write_raw_index("test.html", """<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> """)
        pdfkit.from_file("test.html", output_pdf)
        if os.path.exists("test.html"):
            os.remove("test.html")


    def url_to_pdf(self, url, output_pdf):
        """
        url 转 pdf
        """
        pdfkit.from_url(url, output_pdf)


if __name__ == '__main__':
    pdf_util = PdfUtil()
    pdf_util.markdown_to_pdf(markdonw_file='README.md', output_pdf='test.pdf')
    # pdf_util.url_to_pdf('https://www.hao123.com', 'test1.pdf')