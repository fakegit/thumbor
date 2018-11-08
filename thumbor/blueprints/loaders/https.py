#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from thumbor.blueprints.loaders.http import Loader as HttpLoader


class Loader(HttpLoader):
    def __normalize_url(self, url):
        url = self.__quote_url(url)

        return url if url.startswith("http") else "https://%s" % url


HTTPS_LOADER = Loader()
