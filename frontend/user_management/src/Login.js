import './Login.css'
import React, { useState } from 'react';
import { Link, Redirect } from 'react-router-dom';
import Header from './Header';
import axios from 'axios';
import { useAuth } from "./context/auth";

function Login(props) {
    // const history = useHistory()
    const [isLoggedIn, setLoggedIn] = useState(false)
    const [user, setUser] = useState({})
    const { setAuthTokens } = useAuth()
    // const referer = props.location.state.referer || '/'

    const handleChange = (e) => {
        const { value, name } = e.target
        setUser({...user, [name]: value})
        // console.log(user)
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        var details = {
            method: 'post',
            url: 'http://127.0.0.1:8765/evcharge/api/login',
            data: user,
        }
        axios(details)
            .then( (response) => {
                // console.log(response.data);
                setAuthTokens(response.data);
                setLoggedIn(true);
            })
            .catch( (error) => {
                console.log(error)
            })
    }

    if (isLoggedIn) {
        // return <Redirect to={referer} />
        return <Redirect to='/test' />
    }

    return (
        <>
        <Header />
        <div className='App'>
            <div className='login'>
                <h1>Welcome! Please log in to continue.</h1>
                <form onSubmit={handleSubmit}>
                    <div className='input-div'>
                        <h3>username*</h3>
                        <input type='username' name='username' id='username' onChange={handleChange} required />
                    </div>
                    <div className='input-div'>
                        <h3>password*</h3>
                        <input type='password' name='password' id='password' onChange={handleChange} required />
                    </div>
                    <button type='submit' className='basic-button'>Log in</button>
                </form>
                <h4>Don't have an account yet? <Link to='/signup' className='link'>Sign up</Link></h4>
            </div>
            {/* <h1>{user.password}</h1> */}
        </div>
        </>
    );
}

export default Login;
