import React from 'react';
import {Link} from 'react-router-dom';
import {fetchPlaylist} from "../actions";
import {connect} from 'react-redux';
import PlaylistChannelsList from "./PlaylistChannelsList";
import {FormGroup, ControlLabel, FormControl, HelpBlock, Button} from 'react-bootstrap';
import * as actions from "../actions";
import * as endpoints from '../constants/endpoints';


class Playlist extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      id: this.props.match.params.id,
      playlist: {}
    };
    this.handleChange = this.handleChange.bind(this);
    this.onSave = this.onSave.bind(this);
    this.onDelete = this.onDelete.bind(this);
  };

  onSave() {
    this.props.dispatch(actions.updatePlaylist(this.state.id, this.state.playlist));
  }

  onDelete() {
    this.props.dispatch(actions.deletePlaylist(this.state.id));
  }

  componentDidMount() {
    if (this.state.id !== 'new') {
      this.props.dispatch(fetchPlaylist(this.state.id));
    }
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.isDeleted) {
      this.props.history.push(endpoints.PATH_PLAYLISTS);
      return;
    }

    this.setState({
      playlist: {...nextProps.playlist},
      id: nextProps.playlist.id
    });
  }

  handleChange(e) {
    this.setState({
      playlist: {
        ...this.state.playlist,
        [e.target.id]: e.target.value
      }
    });
  }

  render() {
    const {id} = this.props.match.params;
    return (
      <div>
        <FormGroup>
          <ControlLabel>Playlist Title</ControlLabel>
          <FormControl
            id='title'
            type="text"
            value={this.state.playlist.title || ''}
            placeholder="Enter playlist title"
            onChange={this.handleChange}
          />
          <FormControl.Feedback/>
          <HelpBlock>{this.props.errors.title}</HelpBlock>
          <Button
            bsStyle="primary"
            disabled={this.props.isFetching}
            onClick={this.onSave}
          >
            Save
          </Button>
          <Button
            bsStyle="danger"
            disabled={this.props.isFetching}
            onClick={this.onDelete}
          >
            Delete
          </Button>
        </FormGroup>
        {this.state.id !== 'new' && <PlaylistChannelsList id={this.state.id}/>}
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  return {
    playlist: state.playlists.playlist,
    errors: state.playlists.errors,
    isFetching: state.playlists.isFetching,
    isDeleted: state.playlists.isDeleted
  };
};

export default connect(mapStateToProps)(Playlist);
