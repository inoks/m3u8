import React from 'react';
import {fetchChannels} from "../actions";
import {connect} from 'react-redux';
import {Link} from 'react-router-dom';
import FilterableChannelsList from "./FilterableChannelsList";

class PlaylistChannelsList extends React.Component {
  componentDidMount() {
    this.props.dispatch(fetchChannels(this.props.id));
  }

  render() {
    return (
      <div>
        <h3>Playlist Channels {this.props.id}</h3>
        <FilterableChannelsList channels={this.props.channels}/>
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  return {
    channels: state.playlists.channels,
  };
};

export default connect(mapStateToProps)(PlaylistChannelsList);
