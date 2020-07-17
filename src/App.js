import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import TracksTable from "./components/TracksTable";
import Input from "@material-ui/core/Input";
import FormControl from '@material-ui/core/FormControl';
import FormHelperText from '@material-ui/core/FormHelperText';
import InputLabel from '@material-ui/core/InputLabel';
import Button from "@material-ui/core/Button";
import Login from "./screens/login";

import {MuiThemeProvider, createMuiTheme} from '@material-ui/core/styles';
import Routes from "./Routes";
import './App.css';
import {createBrowserHistory} from "history";
import { Router } from 'react-router';
import indigo from '@material-ui/core/colors/indigo';
import pink from '@material-ui/core/colors/pink';
import red from '@material-ui/core/colors/red';
import green from "@material-ui/core/colors/green";

const theme = createMuiTheme({
  palette: {
    primary: green,
    secondary: pink,
    error: red,
    // Used by `getContrastText()` to maximize the contrast between the background and
    // the text.
    contrastThreshold: 3,
    // Used to shift a color's luminance by approximately
    // two indexes within its tonal palette.
    // E.g., shift from Red 500 to Red 300 or Red 700.
    tonalOffset: 0.2,
  },
})

const browserHistory = createBrowserHistory();


class App extends React.Component {
  render() {
    return (
      <div className="App">
      <header className="App-header">
      <MuiThemeProvider theme={theme}>
        <Router history={browserHistory}>
          <Routes />
        </Router>
      </MuiThemeProvider>
      </header>
      </div>

    );
  }
}

// function App() {
//   const [currentTime, setCurrentTime] = useState(0);
//   const [search, setSearch] = useState('');
//   const [artist, setArtist] = useState('melendi');
//   const [album, setAlbum] = useState('');
//   const [playlists, setPlaylists] = useState([]);
//   const [url, setUrl] = useState('');
//   useEffect(() => {
//     fetch('/login').then( res => res.json().then(data =>  {
//       console.log(data)
//     }));
//   }, []);
//
//   const handleSearchChange = (event) => {
//     setSearch(event.target.value);
//   };
//
//   const handleArtistChange = (event) => {
//     setArtist(event.target.value);
//   };
//
//   const handleAlbumChange = (event) => {
//     setAlbum(event.target.value);
//   };
//
//   const handleButtonClick = () => {
//     fetch("https://accounts.spotify.com/authorize").then(res => {
//       console.log(res);
//     });
//   }
//   return (
//     <div className="App">
//       <header className="App-header">
//         <Login/>
//         {/*<Button*/}
//         {/*  style={{background: 'blue'}}*/}
//         {/*  onClick={handleButtonClick}*/}
//         {/*  >Log in</Button>*/}
//
//         {/*<div style={{background: 'white', width: '100%', justifyContent: 'space-evenly', flexDirection: 'row'}}>*/}
//         {/*  <FormControl style={{width: '33%'}}>*/}
//         {/*    <InputLabel htmlFor="search">Search</InputLabel>*/}
//         {/*    <Input*/}
//         {/*      id="search"*/}
//         {/*      value={search}*/}
//         {/*      onChange={handleSearchChange}*/}
//         {/*      style={{width: '75%'}}*/}
//         {/*      aria-describedby="search-text"*/}
//         {/*    />*/}
//         {/*    <FormHelperText id="search-text">Some important helper text</FormHelperText>*/}
//         {/*  </FormControl>*/}
//
//         {/*  <FormControl style={{width: '33%'}}>*/}
//         {/*    <InputLabel htmlFor="artist-helper">Artist</InputLabel>*/}
//         {/*    <Input*/}
//         {/*      id="artist-helper"*/}
//         {/*      value={artist}*/}
//         {/*      onChange={handleArtistChange}*/}
//         {/*      aria-describedby="artist-helper-text"*/}
//         {/*      style={{width: '75%'}}*/}
//         {/*    />*/}
//         {/*    <FormHelperText id="artist-helper-text">Some important helper text</FormHelperText>*/}
//         {/*  </FormControl>*/}
//
//         {/*  <FormControl style={{width: '33%'}}>*/}
//         {/*    <InputLabel htmlFor="album-helper">Album</InputLabel>*/}
//         {/*    <Input*/}
//         {/*      id="album-helper"*/}
//         {/*      value={album}*/}
//         {/*      onChange={handleAlbumChange}*/}
//         {/*      aria-describedby="album-helper-text"*/}
//         {/*      style={{width: '75%'}}*/}
//         {/*    />*/}
//         {/*    <FormHelperText id="album-helper-text">Some important helper text</FormHelperText>*/}
//         {/*  </FormControl>*/}
//         {/*</div>*/}
//         {/*<TracksTable*/}
//         {/*  search={search}*/}
//         {/*  artist={artist}*/}
//         {/*  album={album}*/}
//         {/*/>*/}
//       </header>
//     </div>
//   );
// }

export default App;
