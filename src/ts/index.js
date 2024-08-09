"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var Papa = require("papaparse");
var fs = require("fs");
function csvToArray(csvData) {
    var parsedData = Papa.parse(csvData, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
    });
    if (parsedData.errors.length > 0) {
        console.error('Error parsing CSV:', parsedData.errors);
        return [];
    }
    return parsedData.data;
}
function combineAllPlaylists(playlistOwners, playlists) {
    var combinedPlaylist = playlists["df_".concat(playlistOwners[0].name)];
    for (var i = 1; i < playlistOwners.length; i++) {
        console.log("\nSearching ".concat(playlistOwners[i].name));
        combinedPlaylist = combineTwoPlaylists(combinedPlaylist, playlists["playlist_".concat(playlistOwners[i].name)]);
    }
    console.log('\nCombination successful');
    combinedPlaylist.sort(function (a, b) { return b.weight - a.weight; });
    console.log('\nSorted results');
    return combinedPlaylist;
}
function combineTwoPlaylists(playlist1, playlist2) {
    var _a;
    var length = playlist1.length;
    for (var j = 0; j < playlist2.length; j++) {
        var match = false;
        for (var i = 0; i < length; i++) {
            if (playlist1[i].track === playlist2[j].track) {
                if (playlist1[i].artist === playlist2[j].artist) {
                    match = true;
                    playlist1[i].weight += playlist2[j].weight + 50;
                    playlist1[i][Object.keys(playlist2[0])[3]] = playlist2[j][Object.keys(playlist2[0])[3]];
                    console.log([playlist2[j].track, playlist2[j].artist]);
                    console.log('match');
                    break;
                }
                console.log('track matched, artist didn\'t');
                console.log([playlist2[j].track, playlist2[j].artist, playlist1[i].artist]);
            }
        }
        if (!match) {
            var newTrack = (_a = {
                    track: playlist2[j].track,
                    artist: playlist2[j].artist,
                    weight: playlist2[j].weight
                },
                _a[Object.keys(playlist2[0])[3]] = playlist2[j][Object.keys(playlist2[0])[3]],
                _a);
            playlist1.push(newTrack);
            length++;
        }
    }
    return playlist1;
}
var csvData = fs.readFileSync('data/result/gaz.csv', 'utf8');
var dataArray = csvToArray(csvData);
console.log(dataArray);
