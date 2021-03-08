import './css/Login.css';
import './css/Header.css';
import './css/Profile.css';
import Profile from './Profile';
import Car from './Car';
import { Link } from 'react-router-dom';

function Test() {

  return (
    <>
    <div className="background-wrapper">
      <nav>
        <div className="nav-wrapper">
          <a href="#!" className="brand-logo center">MHMelectric</a>
          <ul className="left hide-on-med-and-down">
            <li className="active"><a href="/account">Account</a></li>
            <li><Link to='/bill'>Periodic Bill</Link></li>
            <li><a href="#!">Previous Charges</a></li>
            <li><a href="#!">Charge</a></li>
          </ul>
        </div>
      </nav>
      <div className='profile-wrapper'>
        <Profile />
        <Car />
      </div>
      </div>
    </>
  );
}

export default Test;