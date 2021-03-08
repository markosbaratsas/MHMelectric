import './css/Login.css';
import './css/Header.css';
import './css/Profile.css';
import { Link } from 'react-router-dom';

function Bill() {

  return (
    <>
    <div className="background-wrapper">
      <nav>
        <div className="nav-wrapper">
          <a href="#!" className="brand-logo center">MHMelectric</a>
          <ul className="left hide-on-med-and-down">
            <li><a href="/account">Account</a></li>
            <li className="active"><Link to='/bill'>Periodic Bill</Link></li>
            <li><a href="#!">Previous Charges</a></li>
            <li><a href="#!">Charge</a></li>
          </ul>
        </div>
      </nav>
      <div className='profile-wrapper'>
        <div className='profile-div'>
          <div className='profile-center'>
            <button className='basic-button waves-effect waves-light btn'>Pay bill</button>
          </div>
        </div>
      </div>
    </div>
    </>
  );
}

export default Bill;