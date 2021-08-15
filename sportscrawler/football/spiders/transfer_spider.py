# pylint: disable=C0114, C0116, R0201
import scrapy
from sportscrawler.football.items import TransferItem


class TransferSpider(scrapy.Spider):
    """
    Fetches all the transfers done in the season
    """

    name = "football-transfer-info"
    allowed_domains = ["transfermarkt.co.uk"]

    def start_requests(self):
        return [
            scrapy.Request(
                url="https://www.transfermarkt.co.uk/premier-league/transfers/wettbewerb/GB1",
                callback=self.parse,
            )
        ]

    def parse(self, response):
        clubs = response.selector.xpath(
            "//div[@class='large-8 columns']/div[@class='box']"
        )[2:]
        transfers = {}
        for club in clubs:
            transfers[club.xpath("div[1]/h2/a").xpath("@href").get().split("/")[1]] = {
                "In": [],
                "Out": [],
            }
            for transfer in club.xpath("div[2]/table/tbody/tr"):
                transfers[club.xpath("div[1]/h2/a").xpath("@href").get().split("/")[1]][
                    "In"
                ].append(
                    {
                        "name": transfer.xpath("td[1]/div/span/a/text()").get(),
                        "Position": transfer.xpath("td[4]/text()").get(),
                        "From": transfer.xpath("td[8]/a/text()").get(),
                        "Fee": transfer.xpath("td[9]/a/text()").get(),
                    }
                )
            for transfer in club.xpath("div[4]/table/tbody/tr"):
                transfers[club.xpath("div[1]/h2/a").xpath("@href").get().split("/")[1]][
                    "Out"
                ].append(
                    {
                        "name": transfer.xpath("td[1]/div/span/a/text()").get(),
                        "Position": transfer.xpath("td[4]/text()").get(),
                        "To": transfer.xpath("td[8]/a/text()").get(),
                        "Fee": transfer.xpath("td[9]/a/text()").get(),
                    }
                )
        yield TransferItem(transfers=transfers)
