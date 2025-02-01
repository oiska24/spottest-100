import './App.css'
import GeneratorButton from './components/GeneratorButton'
import Title from './components/Title'
import Disclaimer from './components/Disclaimer';
// import { generatePlaylist } from './ts/generate_playlist';
// import * as spotify from './ts/spotify_auth';

function App() {
  return (
    <>
      <Title></Title>
      <GeneratorButton />
      <Disclaimer></Disclaimer>      
    </>
  )
}

export default App
