const path = require('path');

module.exports = {
    entry: {
        main: ['./src/js/generate_playlist.js', './src/js/spotify_auth.js'],
    },
    output: {
        filename: 'index.js',
        path: path.resolve(__dirname, ''),
    },
}
        