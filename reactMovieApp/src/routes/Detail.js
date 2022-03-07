import React from 'react';

class Detail extends React.Component {
    componentDidMount() {
        const {location, history } = this.props;
        if (location.state === undefined) {   // location.state가 없는 경우는 home으로 redirect
            history.push('/');
        }
    }

    render() {
        const { location } = this.props;
        if (location.state) {
            return <span>{location.state.title}</span>;
        }else{
            return null;
        }

    }
}

export default Detail;