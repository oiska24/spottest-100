"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var Papa = require("papaparse");
var fs = require("fs");
console.log(fs);
function csvToPlaylist(csvData) {
    var parsedData = Papa.parse(csvData, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
    });
    var playlist = {
        track: [],
        artist: [],
        weight: [],
    };
    if (parsedData.errors.length > 0) {
        console.error('Error parsing CSV:', parsedData.errors);
        return playlist;
    }
    parsedData.data.forEach(function (row) {
        playlist.track.push(row.track);
        playlist.artist.push(row.artist);
        playlist.weight.push(row.weight);
        // Handling additional columns dynamically
        Object.keys(row).forEach(function (key) {
            if (!['track', 'artist', 'weight'].includes(key)) {
                if (!playlist[key]) {
                    playlist[key] = [];
                }
                playlist[key].push(row[key]);
            }
        });
    });
    return playlist;
}
function getPlaylistNameFromPath(filePath) {
    var fileName = filePath.split('/').pop() || '';
    return fileName.split('.').shift() || 'UnnamedPlaylist';
}
function mergePlaylists(playlists) {
    var combinedList = [];
    Object.keys(playlists).forEach(function (playlistName) {
        var playlist = playlists[playlistName];
        playlist.track.forEach(function (track, index) {
            var artist = playlist.artist[index];
            var weight = playlist.weight[index];
            // Check if the track-artist combination already exists in the combined list
            var existingEntry = combinedList.find(function (entry) { return entry.track === track && entry.artist === artist; });
            if (existingEntry) {
                // If it exists, update the weight and the source index
                existingEntry.weight += weight;
                existingEntry.sources[playlistName] = index + 1; // +1 to adjust for 1-based index
            }
            else {
                // If it doesn't exist, create a new entry with nulls for all sources except the current one
                var newEntry = {
                    track: track,
                    artist: artist,
                    weight: weight,
                    sources: Object.keys(playlists).reduce(function (acc, key) {
                        acc[key] = key === playlistName ? index + 1 : null;
                        return acc;
                    }, {}),
                };
                combinedList.push(newEntry);
            }
        });
    });
    // Sort the combined list in descending order by weight
    combinedList.sort(function (a, b) { return b.weight - a.weight; });
    return combinedList;
}
function createCountdown(combinedList, countdownNumber) {
    // Trim the list to only include the top `countdownNumber` songs
    var trimmedList = combinedList.slice(0, countdownNumber);
    // Reverse the order of the tracks
    var reversedList = trimmedList.reverse();
    return reversedList;
}
// function generatePlaylist() {
//     alert("hi");
// }
// Ensure the function is accessible globally
// window.generatePlaylist = generatePlaylist;
function generatePlaylist() {
    var filePaths = [
        'data/website-data/ash.csv',
        'data/website-data/bee.csv',
        'data/website-data/billy.csv',
        'data/website-data/bryce.csv',
        'data/website-data/cam.csv',
        'data/website-data/eric.csv',
        'data/website-data/eve.csv',
        'data/website-data/gaz.csv',
        'data/website-data/han.csv',
        'data/website-data/jack.csv',
        'data/website-data/james.csv',
        'data/website-data/jim.csv',
        'data/website-data/jo.csv',
        'data/website-data/josh.csv',
        'data/website-data/kara.csv',
        'data/website-data/liana.csv',
        'data/website-data/loz.csv',
        'data/website-data/oscar.csv',
        'data/website-data/sam.csv',
        'data/website-data/sammy.csv'
    ];
    var playlists = {};
    var COUNTDOWN_NUMBER = 50;
    filePaths.forEach(function (filePath) {
        var csvData = fs.readFileSync(filePath, 'utf8');
        var playlistName = getPlaylistNameFromPath(filePath);
        playlists[playlistName] = csvToPlaylist(csvData);
    });
    console.log(playlists);
    var combinedList = mergePlaylists(playlists);
    var countdownList = createCountdown(combinedList, COUNTDOWN_NUMBER);
    console.log(countdownList);
    alert(countdownList[COUNTDOWN_NUMBER - 1].track);
}
// generatePlaylist();
