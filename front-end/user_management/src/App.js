import './materialize/css/materialize.min.css'
import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import PrivateRoute from './PrivateRoute';
import Login from './Login';
import SignUp from './SignUp';
import Error from './Error';
import Test from './Test';
import Bill from './Bill';
import Session from './Session';
import { AuthContext } from './context/auth';

function App(props) {
  const existingTokens = (typeof localStorage.getItem("tokens")==='string' && localStorage.getItem("tokens")==="undefined")
                          ? null : JSON.parse(localStorage.getItem("tokens"))
  const [authTokens, setAuthTokens] = useState(existingTokens);
  
  const setTokens = (data) => {
    localStorage.setItem("tokens", JSON.stringify(data));
    setAuthTokens(data);
  }

  return (
    <div className='total-wrapper'>
      <AuthContext.Provider value={{ authTokens, setAuthTokens: setTokens }}>
        <Router>
          <Switch>
            <Route exact path='/' component={Login} />
            <Route exact path='/signup' component={SignUp} />
            <PrivateRoute exact path='/account' component={Test} />
            <PrivateRoute exact path='/bill' component={Bill} />
            <PrivateRoute exact path='/charge' component={Session} />
            <Route path='*' component={Error} />
          </Switch>
        </Router>
      </AuthContext.Provider>
    </div>
  );
}

export default App;
