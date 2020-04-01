import { h, Component } from 'preact';
import Card from 'preact-material-components/Card';
import 'preact-material-components/Card/style.css';
import 'preact-material-components/Button/style.css';
import style from './style';

export default class TwitterCard extends Component {
  render() {
    return (
          <Card>
            <div class={style.cardHeader}>
              <h2 class=" mdc-typography--title">Link your Spotify account</h2>
            </div>
            <Card.Actions>
              <Card.ActionButton>SIGN IN</Card.ActionButton>
            </Card.Actions>
          </Card>
    );
  }
}
