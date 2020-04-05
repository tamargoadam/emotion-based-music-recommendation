import { Component } from 'preact';
import Card from 'preact-material-components/Card';
import 'preact-material-components/Card/style.css';
import 'preact-material-components/Button/style.css';
import style from './style';
import {TextField} from "preact-material-components";

const VALIDATE_PATH = 'http://127.0.0.1:5000/twitter-username?user='

export default class TwitterCard extends Component {
    constructor(props) {
        super(props);

        this.state = {
            text_input: "",
            twitter_username: "",
            valid: false
        };
    }

    toggleButtonState = () => {
        let currentComponent = this;
        fetch(VALIDATE_PATH + this.state.text_input)
            .then(function(response) {
                return response.text();
            })
            .then( data => {
                currentComponent.setState({
                    ...state,
                    twitter_username: data,
                    valid: true
                })
            })
            .catch(function(error) {
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
              <Card.Actions onClick= {this.toggleButtonState}>
                  <Card.ActionButton>SIGN IN</Card.ActionButton>
              </Card.Actions>
          </Card>
    );
  }
}
