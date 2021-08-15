# pylint: disable=C0114, C0116, R0201
import scrapy
from sportscrawler.football.items import TeamItem


class TeamSpider(scrapy.Spider):
    """
    Scrapy Spider to get club team details
    """

    name = "football-team-info"
    allowed_domains = ["transfermarkt.co.uk"]

    def start_requests(self):
        return [
            scrapy.Request(
                url="https://www.transfermarkt.co.uk/liverpool-fc/erfolge/verein/31",
                callback=self.parse,
            )
        ]

    def parse(self, response):
        titles_names = [
            "".join(championship.get().split("x")[1:]).strip()
            for championship in response.selector.xpath(
                "//div[@class='large-6 columns']/div/div[@class='header']/h2/text()"
            )
        ]
        titles = [
            {
                "Title": titles_names[i],
                "years": [
                    "".join(year.split()) for year in years.get().strip().split(" ")
                ],
            }
            for i, years in enumerate(
                response.selector.xpath(
                    "//div[@class='large-6 columns']/div/div/div[@class='erfolg_infotext_box']/text()"
                )
            )
        ]
        yield scrapy.Request(
            url=response.url.split("erfolge")[0]
            + "kadernachposition"
            + response.url.split("erfolge")[1],
            callback=self.parse_squad,
            cb_kwargs=dict(titles=titles),
        )

    def parse_squad(self, response, titles):
        squad_number = [
            num.get()
            for num in response.selector.xpath(
                "//td[contains(@class,'zentriert smallrueckennummer')]/div/text()"
            )
        ]
        positions = [
            position.get()
            for position in response.selector.xpath("//td[@class='pos_2']/text()")
        ]
        players = [
            {
                "name": player_data.xpath("a/text()").get(),
                "player_ids": {
                    "id": player_data.xpath("a/@href").get().split("/")[1],
                    "code": player_data.xpath("a/@href").get().split("/")[-1],
                },
                "injury_status": player_data.xpath("span/@title").get()
                if player_data.xpath("span/@title").get()
                and "captain" not in player_data.xpath("span/@title").get()
                else None,
                "squad_number": squad_number[i],
                "position": positions[i],
            }
            for i, player_data in enumerate(
                response.selector.xpath("//td[contains(@class,'hauptlink')]")
            )
        ]
        yield TeamItem(
            name=response.selector.xpath("//h1[@itemprop='name']/span/text()").get(),
            titles=titles,
            players=players,
        )
