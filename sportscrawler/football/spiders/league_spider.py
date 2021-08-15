# pylint: disable=C0114, C0116, R0201
import scrapy
from sportscrawler.football.items import LeagueItem


class LeagueSpider(scrapy.Spider):
    """
    Fetches all the information from a league for the current season unless specified
    """

    name = "football-league-info"
    allowed_domains = ["transfermarkt.co.uk"]

    def start_requests(self):
        return [
            # scrapy.Request(
            #     url="https://www.transfermarkt.co.uk/laliga/startseite/wettbewerb/ES1/",
            #     callback=self.parse,
            # ),
            # scrapy.Request(
            #     url="https://www.transfermarkt.co.uk/1-bundesliga/startseite/wettbewerb/L1",
            #     callback=self.parse,
            # ),
            scrapy.Request(
                url="https://www.transfermarkt.co.uk/serie-a/startseite/wettbewerb/IT1",
                callback=self.parse,
            ),
            # scrapy.Request(
            #     url="https://www.transfermarkt.co.uk/ligue-1/startseite/wettbewerb/FR1/",
            #     callback=self.parse,
            # ),
            # scrapy.Request(
            #     url="https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1",
            #     callback=self.parse,
            # ),
        ]

    def parse(self, response):
        yield scrapy.Request(
            url="https://www."
            + self.allowed_domains[0]
            + response.selector.xpath("//a[@title='To complete table']")
            .xpath("@href")
            .get(),
            callback=self.parse_leaguetable,
        )

    def parse_leaguetable(self, response):
        table = response.selector.xpath(
            "//div[@class='responsive-table']/table/tbody/tr"
        )
        league_table = {}
        season = response.url.split("saison_id/")[-1]
        for club in table:
            league_table[club.xpath("td[1]/text()").get()] = {
                "team": {
                    "name": club.xpath("td[3]/a/text()").get(),
                    "id": club.xpath("td[3]/a").xpath("@href").get().split("/")[1],
                    "code": club.xpath("td[3]/a")
                    .xpath("@href")
                    .get()
                    .split("/saison")[0]
                    .split("/")[-1],
                },
                "Matches": club.xpath("td[4]/a/text()").get()
                if club.xpath("td[4]/a/text()")
                else club.xpath("td[4]/text()").get(),
                "Wins": club.xpath("td[5]/a/text()").get()
                if club.xpath("td[5]/a/text()")
                else club.xpath("td[5]/text()").get(),
                "Draws": club.xpath("td[6]/a/text()").get()
                if club.xpath("td[6]/a/text()")
                else club.xpath("td[6]/text()").get(),
                "Losses": club.xpath("td[7]/a/text()").get()
                if club.xpath("td[7]/a/text()")
                else club.xpath("td[7]/text()").get(),
                "Goals Scored/Conceded": club.xpath("td[8]/a/text()").get()
                if club.xpath("td[8]/a/text()")
                else club.xpath("td[8]/text()").get(),
                "Goal difference": club.xpath("td[9]/a/text()").get()
                if club.xpath("td[9]/a/text()")
                else club.xpath("td[9]/text()").get(),
                "Points": club.xpath("td[10]/a/text()").get()
                if club.xpath("td[10]/a/text()")
                else club.xpath("td[10]/text()").get(),
            }
        yield scrapy.Request(
            url=response.url.split("tabelle")[0]
            + "gesamtspielplan"
            + response.url.split("tabelle")[1],
            callback=self.parse_schedule,
            cb_kwargs=dict(season=season, league_table=league_table),
        )

    def parse_schedule(self, response, season, league_table):
        matchdays = response.selector.xpath("//div[@class='large-6 columns']")
        schedule = {}
        for matchday in matchdays:
            matches = matchday.xpath("div/table/tbody/tr[not(@class)]")
            schedule[matchday.xpath("div/div/text()").get()] = {}
            current_date = ""
            for match in matches:
                if match.xpath("td[1]/a/text()").get():
                    current_date = match.xpath("td[1]/a/text()").get()
                    schedule[matchday.xpath("div/div/text()").get()][current_date] = []
                if current_date == "":
                    continue
                schedule[matchday.xpath("div/div/text()").get()][current_date].append(
                    {
                        "team1": match.xpath("td[3]/a/text()").get(),
                        "team2": match.xpath("td[7]/a/text()").get(),
                        "score": "NYS"
                        if "-" in match.xpath("td[5]/a/text()").get()
                        else match.xpath("td[5]/a/text()").get(),
                        "match_code": match.xpath("td[5]/a")
                        .xpath("@href")
                        .get()
                        .split("/")[-1],
                    }
                )
        team_details = [league_table[club]["team"] for club in league_table]
        yield LeagueItem(
            season=season,
            league_leaders=league_table["1"]["team"]["name"]
            + "* susceptible to change if the season isn't over",
            teams=team_details,
            league_table=league_table,
            schedule=schedule,
        )
