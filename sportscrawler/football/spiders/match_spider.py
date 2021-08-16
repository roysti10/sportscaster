# pylint: disable=C0114,C0116,R0201
import scrapy
from sportscrawler.football.items import MatchItem


class MatchSpider(scrapy.Spider):
    """
    Gives complete information of a match
    """

    name = "football-match-info"
    allowed_domains = ["transfermarkt.co.uk"]
    start_urls = [
        "https://www.transfermarkt.co.uk/guatemala_mexico/index/spielbericht/3608536"
    ]

    def parse(self, response):
        match_info = {
            "match_schedule": (
                [
                    i.xpath("text()").get()
                    for i in response.selector.xpath(
                        "//p[@class='sb-datum hide-for-small']/node()"
                    )
                    if "datum" in i.get()
                ][0].strip()
                + " "
                + [
                    i.get()
                    for i in response.selector.xpath(
                        "//p[@class='sb-datum hide-for-small']/node()"
                    )[1:]
                    if ("<a" not in i.get() and "M" in i.get())
                ][0]
                .split("|")[1]
                .strip()
            ),
            "league": {
                "name": response.selector.xpath(
                    "//div[@class='spielername-profil']/h2/span/a/text()"
                ).get(),
                "id": response.selector.xpath(
                    "//div[@class='spielername-profil']/h2/span/a"
                )
                .xpath("@href")
                .get()
                .split("/")[1],
            },
            "stadium": response.selector.xpath(
                "//a[contains(@href,'stadion')]/text()"
            ).get(),
            "teams": [
                {
                    "name": team.xpath("a[2]/text()").get(),
                    "id": team.xpath("a[2]").xpath("@href").get().split("/")[1],
                }
                for team in response.selector.xpath(
                    "//div[contains(@class,'sb-team')]"
                )[0:2]
            ],
            "score": [
                score.get().strip() if "-" not in score.get() else "NYS"
                for score in response.selector.xpath(
                    "//div[@class='sb-endstand']/text()"
                )
            ][0],
        }
        if (
            "NYS" not in match_info["score"]
            and response.selector.xpath("//li[@id='line-ups']/a/@href").get()
        ):
            match_info["match_events"] = {"Substitutions": [], "Goals": [], "Cards": []}
            for event in response.selector.xpath(
                "//div[@class='row' and not(@id)]/div/div"
            )[3:]:
                if (
                    event.xpath("div[@class='header']/h2/text()").get().strip()
                    == "Goals"
                ):
                    match_info["match_events"]["Goals"] = [
                        {
                            "score": i.xpath("div/div[2]/b/text()").get(),
                            "player": i.xpath("div/div[4]/a/text()").get(),
                        }
                        for i in event.xpath("div[@class='sb-ereignisse']/ul/li")
                    ]
                elif (
                    event.xpath("div[@class='header']/h2/text()").get().strip()
                    == "Substitutions"
                ):
                    match_info["match_events"]["Substitutions"] = [
                        {
                            "out": i.xpath("div/div[4]/span[1]/a/text()").get(),
                            "in": i.xpath("div/div[4]/span[2]/a/text()").get(),
                        }
                        for i in event.xpath("div[@class='sb-ereignisse']/ul/li")
                    ]
                elif (
                    event.xpath("div[@class='header']/h2/text()").get().strip()
                    == "Cards"
                ):
                    match_info["match_events"]["Cards"] = [
                        {
                            "player": i.xpath("div/div[4]/a/text()").get(),
                            "card-info": i.xpath("div/div[4]/text()").get().strip(),
                        }
                        for i in event.xpath("div[@class='sb-ereignisse']/ul/li")
                    ]

            (
                match_info["teams"][0]["formation"],
                match_info["teams"][1]["formation"],
            ) = (
                response.selector.xpath(
                    "//div[@class='large-6 columns aufstellung-box']"
                )[0]
                .xpath("div[@class='row']/div/text()")[0]
                .get()
                .split(":")[1]
                .strip(),
                response.selector.xpath("//div[@class='large-6 columns']")[0]
                .xpath("div[@class='row']/div/text()")
                .get()
                .split(":")[1]
                .strip(),
            )
            yield scrapy.Request(
                url="https://www."
                + self.allowed_domains[0]
                + response.selector.xpath("//li[@id='line-ups']/a/@href").get(),
                callback=self.parse_lineup,
                cb_kwargs=dict(match_info=match_info),
            )
        else:
            yield MatchItem(match_info=match_info)

    def parse_lineup(self, response, match_info):
        table_map = {0: "lineups", 1: "substitutes"}
        for i, table in enumerate(response.selector.xpath("//table[@class='items']")):
            if int(i / 2) == 2:
                break
            match_info["teams"][i % 2][table_map[int(i / 2)]] = []
            for player in table.xpath("tr"):
                match_info["teams"][i % 2][table_map[int(i / 2)]].append(
                    {
                        "name": player.xpath("td[2]/table/tr[1]/td[2]/a/text()").get(),
                        "player_code": player.xpath("td[2]/table/tr[1]/td[2]/a")
                        .get()
                        .split("/")[1],
                        "player_id": player.xpath("td[2]/table/tr[1]/td[2]/a")
                        .get()
                        .split("/")[3],
                        "position": player.xpath("td[2]/table/tr[2]/td[1]/text()")
                        .get()
                        .split(",")[0]
                        .strip(),
                    }
                )
        yield MatchItem(match_info=match_info)
