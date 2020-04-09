import { h, Component } from 'preact';
import 'preact-material-components/Card/style.css';
import {Button} from "preact-material-components";
import 'preact-material-components/Button/style.css';
import TwitterCard from '../../components/twitter-card/'
import AuthCard    from '../../components/auth-card/'
import style from './style';

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

    toggleButtonState = () => {
        fetch(getPlaylistPath(this.state.twitter_username, this.state.spotify_token))
            .then(function(response) {
                return response.text();
            })
            .then(data => 
                this.setState({ playlist_url: data })
            )
            .catch(function (error) {
                console.log(error);
            });
    }

    render() {
        return (
        <div class={`${style.home} page`}>
            <h1>Sign in</h1>
            <AuthCard changeToken = {this.onTokenChange.bind(this)}/>
            {this.state.spotify_token &&
            <TwitterCard changeUsername={this.onUsernameChange.bind(this)}/>
            }
            <br/>
            {(this.state.spotify_token && this.state.twitter_username && !this.state.playlist_url) &&
            <Button raised ripple onClick={this.toggleButtonState.bind(this)}>
                Create my playlist
            </Button>
            }
            <br/>
            {this.state.playlist_url &&
            <a href={this.state.playlist_url}>Click here to view your playlist!</a>}
        </div>
        );
    }
}
