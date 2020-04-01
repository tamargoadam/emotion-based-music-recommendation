import { h, Component } from 'preact';
import Card from 'preact-material-components/Card';
import 'preact-material-components/Card/style.css';
import 'preact-material-components/Button/style.css';

import style from './style';

export default class Recommend extends Component {
  render() {
    return (
      <div class={`${style.home} page`}>
        <h1>PART II: Recommendations</h1>
        <Card>
          <div class={style.cardHeader}>
            <h2 class=" mdc-typography--title">Your own personalized playlist</h2>
            <div class=" mdc-typography--caption">Based on your recent activity we came up with this playlist for you!...</div>
          </div>
          <div class={style.cardBody}>
            <ul>
              <div>1. O c e a n s D r e a m e r s by Sunlight-91</div>
              <div>2. First Snow by Kerusu</div>
              <div>3. Close My Eyes by WYS</div>
              <div>4. Zone by JaySwan</div>
            <div>5. Little Cloud by ElektroBin</div>
            <div>6. Passionfruit by Drake</div>
          </ul>
      </div>
      <Card.Actions>
        <Card.ActionButton>Save to my Spotify!</Card.ActionButton>
        <Card.ActionButton>NEXT</Card.ActionButton>
      </Card.Actions>
      </Card>
      </div>
    );
  }
}
