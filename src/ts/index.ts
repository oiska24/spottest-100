import * as Papa from 'papaparse';
import * as fs from 'fs';

interface Playlist {
    track: string;
    artist: string;
    weight: number;
    [key: string]: any;
}

interface PlaylistOwners {
    name: string;
    [key: string]: any;
}

function csvToArray(csvData: string): Playlist[] {
    const parsedData = Papa.parse<Playlist>(csvData, {
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

function combineAllPlaylists(playlistOwners: PlaylistOwners[], playlists: { [key: string]: Playlist[] }): Playlist[] {
    let combinedPlaylist: Playlist[] = playlists[`df_${playlistOwners[0].name}`];

    for (let i = 1; i < playlistOwners.length; i++) {
        console.log(`\nSearching ${playlistOwners[i].name}`);
        combinedPlaylist = combineTwoPlaylists(combinedPlaylist, playlists[`playlist_${playlistOwners[i].name}`]);
    }

    console.log('\nCombination successful');
    combinedPlaylist.sort((a, b) => b.weight - a.weight);
    console.log('\nSorted results');

    return combinedPlaylist;
}

function combineTwoPlaylists(playlist1: Playlist[], playlist2: Playlist[]): Playlist[] {
    let length = playlist1.length;

    for (let j = 0; j < playlist2.length; j++) {
        let match = false;

        for (let i = 0; i < length; i++) {
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
            const newTrack: Playlist = {
                track: playlist2[j].track,
                artist: playlist2[j].artist,
                weight: playlist2[j].weight,
                [Object.keys(playlist2[0])[3]]: playlist2[j][Object.keys(playlist2[0])[3]],
            };
            playlist1.push(newTrack);
            length++;
        }
    }

    return playlist1;
}

const csvData = fs.readFileSync('data/result/gaz.csv', 'utf8');
const dataArray = csvToArray(csvData);
console.log(dataArray);