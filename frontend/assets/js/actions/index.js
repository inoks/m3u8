import * as endpoints from "../constants/endpoints";

export const RECEIVED_PLAYLIST = 'RECEIVED_PLAYLIST';
export const RECEIVED_PLAYLISTS = 'RECEIVED_PLAYLISTS';
export const REQUEST_PLAYLIST = 'REQUEST_PLAYLIST';
export const REQUEST_PLAYLISTS = 'REQUEST_PLAYLISTS';
export const RECEIVED_CHANNELS = 'RECEIVED_CHANNELS';
export const REQUEST_CHANNELS = 'REQUEST_CHANNELS';
export const RECEIVED_CHANNEL = 'RECEIVED_CHANNEL';
export const REQUEST_CHANNEL = 'REQUEST_CHANNEL';
export const REQUEST_CHANNEL_UPDATE = 'REQUEST_CHANNEL_UPDATE';
export const RECEIVED_ERRORS = 'RECEIVED_ERRORS';
export const REQUEST_PLAYLIST_UPDATE = 'REQUEST_PLAYLIST_UPDATE';
export const REQUEST_PLAYLIST_DELETE = 'REQUEST_PLAYLIST_DELETE';
export const PLAYLIST_DELETED = 'PLAYLIST_DELETED';
export const REQUEST_CHANNEL_DELETE = 'REQUEST_CHANNEL_DELETE';
export const CHANNEL_DELETED = 'CHANNEL_DELETED';

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

let csrftoken = getCookie('csrftoken');

/* Function to include in each HTTP request */
function checkStatus(response, dispatch) {
  if (response.ok) {
    // Clear error dictionary
    return response;
  } else {
    // Check if response status === 400 - populate error dict
    if (response.status === 400) {
      response.json().then(json => dispatch(receivedErrors(json)));
    } else {
      console.log('receivedNetworkError', response);
    }
  }
}

export function fetchPlaylists() {
  return dispatch => {
    dispatch(requestPlaylists());
    return fetch(endpoints.API_PLAYLISTS, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'same-origin'
    })
      .then(response => checkStatus(response, dispatch))
      .then(response => {
        if (!response) {
          return;
        }
        return response.json()
      })
      .then(json => {
        if (json) {
          dispatch(receivedPlaylists(json))
        }
      });
  };
}

export function fetchPlaylist(id) {
  return dispatch => {
    dispatch(requestPlaylist());
    return fetch(endpoints.API_PLAYLISTS + id + '/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'same-origin'
    })
      .then(response => checkStatus(response, dispatch))
      .then(response => {
        if (!response) {
          return;
        }
        return response.json()
      })
      .then(json => {
        if (json) {
          dispatch(receivedPlaylist(json))
        }
      });
  };
}

export function fetchAllChannels() {
  return dispatch => {
    dispatch(requestChannels());
    return fetch(endpoints.API_CHANNELS, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'same-origin'
    })
      .then(response => checkStatus(response, dispatch))
      .then(response => {
        if (!response) {
          return;
        }
        return response.json()
      })
      .then(json => {
        if (json) {
          dispatch(receivedChannels(json))
        }
      });
  };
}

export function updateChannel(id, detail) {

  let endpoint, method;
  if (!id || id === 'new') {
    endpoint = endpoints.API_CHANNELS;
    method = 'POST';
  } else {
    endpoint = endpoints.API_CHANNELS + id + '/';
    method = 'PUT';
  }

  return dispatch => {
    dispatch({type: REQUEST_CHANNEL_UPDATE});
    return fetch(endpoint, {
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify(detail),
      credentials: 'same-origin'
    })
      .then(response => checkStatus(response, dispatch))
      .then(response => {
        if (!response) {
          return;
        }
        return response.json()
      })
      .then(json => {
        if (json) {
          dispatch(receivedChannel(json))
        }
      });
  };
}


export function deletePlaylist(id) {
  return dispatch => {
    dispatch(requestPlaylistDelete());
    return fetch(endpoints.API_PLAYLISTS + id + '/', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      credentials: 'same-origin'
    })
      .then(response => checkStatus(response, dispatch))
      .then(response => {
        if (!response) {
          return;
        }
        dispatch(deletedPlaylist());
      });
  };
}

export function deleteChannel(id) {
  return dispatch => {
    dispatch(requestChannelDelete());
    return fetch(endpoints.API_CHANNELS + id + '/', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      credentials: 'same-origin'
    })
      .then(response => checkStatus(response, dispatch))
      .then(response => {
        if (!response) {
          return;
        }
        dispatch(deletedChannel());
      });
  };
}

export function updatePlaylist(id, detail) {
  let endpoint, method;
  if (!id || id === 'new') {
    endpoint = endpoints.API_PLAYLISTS;
    method = 'POST';
  } else {
    endpoint = endpoints.API_PLAYLISTS + id + '/';
    method = 'PUT';
  }

  return dispatch => {
    dispatch({type: REQUEST_PLAYLIST_UPDATE});
    return fetch(endpoint, {
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify(detail),
      credentials: 'same-origin'
    })
      .then(response => checkStatus(response, dispatch))
      .then(response => {
        if (!response) {
          return;
        }
        return response.json()
      })
      .then(json => {
        if (json) {
          dispatch(receivedPlaylist(json))
        }
      });
  };
}

export function fetchChannel(id) {
  return dispatch => {
    dispatch(requestChannel());
    return fetch(endpoints.API_CHANNELS + id + '/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'same-origin'
    })
      .then(response => checkStatus(response, dispatch))
      .then(response => {
        if (!response) {
          return;
        }
        return response.json()
      })
      .then(json => {
        if (json) {
          dispatch(receivedChannel(json))
        }
      });
  };
}

export function fetchChannels(id) {
  return dispatch => {
    dispatch(requestChannels());
    return fetch(endpoints.API_PLAYLISTS + id + '/channels', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'same-origin'
    })
      .then(response => checkStatus(response, dispatch))
      .then(response => {
        if (!response) {
          return;
        }
        return response.json()
      })
      .then(json => {
        if (json) {
          dispatch(receivedChannels(json))
        }
      });
  };
}


/* DISPATCHERS FLOW FUNCTIONS */
function requestPlaylists() {
  return {
    type: REQUEST_PLAYLISTS
  };
}

function requestPlaylist() {
  return {
    type: REQUEST_PLAYLIST
  };
}

function receivedPlaylists(json) {
  return {
    type: RECEIVED_PLAYLISTS,
    playlists: json
  };
}

function receivedPlaylist(json) {
  return {
    type: RECEIVED_PLAYLIST,
    playlist: json
  };
}

function requestChannels() {
  return {
    type: REQUEST_CHANNELS
  };
}

function receivedChannels(json) {
  return {
    type: RECEIVED_CHANNELS,
    channels: json
  };
}

function requestChannel() {
  return {
    type: REQUEST_CHANNEL
  };
}

function receivedChannel(json) {
  return {
    type: RECEIVED_CHANNEL,
    channel: json
  };
}

function receivedErrors(json) {
  return {
    type: RECEIVED_ERRORS,
    errors: json
  };
}

function requestPlaylistDelete() {
  return {
    type: REQUEST_PLAYLIST_DELETE,
  };
}

function deletedPlaylist() {
  return {
    type: PLAYLIST_DELETED,
  };
}

function requestChannelDelete() {
  return {
    type: REQUEST_CHANNEL_DELETE,
  };
}

function deletedChannel() {
  return {
    type: CHANNEL_DELETED,
  };
}
