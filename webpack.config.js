const path = require('path');

module.exports = {
    entry: './src/js/generate_playlist.js',
    output: {
        filename: 'index.js',
        path: path.resolve(__dirname, ''),
    },
}
        