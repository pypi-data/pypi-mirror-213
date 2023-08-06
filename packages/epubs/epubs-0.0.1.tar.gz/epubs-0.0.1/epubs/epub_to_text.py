# -*- coding: UTF-8 -*-
# @Time : 2022/11/30 17:50
# @Author : 刘洪波
import ebooklib
from ebooklib import epub
from pathlib import Path
import html2text


class Epub2Text(object):
    def __init__(self, file_path: str, save_path: str = None, overwrite=False):
        self.file_path = file_path
        self.save_path = Path(save_path) if save_path else None
        self.overwrite = overwrite  # True 重新生成， False不重新生成

    def convert(self, func=None):
        """
        将epub数据转换成 text
        """
        result = []

        book = epub.read_epub(self.file_path)
        if book:
            if self.save_path:
                if self.save_path.exists():
                    print(f'{str(self.save_path)} Directory already exists.')
                    if not self.overwrite:
                        return
                else:
                    self.save_path.mkdir(exist_ok=True)
                for html in book.get_items():
                    if html.get_type() == ebooklib.ITEM_DOCUMENT:
                        self.save_data(html)
            else:
                for html in book.get_items():
                    if html.get_type() == ebooklib.ITEM_DOCUMENT:
                        content = html.get_content()
                        if func:
                            r = func(content)
                        else:
                            r = self.parse_html(content)
                        if r:
                            result.append(r)
        return result

    def save_data(self, data):
        """
        保存解析的数据（html 或 image）
        :param data:
        :return:
        """
        name = data.get_name()
        _save_path = self.save_path / data.get_name()
        if '/' in name:
            new_save_path = Path(Path(_save_path).parent)
            new_save_path.mkdir(exist_ok=True)
        with open(_save_path, 'wb') as f:
            f.write(data.get_content())

    def parse_html(self, html_content):
        """
        解析html
        :param html_content:
        :return:
        """
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.ignore_tables = True
        res = []
        r = h.handle(html_content.decode('utf-8'))
        for i in r.strip().split('\n'):
            if i.strip():
                res.append(i.strip())
        return res
