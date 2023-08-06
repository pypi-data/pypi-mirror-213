# ebook

## 介绍
处理电子书的工具

## 安装


    pip install ebooksp

## 功能
- 支持电子书互相转格式
- 支持将电子书转成文本

## 支持的电子书格式

- epub
- mobi
- azw3
- azw

## 使用
### 转换格式



     import ebooksp
     ebooksp.convert_format('xxx.mobi', 'xxx.epub')



### 转换格式(批量转换)



     import ebooksp
     ebooksp.convert_format_many(['xxx.mobi', 'yyy.epub'], ['xxx.epub', 'yyy.azw3'])


### 电子书转成文本



     import ebooksp
     text = ebooksp.to_text('xxx.mobi')
     print(text)