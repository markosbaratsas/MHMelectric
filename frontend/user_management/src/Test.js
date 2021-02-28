import './Login.css'
import './Header.css'
import './Profile.css'
import Profile from './Profile';

function Test() {

  return (
    <>
      <nav>
        <div className="nav-wrapper">
          <a href="#!" className="brand-logo center">MHMelectric</a>
          <ul className="left hide-on-med-and-down">
            <li className="active"><a href="/account">Account</a></li>
            <li><a href="#!">Periodic Bill</a></li>
            <li><a href="#!">Previous Charges</a></li>
            <li><a href="#!">Charge</a></li>
          </ul>
        </div>
      </nav>
      <div className='profile-wrapper'>
        <Profile />
      </div>
    </>
  );
}

export default Test;