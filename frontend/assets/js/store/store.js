import {applyMiddleware, createStore} from 'redux';
import thunkMiddleware from 'redux-thunk';
import {createLogger} from 'redux-logger'
import rootReducers from '../reducers/playlist';


export default function configureStore(initialState) {
  const store = createStore(
    rootReducers,
    initialState,
    applyMiddleware(thunkMiddleware, createLogger()),
    applyMiddleware(thunkMiddleware)
  );

  if (module.hot) {
    // Enable Webpack hot module replacement for reducers
    module.hot.accept('../reducers/playlist', () => {
      const nextRootReducer = require('../reducers/playlist');
      store.replaceReducer(nextRootReducer);
    });
  }

  return store;
};
