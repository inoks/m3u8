import Root from './containers/Root';
import React from 'react';
import ReactDOM from 'react-dom';
import {AppContainer} from 'react-hot-loader';
import Provider from "react-redux/es/components/Provider";
import configureStore from './store/store';

const store = configureStore();

const render = Component => {
  ReactDOM.render(
    <Provider store={store}>
      <AppContainer>
        <Component/>
      </AppContainer>
    </Provider>,
    document.getElementById('root')
  )
};

render(Root);

if (module.hot) {
  module.hot.accept();
}
