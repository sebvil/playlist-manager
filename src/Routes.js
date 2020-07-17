import React from 'react';
import { Switch, Redirect } from 'react-router';
import Login from "./screens/login";
import Home from "./screens/home";
import RouteComponent from "./RouteComponent";

const Routes = () => {
  return (
    <Switch>
      <Redirect
        exact
        from="/"
        to="/login"
      />

      <RouteComponent
        component={Login}
        path="/login"
      />

      <RouteComponent
        component={Home}
        path="/home"
      />
    </Switch>
  );
};

export default Routes;