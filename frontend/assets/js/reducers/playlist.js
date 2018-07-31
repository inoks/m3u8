import {combineReducers} from 'redux';
import * as actions from '../actions';

const initialState = {
  channel: {},
  channels: [],
  playlist: {},
  playlists: [],
  isFetching: false,
  errors: {},
  isDeleted: false
};

export function playlists(state = initialState, action) {
  switch (action.type) {
    case actions.RECEIVED_ERRORS:
      return {
        ...state,
        errors: action.errors,
        isFetching: false
      };
    case actions.REQUEST_PLAYLISTS:
      return {
        ...state,
        isFetching: true,
        isDeleted: false,
        playlists: [],
      };
    case actions.RECEIVED_PLAYLISTS:
      return {
        ...state,
        isFetching: false,
        isDeleted: false,
        playlists: action.playlists,
      };
    case actions.RECEIVED_PLAYLIST:
      return {
        ...state,
        isFetching: false,
        isDeleted: false,
        playlist: action.playlist,
      };
    case actions.REQUEST_CHANNELS:
      return {
        ...state,
        isFetching: true,
        isDeleted: false,
        channels: []
      };
    case actions.RECEIVED_CHANNELS:
      return {
        ...state,
        isFetching: false,
        channels: action.channels,
      };
    case actions.REQUEST_CHANNEL:
      return {
        ...state,
        isFetching: true
      };
    case actions.RECEIVED_CHANNEL:
      return {
        ...state,
        isFetching: false,
        channel: {...action.channel},
      };
    case actions.REQUEST_PLAYLIST_UPDATE:
      return {
        ...state,
        isFetching: true
      };
    case actions.REQUEST_PLAYLIST_DELETE:
      return {
        ...state,
        isFetching: true
      };
    case actions.PLAYLIST_DELETED:
      return {
        ...state,
        isFetching: false,
        isDeleted: true,
        playlists: []
      };
    case actions.REQUEST_CHANNEL_DELETE:
      return {
        ...state,
        isFetching: true
      };
    case actions.CHANNEL_DELETED:
      return {
        ...state,
        isFetching: false,
        isDeleted: true
      };
    default:
      return state;
  }
}

const rootReducers = combineReducers({
  playlists,
});

export default rootReducers;
