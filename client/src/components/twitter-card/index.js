import { Component } from 'preact';
import Card from 'preact-material-components/Card';
import 'preact-material-components/Card/style.css';
import 'preact-material-components/Button/style.css';
import style from './style';
import {TextField} from "preact-material-components";

const VALIDATE_PATH = 'http://127.0.0.1:5000/twitter-username?user='

class ValidationError extends Error {
    constructor(message) {
        super(message);
        this.name = "ValidationError";
    }
}

export default class TwitterCard extends Component {
    constructor(props) {
        super(props);

        this.state = {
            text_input: "",
            twitter_username: props.twitter_username,
            valid: false
        };
    }

    onUsernameChange() {
        if(this.state.valid) {
            this.props.changeUsername(this.state.twitter_username)
        }
    }

    toggleButtonState = () => {
        fetch(VALIDATE_PATH + this.state.text_input)
            .then(function(response) {
                if(response.status == 400 || response.status == 403){
                    throw new ValidationError("The username entered is invalid.")
                }
                return response.text();
            })
            .then( data => {
                this.setState({
                    twitter_username: data,
                    valid: true
                });
            })
            .then(() => this.onUsernameChange().bind(this))
            .catch(function(error) {
                if(error.name == 'ValidationError')
                    alert(error);
                console.log(error);
            });
    }

    render() {
      return (
          <Card>
              <div class={style.cardHeader}>
              <h2 class=" mdc-typography--title">Link your Twitter account</h2>
              </div>
              <div>
                  <TextField
                  label="Username"
                  onKeyUp={e => {
                      this.setState({
                          text_input: e.target.value
                      });
                  }}
                  />
              </div>
              <Card.Actions onClick={this.toggleButtonState.bind(this)}>
                  <Card.ActionButton>Link Account</Card.ActionButton>
              </Card.Actions>
              {this.state.twitter_username &&
              "Twitter account, " + this.state.twitter_username + ", is connected!"}
          </Card>
    );
  }
}
