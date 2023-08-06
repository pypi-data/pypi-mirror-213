# -*- coding: UTF-8 -*-
# @Time : 2023/6/13 16:32 
# @Author : 刘洪波
def convert_format(ebook_input: str, ebook_output: str, timeout=60):
    from ebooksp.ebook_convert_format import ebook_convert_format
    return ebook_convert_format(ebook_input, ebook_output, timeout)


def convert_format_many(ebooks_input: list, ebooks_output: list, timeout=60):
    from ebooksp.ebook_convert_format import ebook_convert_format_many
    return ebook_convert_format_many(ebooks_input, ebooks_output, timeout)


def to_text(ebook_input: str, delete=True, timeout=60):
    from ebooksp.ebook_to_text import ebook_to_text
    return ebook_to_text(ebook_input, delete, timeout)
