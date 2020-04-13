import { Component } from 'preact';
import Card from 'preact-material-components/Card';
import 'preact-material-components/Card/style.css';
import 'preact-material-components/Button/style.css';
import style from './style';
import {Button, TextField} from "preact-material-components";

function getPlaylistPath(username, token, name, songs) {
    return 'http://127.0.0.1:5000/playlist?user=' + username + '&token=' + token + '&name=' + name + '&songs=' + songs;
}

export default class PlaylistCard extends Component {
    constructor(props) {
        super(props);

        this.state = {
            twitter_username: props.twitter_username,
            spotify_token: props.spotify_token,
            playlist_name: "",
            num_songs: 50,
            playlist_url: ""
        };
    }

    toggleButtonState = () => {
        if(this.state.playlist_name && this.state.num_songs) {
            fetch(getPlaylistPath(this.state.twitter_username, this.state.spotify_token, this.state.playlist_name, this.state.num_songs))
                .then(function (response) {
                    return response.text();
                })
                .then(data =>
                    this.setState({playlist_url: data})
                )
                .catch(function (error) {
                    console.log(error);
                });
        }
        else {
            alert("Please enter a name for your playlist, or a number for the amount of songs.")
        }
    }

    render() {
        return (
            <Card>
                <div class={style.cardHeader}>
                    <h2 class=" mdc-typography--title">Name your playlist</h2>
                </div>
                <div>
                    <TextField class={style.textInput}label="Playlist Name"
                        onKeyUp={e => {
                            this.setState({
                                playlist_name: e.target.value
                            });
                        }}
                    />
                </div>
                <div>
                    <TextField defaultValue={50} class={style.textInput}label="Playlist Song Amount"
                        onKeyUp={e => {
                            this.setState({
                                num_songs: e.target.value
                            });
                        }}
                    />
                </div>
                {!this.state.playlist_url &&
                <Button raised ripple onClick={this.toggleButtonState.bind(this)}>
                    Create my playlist
                </Button>
                }
                {this.state.playlist_url &&
                <a class={style.link} href={this.state.playlist_url}>Click here to view your playlist!</a>
                }
            </Card>
        );
    }
}
