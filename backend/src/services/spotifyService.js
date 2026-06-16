const axios = require('axios');

const SPOTIFY_API = 'https://api.spotify.com/v1';
const SPOTIFY_ACCOUNTS = 'https://accounts.spotify.com/api/token';

function spotifyClient(accessToken) {
  return axios.create({
    baseURL: SPOTIFY_API,
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}

async function exchangeCode({ code, redirectUri, codeVerifier }) {
  const clientId = process.env.SPOTIFY_CLIENT_ID;
  const clientSecret = process.env.SPOTIFY_CLIENT_SECRET;

  if (!clientId) {
    throw Object.assign(new Error('SPOTIFY_CLIENT_ID not configured'), { statusCode: 500 });
  }

  const params = new URLSearchParams({
    grant_type: 'authorization_code',
    code,
    redirect_uri: redirectUri,
    client_id: clientId,
    code_verifier: codeVerifier,
  });

  const headers = { 'Content-Type': 'application/x-www-form-urlencoded' };
  if (clientSecret) {
    headers.Authorization = `Basic ${Buffer.from(`${clientId}:${clientSecret}`).toString('base64')}`;
  }

  const { data } = await axios.post(SPOTIFY_ACCOUNTS, params, { headers });
  return data;
}

async function refreshToken(refreshTokenValue) {
  const clientId = process.env.SPOTIFY_CLIENT_ID;
  const clientSecret = process.env.SPOTIFY_CLIENT_SECRET;

  const params = new URLSearchParams({
    grant_type: 'refresh_token',
    refresh_token: refreshTokenValue,
    client_id: clientId,
  });

  const headers = { 'Content-Type': 'application/x-www-form-urlencoded' };
  if (clientSecret) {
    headers.Authorization = `Basic ${Buffer.from(`${clientId}:${clientSecret}`).toString('base64')}`;
  }

  const { data } = await axios.post(SPOTIFY_ACCOUNTS, params, { headers });
  return data;
}

async function getRecommendations(accessToken, mood) {
  const client = spotifyClient(accessToken);
  const params = new URLSearchParams({
    limit: String(mood.limit || 20),
    market: mood.market || 'US',
  });

  const features = ['energy', 'valence', 'danceability', 'acousticness', 'tempo', 'instrumentalness'];
  features.forEach((key) => {
    if (mood[key] !== undefined && mood[key] !== null) {
      params.append(`target_${key}`, String(mood[key]));
    }
  });

  if (mood.min_energy !== undefined) params.append('min_energy', String(mood.min_energy));
  if (mood.max_energy !== undefined) params.append('max_energy', String(mood.max_energy));

  const seeds = [];
  if (mood.seed_genres?.length) seeds.push(...mood.seed_genres.slice(0, 5).map((g) => `seed_genres=${encodeURIComponent(g)}`));
  if (mood.seed_artists?.length) seeds.push(...mood.seed_artists.slice(0, 5).map((a) => `seed_artists=${encodeURIComponent(a)}`));
  if (mood.seed_tracks?.length) seeds.push(...mood.seed_tracks.slice(0, 5).map((t) => `seed_tracks=${encodeURIComponent(t)}`));

  if (!seeds.length) {
    params.append('seed_genres', 'electronic');
  } else {
    seeds.forEach((s) => {
      const [k, v] = s.split('=');
      params.append(k, decodeURIComponent(v));
    });
  }

  const { data } = await client.get(`/recommendations?${params}`);
  return data;
}

async function getTopArtists(accessToken, limit = 5) {
  const client = spotifyClient(accessToken);
  const { data } = await client.get('/me/top/artists', { params: { limit, time_range: 'medium_term' } });
  return data.items?.map((a) => a.id) || [];
}

async function createPlaylist(accessToken, { name, description, trackUris, isPublic = false }) {
  const client = spotifyClient(accessToken);
  const { data: user } = await client.get('/me');
  const { data: playlist } = await client.post(`/users/${user.id}/playlists`, {
    name,
    description,
    public: isPublic,
  });

  if (trackUris?.length) {
    await client.post(`/playlists/${playlist.id}/tracks`, { uris: trackUris.slice(0, 100) });
  }

  return playlist;
}

async function getProfile(accessToken) {
  const client = spotifyClient(accessToken);
  const { data } = await client.get('/me');
  return data;
}

module.exports = {
  exchangeCode,
  refreshToken,
  getRecommendations,
  getTopArtists,
  createPlaylist,
  getProfile,
};