# -*- coding: UTF-8 -*-
# @Time : 2022/8/11 15:25 
# @Author : 刘洪波

import ebooklib
from ebooklib import epub
from pathlib import Path
"""
将epub文件转换成html
"""


class Epub2Html(object):
    def __init__(self, file_path: str, save_path: str, overwrite=False):
        self.file_path = file_path
        self.save_path = Path(save_path)
        self.overwrite = overwrite  # True 重新生成， False不重新生成

    def convert(self):
        """
        将epub数据转换成 hmtl 与 image
        :return:
        """
        try:
            book = epub.read_epub(self.file_path)
            if book:
                if self.save_path.exists():
                    print(f'{str(self.save_path)} Directory already exists.')
                    if not self.overwrite:
                        return
                else:
                    self.save_path.mkdir(exist_ok=True)
                for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
                    self.save_data(image)
                for html in book.get_items():
                    if html.get_type() == ebooklib.ITEM_DOCUMENT:
                        self.save_data(html)
        except Exception as e:
            print(e)

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


