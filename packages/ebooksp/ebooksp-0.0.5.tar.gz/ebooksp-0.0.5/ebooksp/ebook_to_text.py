# -*- coding: UTF-8 -*-
# @Time : 2023/6/13 18:00 
# @Author : 刘洪波
import subprocess
import epubs
from ebooksp.ebook_convert_format import ebook_convert_format


def ebook_to_text(ebook_input: str, delete=True, timeout=60, func=None):
    """
    电子书转文本
    转换过程中会自动生成电子书的epub版本，路径和原电子书路径相同
    :param ebook_input: 电子书路径
    :param delete: 是否删除电子书的epub版本，
    :param timeout: 超时
    :param func: 解析html的函数，默认使用自有函数
    :return:
    """
    epub_book = ebook_input
    if not ebook_input.endswith('.epub'):
        type_list = ['mobi', 'azw3', 'azw']
        for t in type_list:
            tt = '.' + t
            if ebook_input.endswith(tt):
                epub_book = ebook_input.split(tt)[0] + '.epub'
        ebook_convert_format(ebook_input, epub_book, timeout)
    res = epubs.to_text(epub_book, func=func)
    if delete:
        delete_epub(epub_book, timeout)
    return res


def delete_epub(epub_path: str, timeout=60):
    """删除epub book"""
    command = ['rm', epub_path]
    ret = subprocess.run(command, timeout=timeout)
    if ret.returncode == 0:
        print(f"success: delete {epub_path}")
    else:
        print(f"error: delete {epub_path}")

