import './App.css'
import GeneratorButton from './components/GeneratorButton'
import Title from './components/Title'
import Disclaimer from './components/Disclaimer';
import { generatePlaylist } from './ts/generate_playlist';

function App() {
  return (
    <>
      <Title></Title>
      <GeneratorButton color="dark" onClick={() => generatePlaylist()}></GeneratorButton>
      <Disclaimer></Disclaimer>      
    </>
  )
}

export default App
