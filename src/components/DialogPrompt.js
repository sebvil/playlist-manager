import React from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import FormControl from "@material-ui/core/FormControl";
import FormLabel from "@material-ui/core/FormLabel";
import RadioGroup from "@material-ui/core/RadioGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Radio from "@material-ui/core/Radio";

export default class FormDialog extends React.Component{

  constructor(props) {
    super(props);
    this.state = {
      name: ''
    }
  }


  render() {

    const { open, handleClose, visibility, handleChange, handleSubmit } = this.props;
    const handleNameChange = (event) => {
      this.setState({name: event.target.value});
    }
    return (
      <div >
        <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
          <DialogTitle id="form-dialog-title">Create New Playlist</DialogTitle>
          <DialogContent>
            <DialogContentText>
              Enter the playlist name
            </DialogContentText>
            <TextField
              autoFocus
              margin="dense"
              id="name"
              label="Playlist name"
              fullWidth
              onChange={handleNameChange}
            />
            <FormControl component="fieldset" margin="dense">
              <FormLabel component="legend">Visibility</FormLabel>
              <RadioGroup row aria-label="visibility" name="visibility" value={visibility} onChange={handleChange}>
                <FormControlLabel value="public" control={<Radio />} label="Public" />
                <FormControlLabel value="private" control={<Radio />} label="Private" />
              </RadioGroup>
            </FormControl>
          </DialogContent>

          <DialogActions>
            <Button onClick={handleClose} color="primary">
              Cancel
            </Button>
            <Button onClick={() => {
              handleSubmit(this.state.name, visibility);
            }} color="primary">
              Create Playlist
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
}
