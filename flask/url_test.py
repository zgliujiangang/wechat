# coding: utf-8

from werkzeug.urls import url_parse

if __name__ == '__main__':
    path = "/index?my=1"
    url = url_parse(path)
    print url
    print type(url)
    print dir(url)
    print url.query