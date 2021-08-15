# pylint: disable=C0114,C0116,R0201
import scrapy
from sportscrawler.football.items import LiveItem


class LiveSpider(scrapy.Spider):
    """
    Gets live match data
    """

    name = "football-live-info"
    allowed_domains = ["transfermarkt.co.uk"]

    def start_requests(self):
        return [
            scrapy.Request(
                url="https://www.transfermarkt.co.uk/ticker/index/live",
                callback=self.parse,
            )
        ]

    def parse(self, response):
        for competition in response.selector.xpath("//table[@class='livescore']"):
            for match in competition.xpath("tbody/tr"):
                if match.xpath("td[4]/a").xpath("@href").get():
                    yield LiveItem(
                        match_type=match.xpath("td[1]/text()").get().strip()
                        if match.xpath("td[1]/text()").get().strip()
                        else "Live",
                        match_code=match.xpath("td[4]/a")
                        .xpath("@href")
                        .get()
                        .split("/")[-1],
                        teams=[
                            {
                                "name": match.xpath("td[3]/a/text()").get(),
                                "code": match.xpath("td[3]/a/@href")
                                .get()
                                .split("/")[1],
                                "id": match.xpath("td[3]/a/@href").get().split("/")[-1],
                            },
                            {
                                "name": match.xpath("td[5]/a/text()").get(),
                                "code": match.xpath("td[5]/a/@href")
                                .get()
                                .split("/")[1],
                                "id": match.xpath("td[5]/a/@href").get().split("/")[-1],
                            },
                        ],
                        match_status=match.xpath("td[4]/a/span/text()").get(),
                    )
