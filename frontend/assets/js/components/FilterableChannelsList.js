import React from 'react';
import * as endpoints from "../constants/endpoints";
import {connect} from 'react-redux';
import {Link} from 'react-router-dom';
import {FormGroup, ControlLabel, FormControl} from 'react-bootstrap';

export default class FilterableChannelsList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      q: '',
    };
    this.onChangeFilter = this.onChangeFilter.bind(this);
  }

  onChangeFilter(e) {
    this.setState({
      q: e.target.value
    })
  }

  render() {
    const {channels} = this.props;

    return (
      <div>
        <FormGroup>
          <ControlLabel>Filter list by title or group</ControlLabel>
          <FormControl
            type="text"
            value={this.state.q}
            placeholder="Enter text to filter"
            onChange={this.onChangeFilter}
          />
        </FormGroup>
        {channels && <ul>
          {channels
            .filter(channel => {
              return channel.title.toLowerCase().indexOf(this.state.q.toLowerCase()) > -1 || (channel.group !== null && channel.group.toLowerCase().indexOf(this.state.q.toLowerCase()) > -1)
            })
            .map(channel =>
              <li key={channel.id}>
                <Link to={endpoints.PATH_CHANNELS + channel.id}>
                  {channel.title} <strong>{channel.group}</strong>
                </Link>
              </li>
            )}
        </ul>}
      </div>
    )
  }
}
