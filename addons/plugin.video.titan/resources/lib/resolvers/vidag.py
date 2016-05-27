# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re,urllib
from resources.lib.libraries import client
from resources.lib.libraries import jsunpack


def resolve(url):
    try:
        headers = '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': url})

        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://vid.ag/embed-%s.html' % url

        result = client.request(url, mobile=True)

        result = re.compile('(eval.*?\)\)\))').findall(result)[-1]
        result = jsunpack.unpack(result)

        result = re.compile('sources *: *\[.+?\]').findall(result)[-1]
        result = re.compile('file *: *"(http.+?)"').findall(result)

        url = [i for i in result if '.m3u8' in i]
        if len(url) > 0: return url[0] + headers

        url = [i for i in result if not '.m3u8' in i]
        if len(url) > 0: return url[0] + headers
    except:
        return

