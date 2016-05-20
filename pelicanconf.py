#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'\u674e\u4fca\u4f1f'
SITENAME = u'\u674e\u4fca\u4f1f\u002d\u968f\u7b14'
SITEURL = 'http://lijunwei.github.io/'
DEFAULT_DATE_FORMAT = ('%Y-%m-%d')

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'zh'

THEME = 'tuxlite_tbs'

FEED_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'

ARTICLE_URL = 'pages/{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
ARTICLE_SAVE_AS = 'pages/{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
GITHUB_URL = 'https://github.com/LiJunWei/'
ARCHIVES_URL = 'archives.html'
#AUTHOR_BIO = '专注Python开发，DevOps'
GOOGLE_ANALYTICS = 'UA-71907220-1'
# Blogroll
LINKS =  (('Python', 'http://python.org/'),)
SOCIAL = (('GitHub', 'https://github.com/LiJunWei/'),
	  ('微博', 'http://weibo.com/p/1005053201246451/home'),)

DEFAULT_PAGINATION = 5
MENUITEMS = (('About','/pages/About.html'),)
DISQUS_SITENAME = True
# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
