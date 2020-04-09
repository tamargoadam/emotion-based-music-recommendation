import { Component } from 'preact';
import Card from 'preact-material-components/Card';
import 'preact-material-components/Card/style.css';
import 'preact-material-components/Button/style.css';
import style from './style';

export const authEndpoint = 'https://accounts.spotify.com/authorize?';

const clientId = "2c505498d4de4226a5749df64d69d1a6";
const redirectUri = "http://localhost:8080";
const scopes = [
    "user-library-read",
    "user-top-read",
    "playlist-modify-public",
    "user-follow-read"
];

const hash = window.location.hash
    .substring(1)
    .split("&")
    .reduce(function(initial, item) {
        if (item) {
            let parts = item.split("=");
            initial[parts[0]] = decodeURIComponent(parts[1]);
        }
        return initial;
    }, {});

export default class AuthCard extends Component {

    constructor(props) {
        super(props);

        this.state = {
            token: props.token
        };
    }

    onTokenChange() {
        if(this.state.token) {
            this.props.changeToken(this.state.token);
        }
    }

    componentDidMount() {
        // Set token
        let _token = hash.access_token;
        if (_token) {
            this.setState({ token: _token },
                () => this.onTokenChange().bind(this));
        }
    }

    render() {
        return (
            <Card>
                <div class={style.cardHeader}>
                    <h2 class=" mdc-typography--title">Link your Spotify account</h2>
                </div>
                {!this.state.token && (
                    <a
                        className="btn btn--loginApp-link"
                        href={`${authEndpoint}client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scopes.join("%20")}&response_type=token&show_dialog=true`}
                    >
                        SIGN IN
                    </a>
                )}
                {this.state.token && (
                    <div>
                        You're Spotify account is connected!
                    </div>
                )}
            </Card>
        );
    }
}
