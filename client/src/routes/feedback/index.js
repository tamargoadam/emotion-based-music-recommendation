import { h, Component } from 'preact';
import Button from 'preact-material-components/Button';
import 'preact-material-components/Button/style.css';
import style from './style';
import List from 'preact-material-components/List';
import Card from 'preact-material-components/Card';
import 'preact-material-components/Card/style.css';
import 'preact-material-components/Button/style.css';


export default class Feedback extends Component {
  render() {
    return (
      <div class={`${style.home} page`}>
        <h1>PART III: Feedback</h1>
        <Card>
          <div class={style.cardHeader}>
            <h2 class=" mdc-typography--title">Let us know what you think</h2>
          </div>
          <div class={style.cardBody}>
            <ul class="mdc-list" role="radiogroup">
              <span>- - How strongly did you feel that these results reflect your current emotional state? - -</span>
              <li class="mdc-list-item" role="radio" aria-checked="false">
                <span class="mdc-list-item__graphic">
                <input 
                  class="mdc-radio__native_control"
                  type="radio"
                  value="1"
                ></input>
                <div class="mdc-radio__background">
                  <div class="mdc-radio__outer-circle"></div>
                  <div class="mdc-radio__outer-circle"></div>
                </div>
              </span>
              <label class="mdc-list-item__text">Inaccurate</label>
              </li>
              <li class="mdc-list-item" role="radio" aria-checked="false">
                <span class="mdc-list-item__graphic">
                <input 
                  class="mdc-radio__native_control"
                  type="radio"
                  value="2"
                ></input>
                <div class="mdc-radio__background">
                  <div class="mdc-radio__outer-circle"></div>
                  <div class="mdc-radio__outer-circle"></div>
                </div>
              </span>
              <label class="mdc-list-item__text">Somewhat inaccurate</label>

              </li>
              <li class="mdc-list-item" role="radio" aria-checked="false">
                <span class="mdc-list-item__graphic">
                <input 
                  class="mdc-radio__native_control"
                  type="radio"
                  value="1"
                ></input>
                <div class="mdc-radio__background">
                  <div class="mdc-radio__outer-circle"></div>
                  <div class="mdc-radio__outer-circle"></div>
                </div>
              </span>
              <label class="mdc-list-item__text">Somewhat accurate</label>
              </li>
              <li class="mdc-list-item" role="radio" aria-checked="false">
                <span class="mdc-list-item__graphic">
                <input 
                  class="mdc-radio__native_control"
                  type="radio"
                  value="1"
                ></input>
                <div class="mdc-radio__background">
                  <div class="mdc-radio__outer-circle"></div>
                  <div class="mdc-radio__outer-circle"></div>
                </div>
              </span>
              <label class="mdc-list-item__text">Accurate</label>
              </li>
            </ul>
          </div>
      <Card.Actions>
        <Card.ActionButton>NEXT</Card.ActionButton>
      </Card.Actions>
      </Card>
      </div>
    );
  }
}
