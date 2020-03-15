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
              <h2 class=" mdc-typography--title">Home card</h2>
              <div class=" mdc-typography--caption">Welcome to home route</div>
            </div>
            <div class={style.cardBody}>
              login to twitter
            </div>
            <Card.Actions>
              <Card.ActionButton>Link Twitter</Card.ActionButton>
            </Card.Actions>
          </Card>
    );
  }
}
