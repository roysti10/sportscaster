const express = require('express');
const router = new express.Router();
const getJson = require('bent')('json');

const leagueMap = {
  'premier-league': 'GB1',
  'laliga': 'ES1',
  '1-bundesliga': 'L1',
  'serie-a': 'IT1',
  'ligue-1': 'FR1',
};

router.get('/:season/all', async (req, res) => {
  const response = await getJson(
      process.env.API_URL +
    'crawl.json?spider_name=football-league-info&' +
    'url=https://www.transfermarkt.co.uk/' +
    req.baseUrl.split('/football/')[1].split('/teams')[0] +
    '/startseite/wettbewerb/' +
    leagueMap[req.baseUrl.split('/football/')[1].split('/teams')[0]] +
    '/plus/?saison_id=' +
    req.params.season,
  );

  res.json({'teams': response.items[0].teams});
});

router.get('/:season/:teamId/:teamCode', async (req, res) => {
  const response = await getJson(
      process.env.API_URL +
    'crawl.json?spider_name=football-league-info&' +
    'url=https://www.transfermarkt.co.uk/' +
    req.baseUrl.split('/football/')[1].split('/teams')[0] +
    '/startseite/wettbewerb/' +
    leagueMap[req.baseUrl.split('/football/')[1].split('/teams')[0]] +
    '/plus/?saison_id=' +
    req.params.season,
  );
  let flag = 0;
  for (let i = 0; i < response.items[0].teams.length; i++) {
    if (req.params.teamId == response.items[0].teams[i]['id']) {
      flag = 1;
      break;
    }
  }
  if (flag == 0) {
    res.status(500);
    res.json('Team not in league');
  } else {
    const teamResponse = await getJson(
        process.env.API_URL +
      'crawl.json?spider_name=football-team-info&' +
      'url=https://www.transfermarkt.co.uk/' +
      req.params.teamId +
      '/erfolge/verein/' +
      req.params.teamCode,
    );
    const transferResponse = await getJson(
        process.env.API_URL +
      'crawl.json?spider_name=football-transfer-info&' +
       'url=https://www.transfermarkt.co.uk/' +
        req.baseUrl.split('/football/')[1].split('/teams')[0] +
        '/transfers/wettbewerb/' +
        leagueMap[req.baseUrl.split('/football/')[1].split('/teams')[0]],
    );
    teamResponse.items[0].transfers =
      transferResponse.items[0].transfers[req.params.teamId];
    res.json(teamResponse.items[0]);
  }
});

module.exports = router;
