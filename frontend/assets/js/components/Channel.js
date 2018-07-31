import React from 'react';
import {Link} from 'react-router-dom';
import * as actions from "../actions";
import {connect} from 'react-redux';
import {Button, FormControl, ControlLabel, FormGroup, HelpBlock} from 'react-bootstrap';
import ReactHLS from 'react-hls';
import * as endpoints from "../constants/endpoints";


class Channel extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      id: this.props.match.params.id,
      channel: {
        playlists: []
      }
    };
    this.onSave = this.onSave.bind(this);
    this.onDelete = this.onDelete.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handlePlaylistsChange = this.handlePlaylistsChange.bind(this);
  }

  handleChange(e) {
    this.setState({
      channel: {
        ...this.state.channel,
        [e.target.id]: e.target.value
      }
    });
  }

  handlePlaylistsChange(e) {
    this.setState({
      channel: {
        ...this.state.channel,
        playlists: [...e.target.options].filter(o => o.selected).map(o => o.value)
      }
    });
  }

  onSave() {
    this.props.dispatch(actions.updateChannel(this.state.id, this.state.channel));
  }

  onDelete() {
    this.props.dispatch(actions.deleteChannel(this.state.id));
  }

  componentDidMount() {
    if (this.state.id !== 'new') {
      this.props.dispatch(actions.fetchChannel(this.state.id));
    }
    if (this.props.playlists.length === 0) {
      this.props.dispatch(actions.fetchPlaylists());
    }
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.isDeleted) {
      this.props.history.push(endpoints.PATH_CHANNELS);
      return;
    }
    this.setState({
      channel: nextProps.channel,
      id: nextProps.channel.id
    });
  }

  render() {
    return (
      this.props.isFetching ? (<h4>Loading</h4>) :
        (<div>
          <FormGroup>
            <ControlLabel>Channel Playlists</ControlLabel>
            <FormControl
              id="playlists"
              componentClass="select"
              value={this.state.channel.playlists || []}
              multiple
              onChange={this.handlePlaylistsChange}
            >
              {this.props.playlists.map(playlist =>
                <option key={playlist.id} value={playlist.id}>
                  {playlist.title}
                </option>
              )}
            </FormControl>
          </FormGroup>

          <FormGroup>
            <ControlLabel>Channel Title</ControlLabel>
            <FormControl
              id="title"
              type="text"
              value={this.state.channel.title || ''}
              placeholder="Enter Title"
              onChange={this.handleChange}
            />
          </FormGroup>

          <FormGroup>
            <ControlLabel>Channel Group</ControlLabel>
            <FormControl
              id="group"
              type="text"
              value={this.state.channel.group || ''}
              placeholder="Enter Group Name"
              onChange={this.handleChange}
            />
          </FormGroup>

          <FormGroup>
            <ControlLabel>Channel Content Path</ControlLabel>
            <FormControl
              id="path"
              type="text"
              value={this.state.channel.path || ''}
              placeholder="Enter Path"
              onChange={this.handleChange}
            />
            {this.props.errors.path && <HelpBlock>{this.props.errors.path}</HelpBlock>}
          </FormGroup>

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
            Delete Channel
          </Button>

          {this.state.channel.path && this.state.channel.path.startsWith('http') &&
          <ReactHLS url={this.state.channel.path}/>}

        </div>)
    )
  }
}

const mapStateToProps = (state) => {
  return {
    playlists: state.playlists.playlists,
    errors: state.playlists.errors,
    channel: state.playlists.channel,
    isFetching: state.playlists.isFetching,
    isDeleted: state.playlists.isDeleted
  };
};

export default connect(mapStateToProps)(Channel);
