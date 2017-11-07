# -*- coding: utf-8 -*-

# Scrapy settings for lianjia project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'lianjia'

SPIDER_MODULES = ['lianjia.spiders']
NEWSPIDER_MODULE = 'lianjia.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'lianjia (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

LOG_FILE = "scrapy.log"
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
   'Cookies':'lianjia_uuid=095b47d2-4dda-4696-82ea-71c1ca27ff27; UM_distinctid=15f7a523eb9121-0f879e850b9996-c303767-190140-15f7a523eba9e8; lianjia_token=2.007ad3034c036df9896b7e2a7dd18d8493; _jzqckmp=1; cityCode=sh; select_city=110000; all-lj=eae2e4b99b3cdec6662e8d55df89179a; _ga=GA1.2.2014829107.1508225585; _gid=GA1.2.343263446.1509585734; _jzqy=1.1508225583.1509760646.4.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6.jzqsr=baidu; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1509585731,1509624252,1509708038,1509760624; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1509763063; _smt_uid=59e5b22e.3c65172a; CNZZDATA1253477573=1778571283-1509619331-https%253A%252F%252Fnj.lianjia.com%252F%7C1509758639; CNZZDATA1254525948=384226554-1509621195-https%253A%252F%252Fnj.lianjia.com%252F%7C1509759553; _jzqa=1.2430296763589702700.1508225583.1509760646.1509763064.11; _jzqc=1; _jzqx=1.1509602015.1509763064.4.jzqsr=nj%2Elianjia%2Ecom|jzqct=/.jzqsr=bj%2Elianjia%2Ecom|jzqct=/chengjiao/; CNZZDATA1255633284=419018917-1509622304-https%253A%252F%252Fnj.lianjia.com%252F%7C1509763033; CNZZDATA1255604082=1524619808-1509619261-https%253A%252F%252Fnj.lianjia.com%252F%7C1509760296; _jzqb=1.1.10.1509763064.1; _qzja=1.1803723519.1509624272584.1509760646097.1509763063780.1509760646097.1509763063780.0.0.0.118.6; _qzjb=1.1509763063780.1.0.0.0; _qzjc=1; _qzjto=2.2.0; lianjia_ssid=bbf1859d-2da2-4947-9bb5-a6c0b35e5a78',

}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'lianjia.middlewares.LianjiaSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'lianjia.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'lianjia.pipelines.LianjiaPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
