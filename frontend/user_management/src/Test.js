import './Login.css'
import './Header.css'
import { useAuth } from './context/auth'

function Test() {
    const { setAuthTokens } = useAuth();
    const username = localStorage.getItem("username")

    function logOut() {
        setAuthTokens();
    }

  return (
    <>
      <nav>
        <div className="nav-wrapper">
          <a href="#!" className="brand-logo center">MHMelectric</a>
          <ul className="left hide-on-med-and-down">
            <li className="active"><a href="#!">Home</a></li>
            <li><a href="#!">Periodic Bill</a></li>
            <li><a href="#!">Previous Charges</a></li>
            <li><a href="#!">Charge</a></li>
          </ul>
        </div>
      </nav>
      <div className='App'>
        <div className='login'>
          <h1>Hello {username}</h1>
        </div>
        <button onClick={logOut} className='basic-button waves-effect waves-light btn'>Log out</button>
      </div>
    </>
  );
}

export default Test;