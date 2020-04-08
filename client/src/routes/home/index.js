import { h, Component } from 'preact';
import 'preact-material-components/Card/style.css';
import 'preact-material-components/Button/style.css';
import TwitterCard from '../../components/twitter-card/'
import AuthCard    from '../../components/auth-card/'

import style from './style';

export default class Home extends Component {

    constructor(props) {
        super(props);

        this.state = {
            twitter_username: "",
            token: ""
        };
    }

    onTokenChange(token) {
        this.setState({
            token: token
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
            <h1>PART I: Sign in</h1>
            <AuthCard changeToken = {this.onTokenChange.bind(this)}/>
            {this.state.token &&
            <TwitterCard changeUsername={this.onUsernameChange.bind(this)}/>
            }
        </div>
        );
    }
}
