import React from 'react';
import ReactPlayer from "react-player";
import {makeStyles, useTheme} from "@material-ui/core/styles";

const styles = makeStyles((theme) => ({
  player_wrapper: {
    position: 'relative',
    height: '10%'
  },
  react_player: {
    position: 'relative',
    top: 0,
    left: 0,
  }
}));



export default function ResponsivePlayer(props) {
    const {url} = props;
    const classes = styles();

    return (
      <div className={classes.player_wrapper}>
        <ReactPlayer
          className={classes.react_player}
          url={url}
          controls={true}
          height='50px'
          width='100%%'
        />
    </div>
    )

}