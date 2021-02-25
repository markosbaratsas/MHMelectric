import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import PrivateRoute from './PrivateRoute';
import Login from './Login';
import SignUp from './SignUp';
import Error from './Error';
import Test from './Test';
import { AuthContext } from './context/auth';

function App(props) {
  return (
    <AuthContext.Provider value={false}>
      <Router>
        <Switch>
          <Route exact path='/' component={Login} />
          <Route exact path='/signup' component={SignUp} />
          <PrivateRoute exact path='/test' component={Test} />
          <Route path='*' component={Error} />
        </Switch>
      </Router>
    </AuthContext.Provider>
  );
}

export default App;
