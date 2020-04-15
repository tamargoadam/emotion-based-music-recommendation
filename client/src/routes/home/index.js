import { h, Component } from 'preact';
import 'preact-material-components/Card/style.css';
import {Button} from "preact-material-components";
import 'preact-material-components/Button/style.css';
import TwitterCard from '../../components/twitter-card/'
import AuthCard    from '../../components/auth-card/'
import style from './style';
import PlaylistCard from "../../components/playlist-card";

function getPlaylistPath(username, token) {
    return 'http://127.0.0.1:5000/playlist?user=' + username + '&token=' + token;
}

export default class Home extends Component {

    constructor(props) {
        super(props);

        this.state = {
            twitter_username: "",
            spotify_token: "",
            playlist_url: ""
        };
    }

    onTokenChange(token) {
        this.setState({
            spotify_token: token
        });
    }

    onUsernameChange(username) {
        this.setState({
            twitter_username: username
        });
    }

    render() {
        return (
        <div class={`${style.home} page`}>
            <h1>Link Accounts</h1>
            <AuthCard changeToken = {this.onTokenChange.bind(this)}/>
            {this.state.spotify_token &&
            <TwitterCard changeUsername={this.onUsernameChange.bind(this)}/>
            }
            {(this.state.spotify_token && this.state.twitter_username) &&
            <PlaylistCard spotify_token={this.state.spotify_token}
                          twitter_username={this.state.twitter_username}/>
            }
        </div>
        );
    }
}
