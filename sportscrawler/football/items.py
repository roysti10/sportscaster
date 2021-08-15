# pylint: disable=C0114
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LeagueItem(scrapy.Item):
    """
    Item for League Details
    """

    season = scrapy.Field()
    league_leaders = scrapy.Field()
    teams = scrapy.Field()
    league_table = scrapy.Field()
    schedule = scrapy.Field()


class LiveItem(scrapy.Item):
    """
    Item for live spider
    """

    match_type = scrapy.Field()
    match_code = scrapy.Field()
    teams = scrapy.Field()
    match_status = scrapy.Field()


class MatchItem(scrapy.Item):
    """
    Item for match spider
    """

    match_info = scrapy.Field()


class PlayerItem(scrapy.Item):
    """
    Item for player spider
    """

    name = scrapy.Field()
    dob = scrapy.Field()
    Height = scrapy.Field()
    Country = scrapy.Field()
    Position = scrapy.Field()
    Foot = scrapy.Field()
    Club = scrapy.Field()
    Contract_expiry = scrapy.Field()
    Market_Value = scrapy.Field()
    Transfers = scrapy.Field()
    Titles = scrapy.Field()
    Career = scrapy.Field()


class TeamItem(scrapy.Item):
    """
    Item for team spider
    """

    name = scrapy.Field()
    titles = scrapy.Field()
    players = scrapy.Field()


class TransferItem(scrapy.Item):
    """
    Item for transfer spider
    """

    transfers = scrapy.Field()
