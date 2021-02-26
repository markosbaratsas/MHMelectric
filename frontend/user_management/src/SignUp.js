import './Login.css';
import React, { useState } from 'react';
import { Link, Redirect } from 'react-router-dom';
import Header from './Header';
import axios from 'axios';
import { useAuth } from "./context/auth";

function SignUp() {
    // const history = useHistory()
    const [isLoggedIn, setLoggedIn] = useState(false)
    const [ user, setUser] = useState({})
    const { setAuthTokens } = useAuth()

    const handleChange = (e) => {
        const { value, name } = e.target
        setUser({...user, [name]: value})
        // console.log(user)
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        var details = {
            method: 'post',
            url: 'http://127.0.0.1:8765/evcharge/api/register',
            data: user,
        }
        axios(details)
            .then( (response) => {
                // console.log(response.data)
                setAuthTokens(response.data);
                setLoggedIn(true);
            })
            .catch( (error) => {
                console.log(error)
            })
    }

    if (isLoggedIn) {
        return <Redirect to="/test" />;
    }

    return (  
        <>
            <Header />
            <div className='App'>
                <div className='login'>
                    <form onSubmit={handleSubmit}>
                        <div className='input-div'>
                            <h3>username*</h3>
                            <input type='username' name='username' id='username' onChange={handleChange} required />
                        </div>
                        <div className='input-div'>
                            <h3>email*</h3>
                            <input type='email' name='email' id='email' onChange={handleChange} required />
                        </div>
                        <div className='input-div'>
                            <h3>password*</h3>
                            <input type='password' name='password' id='password' onChange={handleChange} required />
                        </div>
                        <div className='input-div'>
                            <h3>repeat password*</h3>
                            <input type='password' name='password2' id='password2' onChange={handleChange} required />
                        </div>
                        <button type='submit' className='basic-button'>Sign up</button>
                        <h4>Already have an account yet? <Link to='/' className='link'>Log in</Link></h4>
                    </form>
                </div>
            </div>
        </>
    );
}

export default SignUp;