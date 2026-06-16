const express = require('express');
const router = express.Router();

// Import route modules
const authRoutes = require('./auth.routes');
const zoteroRoutes = require('./zoteroRoutes');
const spotifyRoutes = require('./spotifyRoutes');
// const userRoutes = require('./user.routes');
// const videoRoutes = require('./video.routes');
// const commentRoutes = require('./comment.routes');
// const soundRoutes = require('./sound.routes');
// const searchRoutes = require('./search.routes');

// API documentation endpoint
router.get('/docs', (req, res) => {
  res.json({
    message: 'K-Lab API Documentation',
    version: '1.0.0',
    endpoints: {
      auth: {
        register: 'POST /api/v1/auth/register',
        login: 'POST /api/v1/auth/login',
        logout: 'POST /api/v1/auth/logout',
        refresh: 'POST /api/v1/auth/refresh',
        verify: 'GET /api/v1/auth/verify',
      },
      users: {
        getProfile: 'GET /api/v1/users/:id',
        updateProfile: 'PUT /api/v1/users/:id',
        follow: 'POST /api/v1/users/:id/follow',
        unfollow: 'DELETE /api/v1/users/:id/follow',
        followers: 'GET /api/v1/users/:id/followers',
        following: 'GET /api/v1/users/:id/following',
      },
      videos: {
        upload: 'POST /api/v1/videos',
        getFeed: 'GET /api/v1/videos/feed',
        getVideo: 'GET /api/v1/videos/:id',
        updateVideo: 'PUT /api/v1/videos/:id',
        deleteVideo: 'DELETE /api/v1/videos/:id',
        like: 'POST /api/v1/videos/:id/like',
        unlike: 'DELETE /api/v1/videos/:id/like',
        trending: 'GET /api/v1/videos/trending',
      },
      comments: {
        create: 'POST /api/v1/videos/:videoId/comments',
        get: 'GET /api/v1/videos/:videoId/comments',
        update: 'PUT /api/v1/comments/:id',
        delete: 'DELETE /api/v1/comments/:id',
        like: 'POST /api/v1/comments/:id/like',
      },
      sounds: {
        upload: 'POST /api/v1/sounds',
        library: 'GET /api/v1/sounds/library',
        getSound: 'GET /api/v1/sounds/:id',
        use: 'POST /api/v1/sounds/:id/use',
        trending: 'GET /api/v1/sounds/trending',
      },
      search: {
        all: 'GET /api/v1/search?q=query',
        users: 'GET /api/v1/search/users?q=query',
        videos: 'GET /api/v1/search/videos?q=query',
        sounds: 'GET /api/v1/search/sounds?q=query',
        hashtags: 'GET /api/v1/search/hashtags?q=query',
      },
      zotero: {
        library: 'GET /api/v1/zotero/library',
        collections: 'GET /api/v1/zotero/collections',
        collectionItems: 'GET /api/v1/zotero/collections/:collectionId',
        search: 'GET /api/v1/zotero/search?q=query',
        status: 'GET /api/v1/zotero/status',
      },
      spotify: {
        token: 'POST /api/v1/spotify/token',
        refresh: 'POST /api/v1/spotify/refresh',
        me: 'GET /api/v1/spotify/me',
        recommendations: 'POST /api/v1/spotify/recommendations',
        playlist: 'POST /api/v1/spotify/playlist',
      },
    },
    features: {
      beatSync: 'AI-powered music synchronization',
      vocoder: 'Daft Punk-style voice effects',
      vibeModes: 'Pre-configured aesthetic packages',
      thePyramid: 'Fair discovery algorithm',
      soundLab: 'Mobile DAW features',
    },
  });
});

// Mount routes
router.use('/auth', authRoutes);
router.use('/zotero', zoteroRoutes);
router.use('/spotify', spotifyRoutes);
// router.use('/users', userRoutes);
// router.use('/videos', videoRoutes);
// router.use('/comments', commentRoutes);
// router.use('/sounds', soundRoutes);
// router.use('/search', searchRoutes);

// Temporary test endpoint
router.get('/test', (req, res) => {
  res.json({
    message: '🤖💙 K-Lab API is working!',
    tagline: 'Digital Love Edition',
    timestamp: new Date().toISOString(),
  });
});

module.exports = router;

// Made with Bob
