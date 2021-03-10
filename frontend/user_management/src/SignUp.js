import './css/Login.css';
import React, { useState, useEffect } from 'react';
import { Link, Redirect } from 'react-router-dom';
import Header from './Header';
import axios from 'axios';
import { useAuth } from "./context/auth";

function SignUp() {
    const [isLoggedIn, setLoggedIn] = useState(false)
    const [ user, setUser] = useState({})
    const { setAuthTokens } = useAuth()

    useEffect(() => {
        if(localStorage.getItem("username")!==null) setLoggedIn(true)
    }, [])

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
            <div className='background-wrapper'>
                <div className='App'>
                    <div className='login'>
                        <form onSubmit={handleSubmit}>
                            <div className='input-div'>
                                <input placeholder='username*' type='text' name='username' id='username' onChange={handleChange} required />
                            </div>
                            <div className='input-div'>
                                <input placeholder='email*' type='email' name='email' id='email' onChange={handleChange} required />
                            </div>
                            <div className='input-div'>
                                <input placeholder='password*' type='password' name='password' id='password' onChange={handleChange} required />
                            </div>
                            <div className='input-div'>
                                <input placeholder='repeat password*' type='password' name='password2' id='password2' onChange={handleChange} required />
                            </div>
                            <button type='submit' className='basic-button waves-effect waves-light btn'>Sign up</button>
                            <h4>Already have an account yet? <Link to='/' className='link'>Log in</Link></h4>
                        </form>
                    </div>
                </div>
            </div>
        </>
    );
}

export default SignUp;