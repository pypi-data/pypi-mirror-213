# -*- coding: UTF-8 -*-
# @Time : 2023/6/13 16:39 
# @Author : 刘洪波

import subprocess


def check_type(ebook_path: str):
    type_list = ['epub', 'mobi', 'azw3', 'azw']
    if isinstance(ebook_path, str):
        tag = False
        for t in type_list:
            if ebook_path.endswith('.' + t):
                tag = True
                break
        if not tag:
            raise ValueError(f'the formats supported by e-books include {type_list}')
    else:
        raise ValueError(f'ebook need require a str, not a {type(ebook_path)}')


def ebook_convert_format(ebook_input: str, ebook_output: str, timeout=60):
    """
    电子书格式转换
    :param ebook_input:  输入待转换的电子书路径
    :param ebook_output: 输出转换后的电子书路径
    :param timeout: 转换超时
    :return:
    """
    url = 'https://calibre-ebook.com/download'
    check_type(ebook_input)
    check_type(ebook_output)
    try:
        command = ['ebook-convert', ebook_input, ebook_output]
        ret = subprocess.run(command, timeout=timeout)
        if ret.returncode == 0:
            print(f"success: {ebook_input} to {ebook_output}")
        else:
            print(f"error: {ebook_input} to {ebook_output}")
    except Exception as e:
        if "No such file or directory: 'ebook-convert'" in str(e):
            raise EnvironmentError(f'Please install calibre first, url is {url}')
        else:
            raise


def ebook_convert_format_many(ebooks_input: list, ebooks_output: list, timeout=60):
    """
    电子书格式转换（批量转换）
    :param ebooks_input:  输入待转换的电子书路径列表
    :param ebooks_output: 输出转换后的电子书路径列表
    :param timeout: 转换超时
    :return:
    """
    if (not isinstance(ebooks_input, list)) or (not isinstance(ebooks_input, list)):
        raise ValueError(f'ebooks_input or ebooks_output need require a list')
    for i, o in zip(ebooks_input, ebooks_output):
        ebook_convert_format(i, o, timeout)
