const express = require('express');
const router = express.Router();
const spotify = require('../services/spotifyService');

function getToken(req) {
  const auth = req.headers.authorization || '';
  if (auth.startsWith('Bearer ')) return auth.slice(7);
  return req.body?.accessToken || null;
}

router.post('/token', async (req, res) => {
  try {
    const { code, redirectUri, codeVerifier } = req.body;
    if (!code || !redirectUri || !codeVerifier) {
      return res.status(400).json({ error: 'code, redirectUri, and codeVerifier required' });
    }
    const tokens = await spotify.exchangeCode({ code, redirectUri, codeVerifier });
    res.json(tokens);
  } catch (err) {
    const status = err.response?.status || err.statusCode || 500;
    res.status(status).json({
      error: 'Token exchange failed',
      message: err.response?.data?.error_description || err.message,
    });
  }
});

router.post('/refresh', async (req, res) => {
  try {
    const { refreshToken } = req.body;
    if (!refreshToken) return res.status(400).json({ error: 'refreshToken required' });
    const tokens = await spotify.refreshToken(refreshToken);
    res.json(tokens);
  } catch (err) {
    const status = err.response?.status || 500;
    res.status(status).json({
      error: 'Refresh failed',
      message: err.response?.data?.error_description || err.message,
    });
  }
});

router.get('/me', async (req, res) => {
  try {
    const token = getToken(req);
    if (!token) return res.status(401).json({ error: 'Access token required' });
    const profile = await spotify.getProfile(token);
    res.json(profile);
  } catch (err) {
    const status = err.response?.status || 500;
    res.status(status).json({ error: err.response?.data?.error?.message || err.message });
  }
});

router.post('/recommendations', async (req, res) => {
  try {
    const token = getToken(req);
    if (!token) return res.status(401).json({ error: 'Access token required' });

    const mood = { ...req.body };
    delete mood.accessToken;

    if (req.body.useTopArtists) {
      const artistIds = await spotify.getTopArtists(token, 3);
      if (artistIds.length) mood.seed_artists = artistIds;
    }

    const data = await spotify.getRecommendations(token, mood);
    res.json(data);
  } catch (err) {
    const status = err.response?.status || 500;
    res.status(status).json({
      error: 'Recommendations failed',
      message: err.response?.data?.error?.message || err.message,
    });
  }
});

router.post('/playlist', async (req, res) => {
  try {
    const token = getToken(req);
    if (!token) return res.status(401).json({ error: 'Access token required' });

    const { name, description, trackUris, isPublic } = req.body;
    if (!name || !trackUris?.length) {
      return res.status(400).json({ error: 'name and trackUris required' });
    }

    const playlist = await spotify.createPlaylist(token, { name, description, trackUris, isPublic });
    res.json(playlist);
  } catch (err) {
    const status = err.response?.status || 500;
    res.status(status).json({
      error: 'Playlist creation failed',
      message: err.response?.data?.error?.message || err.message,
    });
  }
});

module.exports = router;