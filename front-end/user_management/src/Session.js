import './css/Login.css';
import './css/Header.css';
import './css/Profile.css';
import { Link } from 'react-router-dom';
import Select from './Select'

function Session() {

    return (
        <>
        <div className="background-wrapper">
        <nav>
            <div className="nav-wrapper">
            <a href="#!" className="brand-logo center">MHMelectric</a>
            <ul className="left hide-on-med-and-down">
                <li><a href="/account">Account</a></li>
                <li><Link to='/bill'>Periodic Bill</Link></li>
                <li className="active"><Link to='/charge'>Charge</Link></li>
            </ul>
            </div>
        </nav>
        <div className='profile-wrapper'>
            <div className='profile-div'>
                <div className='profile-center'>
                    <h3>Create a charge session</h3>
                    <hr />
                </div>
                <Select/>
            </div>
        </div>
        </div>
        </>
    );
}

export default Session;