const express = require('express');
const router = new express.Router();
const getJson = require('bent')('json');
const team = require('./team');

router.get('/', (req, res) => {
  res.status(400);
  res.json('Bad Request!');
});

const leagueMap = {
  'premier-league': 'GB1',
  'laliga': 'ES1',
  '1-bundesliga': 'L1',
  'serie-a': 'IT1',
  'ligue-1': 'FR1',
};

router.use('/teams', team);

router.get('/table/:season', async (req, res) => {
  const response = await getJson(
      process.env.API_URL +
    'crawl.json?spider_name=football-league-info&' +
    'url=https://www.transfermarkt.co.uk/' +
    req.baseUrl.split('/football/')[1] +
    '/startseite/wettbewerb/' +
    leagueMap[req.baseUrl.split('/football/')[1]] +
    '/plus/?saison_id=' +
    req.params.season,
  );

  res.json({
    'league_leaders': response.items[0].league_leaders,
    'league_table': response.items[0].league_table,
  });
});

router.get('/match-schedule/:season', async (req, res) => {
  const response = await getJson(
      process.env.API_URL +
    'crawl.json?spider_name=football-league-info&' +
    'url=https://www.transfermarkt.co.uk/' +
    req.baseUrl.split('/football/')[1] +
    '/startseite/wettbewerb/' +
    leagueMap[req.baseUrl.split('/football/')[1]] +
    '/plus/?saison_id=' +
    req.params.season,
  );

  res.json(response.items[0].schedule);
});

router.get('/transfers/:season', async (req, res) => {
  const response = await getJson(
      process.env.API_URL +
    'crawl.json?spider_name=football-transfer-info&' +
       'url=https://www.transfermarkt.co.uk/' +
        req.baseUrl.split('/football/')[1] +
        '/transfers/wettbewerb/' +
        leagueMap[req.baseUrl.split('/football/')[1]],
  );
  res.json(response.items[0].transfers);
});
module.exports = router;
