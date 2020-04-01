import { h, Component } from 'preact';
import Card from 'preact-material-components/Card';
import 'preact-material-components/Card/style.css';
import 'preact-material-components/Button/style.css';
import TwitterCard from '../../components/twitter-card/'
import AuthCard    from '../../components/auth-card/'

import style from './style';

export default class Home extends Component {
  render() {
    return (
      <div class={`${style.home} page`}>
        <h1>PART I: Sign in</h1>
        <TwitterCard /> 
        <AuthCard /> 
      </div>
    );
  }
}
