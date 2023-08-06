#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
生成epub图书
@Project ：spider
@File    ：EpubSpliter.py
@Author  ：Pipiyi
@Date    ：23/5/23 14:43
"""
import os
from ebooklib import epub


class EpubSpliter:
    def __init__(self, title, author, identifier, language="zh-CN"):
        """
        Initialize an EpubSpliter object.
        :param title: Title of the book.
        :param author: Author of the book.
        :param identifier: Identifier of the book.
        :param language: Language of the book (default is 'zh-CN').
        """
        self.book = epub.EpubBook()
        self.book.set_title(title)
        self.book.set_identifier(identifier)
        self.book.add_author(author)
        self.book.set_language(language)
        self.epub_list = []
        self.title = title
        self.is_thumb = False

    def add_cover(self, filename, file_content):
        """
        Add a cover to the book.
        :param filename: The filename of the cover
        :param file_content: The content of the cover (binary format).
        """
        self.book.set_cover(filename, file_content)
        self.is_thumb = True

    def add_item(self, title, file_name, content):
        """
        Add a chapter to the book.
        :param title: The title of the chapter
        :param file_name: The filename of the chapter.
        :param content: The content of the chapter.
        :return:
        """
        chapter = epub.EpubHtml(title=title, file_name=f"{file_name}.xhtml", lang="zh-CN")
        chapter.set_content(content)
        self.book.add_item(chapter)
        self.epub_list.append(chapter)

    def save(self, file_path="", file_name=""):
        """
        Save the book to a file.
        :param file_path: The directory where the book should be saved (default is current directory).
        :param file_name: The name of the file (default is the book title).
        :return:
        """
        # self.book.toc = (epub.Link(chapter.file_name, chapter.title, f"chapter{key}") for key, chapter in
                         # enumerate(self.epub_list))
        self.book.toc = tuple(self.epub_list)
        self.book.spine = ["cover", "nav"] + self.epub_list if self.is_thumb else ["nav"] + self.epub_list

        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

        file_name = file_name if file_name else self.title
        output_path = os.path.join(file_path, f"{file_name}.epub")
        try:
            epub.write_epub(output_path, self.book)
        except Exception as e:
            raise Exception(e)
