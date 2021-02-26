import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import PrivateRoute from './PrivateRoute';
import Login from './Login';
import SignUp from './SignUp';
import Error from './Error';
import Test from './Test';
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
    <AuthContext.Provider value={{ authTokens, setAuthTokens: setTokens }}>
      {console.log(typeof localStorage.getItem("tokens"))}
      {console.log(localStorage.getItem("tokens"))}
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
