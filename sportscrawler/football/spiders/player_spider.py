# pylint: disable=C0114,C0116,R0201
import scrapy
from sportscrawler.football.items import PlayerItem


class PlayerSpider(scrapy.Spider):
    """
    Lists complete player info
    """

    name = "football-player-info"
    allowed_domains = ["transfermarkt.co.uk"]

    def start_requests(self):
        return [
            scrapy.Request(
                url="https://www.transfermarkt.co.uk/robert-lewandowski/profil/spieler/38253",
                callback=self.parse,
            )
        ]

    def parse(self, response):
        player_info = {
            "dob": response.selector.xpath("//table[@class='auflistung']")[0]
            .xpath("tr[1]/td[1]/a/text()")
            .get()
            .strip(),
            "Height": response.selector.xpath("//table[@class='auflistung']")[0]
            .xpath("tr[4]/td[1]/text()")
            .get()
            .strip(),
            "Country": response.selector.xpath("//table[@class='auflistung']")[0]
            .xpath("tr[5]/td[1]")
            .get()
            .split('flaggenrahmen">')[-1]
            .split("</td>")[0]
            .strip(),
            "Position": response.selector.xpath("//table[@class='auflistung']")[0]
            .xpath("tr[6]/td[1]/text()")
            .get()
            .strip(),
            "Foot": response.selector.xpath("//table[@class='auflistung']")[0]
            .xpath("tr[7]/td[1]/text()")
            .get()
            .strip(),
            "Club": response.selector.xpath("//table[@class='auflistung']")[0]
            .xpath("tr[9]/td[1]/a/text()")
            .get()
            .strip(),
            "Contract Expiry": response.selector.xpath("//table[@class='auflistung']")[
                0
            ]
            .xpath("tr[11]/td[1]/text()")
            .get()
            .strip(),
            "Market Value": response.selector.xpath(
                "//div[@class='large-5 columns small-12']/div/div/div[@class='right-td']/text()"
            )
            .get()
            .strip(),
            "Transfer_news": [],
        }
        for transfer in response.selector.xpath("//tr[@class='zeile-transfer']"):
            player_info["Transfer_news"].append(
                {
                    "Season": transfer.xpath("td[1]/text()").get(),
                    "Date": transfer.xpath("td[2]/text()").get(),
                    "Transfer_from": transfer.xpath("td[5]/a/text()").get(),
                    "Transfer_to": transfer.xpath("td[8]/a/text()").get(),
                    "Market_Value": transfer.xpath("td[9]/text()").get(),
                    "Fee": transfer.xpath("td[10]/text()").get(),
                }
            )
        yield scrapy.Request(
            url="https://www."
            + self.allowed_domains[0]
            + response.url.split(self.allowed_domains[0])[-1].split("/profil")[0]
            + "/erfolge"
            + response.url.split(self.allowed_domains[0])[-1].split("/profil")[-1],
            callback=self.parse_titles,
            cb_kwargs=dict(player_info=player_info),
        )

    def parse_titles(self, response, player_info):
        titles_names = [
            "".join(championship.get().split("x")[1:]).strip()
            for championship in response.selector.xpath(
                "//div[@class='large-6 columns']/div/div[@class='subkategorie-header']/span/text()"
            )
        ]
        player_info["titles"] = [
            {
                "Title": titles_names[i],
                "Team and Year": [
                    [
                        title_info.xpath("td[3]/a/text()").get(),
                        title_info.xpath("td[1]/text()").get(),
                    ]
                    for title_info in title.xpath("tr")
                ],
            }
            for i, title in enumerate(
                response.selector.xpath(
                    "//div[@class='large-6 columns']/div/div[not(@class)]/\
                            div[@class='erfolg_info_box']/table"
                )
            )
        ]
        yield scrapy.Request(
            url="https://www."
            + self.allowed_domains[0]
            + response.url.split(self.allowed_domains[0])[-1].split("/erfolge")[0]
            + "/leistungsdatenverein"
            + response.url.split(self.allowed_domains[0])[-1].split("/erfolge")[-1],
            callback=self.parse_career,
            cb_kwargs=dict(player_info=player_info),
        )

    def parse_career(self, response, player_info):
        player_info["career"] = {}
        player_info["career"]["club_stats"] = {}
        leagues = response.selector.xpath("//div[@class='table-header']/text()")
        for i, league in enumerate(
            response.selector.xpath("//table[not(@class)]")[:-1]
        ):
            player_info["career"]["club_stats"][leagues[2 * i + 1].get().strip()] = {}
            for stat in league.xpath("tbody/tr"):
                player_info["career"]["club_stats"][leagues[2 * i + 1].get().strip()][
                    stat.xpath("td[2]/a/text()").get()
                ] = {}
                player_info["career"]["club_stats"][leagues[2 * i + 1].get().strip()][
                    stat.xpath("td[2]/a/text()").get()
                ]["Matches"] = stat.xpath("td[3]/text()").get()
                player_info["career"]["club_stats"][leagues[2 * i + 1].get().strip()][
                    stat.xpath("td[2]/a/text()").get()
                ]["Goals"] = stat.xpath("td[4]/text()").get()
                player_info["career"]["club_stats"][leagues[2 * i + 1].get().strip()][
                    stat.xpath("td[2]/a/text()").get()
                ]["Assists"] = stat.xpath("td[5]/text()").get()
                player_info["career"]["club_stats"][leagues[2 * i + 1].get().strip()][
                    stat.xpath("td[2]/a/text()").get()
                ]["Yellows"] = stat.xpath("td[6]/text()").get()
                player_info["career"]["club_stats"][leagues[2 * i + 1].get().strip()][
                    stat.xpath("td[2]/a/text()").get()
                ]["Second Yellows"] = stat.xpath("td[7]/text()").get()
                player_info["career"]["club_stats"][leagues[2 * i + 1].get().strip()][
                    stat.xpath("td[2]/a/text()").get()
                ]["Reds"] = stat.xpath("td[8]/text()").get()
                player_info["career"]["club_stats"][leagues[2 * i + 1].get().strip()][
                    stat.xpath("td[2]/a/text()").get()
                ]["Minutes_played"] = stat.xpath("td[9]/text()").get()
        yield scrapy.Request(
            url="https://www."
            + self.allowed_domains[0]
            + response.url.split(self.allowed_domains[0])[-1].split(
                "/leistungsdatenverein"
            )[0]
            + "/nationalmannschaft"
            + response.url.split(self.allowed_domains[0])[-1].split(
                "/leistungsdatenverein"
            )[-1],
            callback=self.parse_nationalcareer,
            cb_kwargs=dict(player_info=player_info),
        )

    def parse_nationalcareer(self, response, player_info):
        player_info["career"]["national_stats"] = {}
        for stat in response.selector.xpath("//table[@class='items']/tbody/tr"):
            player_info["career"]["national_stats"][
                stat.xpath("td[2]/a/text()").get()
            ] = {}
            player_info["career"]["national_stats"][stat.xpath("td[2]/a/text()").get()][
                "Matches"
            ] = stat.xpath("td[3]/a/text()").get()
            player_info["career"]["national_stats"][stat.xpath("td[2]/a/text()").get()][
                "Goals"
            ] = stat.xpath("td[4]/a/text()").get()
            player_info["career"]["national_stats"][stat.xpath("td[2]/a/text()").get()][
                "Assists"
            ] = stat.xpath("td[5]/text()").get()
            player_info["career"]["national_stats"][stat.xpath("td[2]/a/text()").get()][
                "Yellows"
            ] = stat.xpath("td[6]/text()").get()
            player_info["career"]["national_stats"][stat.xpath("td[2]/a/text()").get()][
                "Second Yellows"
            ] = stat.xpath("td[7]/text()").get()
            player_info["career"]["national_stats"][stat.xpath("td[2]/a/text()").get()][
                "Reds"
            ] = stat.xpath("td[8]/text()").get()
        player_info["career"]["national_stats"]["teams_played_for"] = []
        skip_flag = 0
        for team in response.selector.xpath("//table[not(@class)]")[0].xpath(
            "tbody/tr"
        )[1:]:
            if skip_flag:
                skip_flag = 0
                continue
            player_info["career"]["national_stats"]["teams_played_for"].append(
                team.xpath("td[3]/a/text()").get()
            )
            skip_flag = 1

        yield PlayerItem(
            name=response.selector.xpath("//h1[@itemprop='name']/text()")
            .get()
            .split('"')[0]
            .split('"')[0]
            .strip()
            + " "
            + response.selector.xpath("//h1[@itemprop='name']/b/text()").get(),
            dob=player_info["dob"],
            Height=player_info["Height"],
            Country=player_info["Country"],
            Position=player_info["Position"],
            Foot=player_info["Foot"],
            Club=player_info["Club"],
            Contract_expiry=player_info["Contract Expiry"],
            Market_Value=player_info["Market Value"],
            Transfers=player_info["Transfer_news"],
            Titles=player_info["titles"],
            Career=player_info["career"],
        )
