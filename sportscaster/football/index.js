const express = require('express');
const router = new express.Router();
const getJson = require('bent')('json');
const league = require('./league');


router.get(['/', '/match-info'], (req, res) =>{
  res.status(400);
  res.send('Bad Request!');
});

router.use(['/premier-league',
  '/laliga',
  '/1-bundesliga',
  '/ligue-1',
  '/serie-a',
], league);

router.get('/live-matches', async (req, res)=>{
  const response = await getJson(
      process.env.API_URL +
    'crawl.json?spider_name=football-live-info&start_requests=true',
  );
  res.send(response.items);
});

router.get('/match-info/:match_code', async (req, res) => {
  const response = await getJson(
      process.env.API_URL +
    'crawl.json?spider_name=football-match-info&' +
      'url=https://www.transfermarkt.co.uk/spielbericht/index/spielbericht/' +
    req.params.match_code,
  );
  res.send(response.items[0].match_info);
});

router.get('/player/:playerID/:playerCode', async (req, res)=>{
  const response = await getJson(
      process.env.API_URL +
    'crawl.json?spider_name=football-player-info&' +
    'url=https://www.transfermarkt.co.uk/'+
    req.params.playerID +
    '/profil/spieler/'+
    req.params.playerCode,
  );
  res.send(response.items[0]);
});
module.exports = router;
