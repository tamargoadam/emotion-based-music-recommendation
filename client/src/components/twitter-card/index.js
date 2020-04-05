import { h, Component } from 'preact';
import Card from 'preact-material-components/Card';
import 'preact-material-components/Card/style.css';
import 'preact-material-components/Button/style.css';
import style from './style';

const VALIDATE_PATH = 'http://127.0.0.1:5000/twitter-username?user='

export default class TwitterCard extends Component {
    constructor(props) {
        super(props);

        this.state = {
            twitter_username: "",
            valid: false
        };
    }

    toggleButtonState = () => {
        fetch(VALIDATE_PATH + 'atamargo')
            .then(function(response) {
                return response.text();
            })
            .then( data => {
                this.setState({
                    twitter_username: data,
                    valid: true
                })
            });
    }

    render() {
      return (
          <Card>
            <div class={style.cardHeader}>
              <h2 class=" mdc-typography--title">Link your Twitter account</h2>
            </div>
            <Card.Actions onClick= {this.toggleButtonState}
            >
              <Card.ActionButton>SIGN IN</Card.ActionButton>
            </Card.Actions>
          </Card>
    );
  }
}
