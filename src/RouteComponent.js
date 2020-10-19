import React from 'react';
import { Route } from 'react-router';
import PropTypes from 'prop-types';

const RouteComponent = props => {
  const { component: Component, ...rest } = props;
  return (
    <Route
      {...rest}
      render={matchProps => (
        <div>
          <Component {...matchProps} />
        </div>
      )}
    />
  );
};

RouteComponent.propTypes = {
  component: PropTypes.any.isRequired,
  path: PropTypes.string
};

export default RouteComponent;