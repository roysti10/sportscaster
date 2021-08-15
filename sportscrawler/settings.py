"""
Scrapy settings for espncricinfo project
For simplicity, this file contains only settings considered important or
commonly used. You can find more settings consulting the documentation:
https://docs.scrapy.org/en/latest/topics/settings.html
https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
https://docs.scrapy.org/en/latest/topics/spider-middleware.html
"""

BOT_NAME = "sportscaster"

SPIDER_MODULES = ["sportscrawler.football.spiders"]

USER_AGENT = "sportscaster"
# Obey robos.txt rules
ROBOTSTXT_OBEY = True

# Enable and configure HTTP caching (disabled by default
HTTPCACHE_ENABLED = False
