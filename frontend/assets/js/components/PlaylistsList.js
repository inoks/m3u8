import React from 'react';
import {Link} from 'react-router-dom';
import * as endpoints from "../constants/endpoints";
import {fetchPlaylists} from "../actions";
import {connect} from 'react-redux';

class PlaylistsList extends React.Component {
  componentDidMount() {
    const {dispatch} = this.props;
    dispatch(fetchPlaylists());
  }

  render() {
    const {playlists} = this.props;
    return (
      <div>
        <h4>My Playlists</h4>
        <Link to={endpoints.PATH_PLAYLISTS + 'new/'}>Add New Playlist</Link>

        {playlists && <ul>
          {playlists.map(playlist =>
            <li key={playlist.id}>
              <Link to={endpoints.PATH_PLAYLISTS + playlist.id}>{playlist.title} ({playlist.count})</Link>
              &nbsp;Public link:
              <a href={playlist.public_link} target='_blank'>{playlist.public_link}</a>
            </li>
          )}
        </ul>}
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  return {
    playlists: state.playlists.playlists,
  };
};

export default connect(mapStateToProps)(PlaylistsList);
