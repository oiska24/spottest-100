import * as Papa from 'papaparse';
import * as fs from 'fs';

interface Playlist {
    track: string[];
    artist: string[];
    weight: number[];
    [key: string]: any[];
}

function csvToPlaylist(csvData: string): Playlist {
    const parsedData = Papa.parse<Record<string, string | number>>(csvData, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
    });

    const playlist: Playlist = {
        track: [],
        artist: [],
        weight: [],
    };

    if (parsedData.errors.length > 0) {
        console.error('Error parsing CSV:', parsedData.errors);
        return playlist;
    }

    parsedData.data.forEach(row => {
        playlist.track.push(row.track as string);
        playlist.artist.push(row.artist as string);
        playlist.weight.push(row.weight as number);

        // Handling additional columns dynamically
        Object.keys(row).forEach(key => {
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

function getPlaylistNameFromPath(filePath: string): string {
    const fileName = filePath.split('/').pop() || '';
    return fileName.split('.').shift() || 'UnnamedPlaylist';
}

interface CombinedPlaylist {
    track: string;
    artist: string;
    weight: number;
    sources: { [key: string]: number | null };
}

function mergePlaylists(playlists: { [key: string]: Playlist }): CombinedPlaylist[] {
    const combinedList: CombinedPlaylist[] = [];

    Object.keys(playlists).forEach(playlistName => {
        const playlist = playlists[playlistName];

        playlist.track.forEach((track, index) => {
            const artist = playlist.artist[index];
            const weight = playlist.weight[index];

            // Check if the track-artist combination already exists in the combined list
            const existingEntry = combinedList.find(
                entry => entry.track === track && entry.artist === artist
            );

            if (existingEntry) {
                // If it exists, update the weight and the source index
                existingEntry.weight += weight;
                existingEntry.sources[playlistName] = index + 1; // +1 to adjust for 1-based index
            } else {
                // If it doesn't exist, create a new entry with nulls for all sources except the current one
                const newEntry: CombinedPlaylist = {
                    track,
                    artist,
                    weight,
                    sources: Object.keys(playlists).reduce((acc, key) => {
                        acc[key] = key === playlistName ? index + 1 : null;
                        return acc;
                    }, {} as { [key: string]: number | null }),
                };
                combinedList.push(newEntry);
            }
        });
    });

    // Sort the combined list in descending order by weight
    combinedList.sort((a, b) => b.weight - a.weight);

    return combinedList;
}

function createCountdown(combinedList: CombinedPlaylist[], countdownNumber: number): CombinedPlaylist[] {
    // Trim the list to only include the top `countdownNumber` songs
    const trimmedList = combinedList.slice(0, countdownNumber);

    // Reverse the order of the tracks
    const reversedList = trimmedList.reverse();

    return reversedList;
}

// function generatePlaylist() {
//     alert("hi");
// }


// Ensure the function is accessible globally
// window.generatePlaylist = generatePlaylist;


function generatePlaylist() {
    const filePaths = [
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

    const playlists: { [key: string]: Playlist } = {};

    const COUNTDOWN_NUMBER = 50;

    filePaths.forEach(filePath => {
        const csvData = fs.readFileSync(filePath, 'utf8');
        const playlistName = getPlaylistNameFromPath(filePath);
        playlists[playlistName] = csvToPlaylist(csvData);
    });

    console.log(playlists);

    const combinedList = mergePlaylists(playlists);
    const countdownList = createCountdown(combinedList, COUNTDOWN_NUMBER);
    console.log(countdownList);
    alert(countdownList[COUNTDOWN_NUMBER - 1].track)
}
// generatePlaylist();