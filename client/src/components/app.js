import { h, Component } from 'preact';
import { Router } from 'preact-router';

import Header from './header';
import TwitterCard from './twitter-card';
import AuthCard from './auth-card';
import Home from '../routes/home';
import Profile from '../routes/profile';
import NotFound from '../routes/404';
import Recommend from '../routes/recommend'
import Feedback from '../routes/feedback'

export default class App extends Component {
  /** Gets fired when the route changes.
   *  @param {Object} event   "change" event from [preact-router](http://git.io/preact-router)
   *  @param {string} event.url The newly routed URL
   */
  handleRoute = e => {
    this.setState({
      currentUrl: e.url
    });
  };

  render() {
    return (
      <div id="app">
        <Header selectedRoute={this.state.currentUrl} />
        <Router onChange={this.handleRoute}>
          <Home path="/" />
          <Recommend path="/results/" />
          <Feedback path="/feedback/" />
          <NotFound default />
        </Router>
      </div>
    );
  }
}
