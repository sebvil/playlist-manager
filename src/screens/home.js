import React from 'react';
import Button from "@material-ui/core/Button";
import { withRouter } from "react-router";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import Checkbox from "@material-ui/core/Checkbox";
import ListItemText from "@material-ui/core/ListItemText";
import List from "@material-ui/core/List";
import ListItemSecondaryAction from "@material-ui/core/ListItemSecondaryAction";
import CircularProgress from "@material-ui/core/CircularProgress";
import TracksTable from "../components/TracksTable";
import Sidebar from "react-sidebar";
import FormControl from "@material-ui/core/FormControl";
import InputLabel from "@material-ui/core/InputLabel";
import Input from "@material-ui/core/Input";
import FormHelperText from "@material-ui/core/FormHelperText";
import Fab from "@material-ui/core/Fab";
import AddIcon from '@material-ui/icons/Add';
import DialogPrompt from "../components/DialogPrompt";

const mql = window.matchMedia(`(min-width: 800px)`);

class Home extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      username: '',
      loading: true,
      playlists: null,
      checked: [],
      sidebarDocked: mql.matches,
      sidebarOpen: false,
      width: 0,
      height: 0,
      search: '',
      artist: '',
      album: '',
      searchCount: 0,
      open: false,
      visibility: 'public',
      tracks: [],
      checkedTracks: []
    };
    this.mediaQueryChanged = this.mediaQueryChanged.bind(this);
    this.onSetSidebarOpen = this.onSetSidebarOpen.bind(this);
    this.updateWindowDimensions = this.updateWindowDimensions.bind(this);
  };

  componentDidMount() {
    mql.addEventListener("change", () => {
      this.mediaQueryChanged();
    });

    this.updateWindowDimensions();
    window.addEventListener('resize', this.updateWindowDimensions);

    fetch('/check_login').then(res => res.json().then(data => {
      console.log(data);

      if (data['logged_in'] === 'false') {
        console.log('test');
        this.props.history.push('/');
      }
    }).then(() => {
      fetch('/get_playlists').then(res => res.json().then(data => {
        this.setState({ playlists: data['playlists'] }, () => {
          console.log(this.state.playlists);
          this.setState({ loading: false })
        });
      }));
    }).catch(err => {
      console.log(err);
    }))
  }

  componentWillUnmount() {
    mql.removeEventListener("change", () => {
      this.mediaQueryChanged();
    });
    window.removeEventListener('resize', this.updateWindowDimensions);

  }

  onSetSidebarOpen(open) {
    this.setState({ sidebarOpen: open });
  }

  mediaQueryChanged() {
    this.setState({ sidebarDocked: mql.matches, sidebarOpen: false });
  }



  updateWindowDimensions() {
    console.log(this.state)
    this.setState({ width: window.innerWidth, height: window.innerHeight });
  }
  render() {

    const handleToggle = (value) => () => {
      const currentIndex = this.state.checked.indexOf(value);
      const newChecked = [...this.state.checked];

      if (currentIndex === -1) {
        newChecked.push(value);
      } else {
        newChecked.splice(currentIndex, 1);
      }

      this.setState({ checked: newChecked });
    };

    const handleSearchChange = (event) => {
      this.setState({ search: event.target.value });
    };

    const handleArtistChange = (event) => {
      this.setState({ artist: event.target.value });
    };

    const handleAlbumChange = (event) => {
      this.setState({ album: event.target.value });
    };

    const handleButtonClick = () => {
      this.setState({ searchCount: this.state.searchCount + 1 });
    }

    const handleClickOpen = () => {
      console.log(this.state);
      this.setState({ open: true });
    };

    const handleClose = () => {
      this.setState({ open: false });
    };

    const handleChange = (event) => {
      this.setState({ visibility: event.target.value });
    }

    const handleSearch = () => {
      let query = '';

      const { search, album, artist } = this.state;

      if (search !== '') {
        query = query.concat('search=', search);
        console.log(search);
      }
      if (artist !== '') {
        if (query.length > 0) {
          query = query.concat('&artist=', artist);
        } else {
          query = query.concat('artist=', artist);
        }
        console.log(artist)
      }

      if (album !== '') {
        if (query.length > 0) {
          query = query.concat('&album=', album);
        } else {
          query = query.concat('album=', album);
        }
      }
      if (query.length == 0) {
        query = '/search';
      } else {
        query = '/search?'.concat(query, '&unique=True');
      }
      console.log(query);
      fetch(query).then(res => res.json()).then(data => {
        let result = data['result']
        result.sort((a, b) => (a.track > b.track) ? 1 : -1)
        this.setState({ tracks: result });
      });
    }

    const handleChangeCheck = (value) => {
      const currentIndex = this.state.checkedTracks.indexOf(value);
      const newChecked = [...this.state.checkedTracks];

      if (currentIndex === -1) {
        newChecked.push(value);
      } else {
        newChecked.splice(currentIndex, 1);
      }

      this.setState({ checkedTracks: newChecked });
    }
    const handleNewPlaylist = (name, visibility) => {
      let playlists = this.state.checked.map(playlist => playlist['uri']);

      fetch('/new/' + name + '/' + visibility).then(ref => ref.json().then(data => {
        if ('error' in data) {
          console.log(data);
        }
        else {
          console.log(data);
        }
      }).then(() => {
        this.setState({ open: false });
      }));
    }

    if (this.state.loading) {
      return (
        <CircularProgress />
      );

    }

    const handleAddToPlaylist = () => {
      const tracks = this.state.checkedTracks.map(item => item['track_id']);
      const playlists = this.state.checked.map(item => item['uri']);
      const data = {
        playlists: playlists,
        tracks: tracks
      };
      fetch('/add', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: { 'Content-Type': 'application/json' }
      }).then(res => res.json().then(data => {
        console.log(data);
      }));
    }
    return (
      <div style={{ display: 'flex', overflowY: 'hidden' }}>
        <div style={{ flex: 1, maxHeight: this.state.height, overflow: 'hidden', minWidth: '200px' }}>
          <div>
            <List style={{ overflow: 'auto', maxHeight: this.state.height - 120 }}>
              {this.state.playlists.map((value) => {
                const labelId = `checkbox-list-label-${value['name']}`;
                return (
                  <ListItem key={value['name']} role={undefined} dense button onClick={handleToggle(value)}>
                    <ListItemIcon>
                      <Checkbox
                        edge="start"
                        checked={this.state.checked.indexOf(value) !== -1}
                        tabIndex={-1}
                        disableRipple
                        inputProps={{ 'aria-labelledby': labelId }}
                      />
                    </ListItemIcon>
                    <ListItemText id={labelId} primary={value['name']} style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }} />
                  </ListItem>
                );
              })}
            </List>
          </div>
          <div >
            <Fab color='primary'
              aria-label='add'
              variant='extended'
              size='small'
              onClick={handleClickOpen}>
              <AddIcon />
          New Playlist
        </Fab>
          </div>
        </div>
        <div style={{ flex: 4 }}>

          <div style={{ display: 'flex' }}>
            <FormControl style={{ flex: 2 }}>
              <InputLabel htmlFor="search" style={{ color: 'white' }}>Enter search terms</InputLabel>
              <Input
                id="search"
                value={this.state.search}
                onChange={handleSearchChange}
                style={{ width: '75%', color: 'white' }}
                aria-describedby="search-text"
              />
            </FormControl>

            <FormControl style={{ flex: 2 }}>
              <InputLabel htmlFor="artist-helper" style={{ color: 'white' }}>Filter by artist</InputLabel>
              <Input
                id="artist-helper"
                value={this.state.artist}
                onChange={handleArtistChange}
                aria-describedby="artist-helper-text"
                style={{ width: '75%', color: 'white' }}
              />
            </FormControl>

            <FormControl style={{ flex: 2 }}>
              <InputLabel htmlFor="album-helper" style={{ color: 'white' }}>Filter by album</InputLabel>
              <Input
                id="album-helper"
                value={this.state.album}
                variant='filled'
                onChange={handleAlbumChange}
                aria-describedby="album-helper-text"
                style={{ width: '75%', color: 'white' }}
              />
            </FormControl>
            <Button style={{ flex: 1, background: 'green' }} onClick={handleSearch} >Search</Button>
          </div>
          <TracksTable
            trackData={this.state.tracks}
            checked={this.state.checkedTracks}
            handleChangeClick={handleChangeCheck}
          />
          <Button style={{ background: 'green' }} onClick={handleAddToPlaylist} >Add to Playlist</Button>
        </div>
        <DialogPrompt open={this.state.open}
          handleClose={handleClose}
          visibility={this.state.visibility}
          handleChange={handleChange}
          handleSubmit={handleNewPlaylist}
        />
      </div>
    )
  }

}

export default withRouter(Home);