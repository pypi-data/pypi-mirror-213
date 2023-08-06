# -*- coding: UTF-8 -*-
# @Time : 2023/6/9 16:48 
# @Author : 刘洪波


def to_html(file_path: str, save_path, overwrite=False):
    from epub_to_html import Epub2Html
    return Epub2Html(file_path, save_path, overwrite).convert()


def to_text(file_path: str, save_path, overwrite=False, func=None):
    from epub_to_text import Epub2Text
    return Epub2Text(file_path, save_path, overwrite).convert(func)
