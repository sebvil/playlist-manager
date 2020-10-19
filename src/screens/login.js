import React from 'react';
import Button from "@material-ui/core/Button";
import { withRouter } from "react-router";

class Login extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      username : '',
      loading: true
    };

  };

  componentDidMount() {
    fetch('/check_login').then(res => res.json().then(data => {
      console.log(data);

      if (data['logged_in'] === 'true') {
        console.log('test');
        this.props.history.push('/home');
      }
    }).catch(err => {
      console.log(err);
    }))
  }

  render() {
    const handleButtonClick = () => {
      fetch('/login').then( res => res.json().then(data =>  {
        console.log(data)
        if (data['logged_in'] === 'true') {
          console.log('test');
          this.props.history.push('/home');
        }
      }));
    }


    return(
      <div>
      <p>Login with Spotify to begin using the Playlist Manager</p>
        <Button
          style={{background: 'green'}}
          onClick={handleButtonClick}
        >Log in</Button>
      </div>
    )
  }

}

export default withRouter(Login);