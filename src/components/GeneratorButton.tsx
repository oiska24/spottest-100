// interface Generation {
//     color: string;
//     onClick: () => void;
// }

// const GeneratorButton = ({color, onClick}: Generation) => {
//     return (
//         <button type="button" className={"btn btn-" + color} onClick={onClick}>Generate Playlist</button>
//     )
// }

// export default GeneratorButton;


import React from 'react';
import SpotifyAuth from './SpotifyAuth';

const GeneratorButton: React.FC = () => {
    return (
        <div>
            <SpotifyAuth />
        </div>
    );
};

export default GeneratorButton;