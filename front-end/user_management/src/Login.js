import './css/Login.css'
import React, { useEffect, useState } from 'react';
import { Link, Redirect } from 'react-router-dom';
import Header from './Header';
import axios from 'axios';
import { useAuth } from "./context/auth";

function Login(props) {
    const [isLoggedIn, setLoggedIn] = useState(false)
    const [user, setUser] = useState({})
    const { setAuthTokens } = useAuth()

    const handleChange = (e) => {
        const { value, name } = e.target
        setUser({...user, [name]: value})
        // console.log(user)
    }

    useEffect(() => {
        if(localStorage.getItem("username")!==null) setLoggedIn(true)
    }, [])

    const handleSubmit = (e) => {
        e.preventDefault()
        var details = {
            method: 'post',
            url: 'http://127.0.0.1:8765/evcharge/api/login',
            data: user,
        }
        axios(details)
            .then( (response) => {
                setAuthTokens(response.data["token"]);
                setLoggedIn(true);
            })
            .catch( (error) => {
                console.log(error)
                alert("Invalid credentials")
            })
    }

    if (isLoggedIn) {
        return <Redirect to='/account'/>
    }

    return (
        <>
        <Header />
        <div className='background-wrapper'>
            <div className='App'>
                <div className='login'>
                    <h1>Welcome! Please log in to continue.</h1>
                    <form onSubmit={handleSubmit}>
                        <div className='input-div'>
                            <input placeholder='username*' type='text' name='username' onChange={handleChange} required />
                        </div>
                        <div className='input-div'>
                            <input placeholder='password*' type='password' name='password' onChange={handleChange} required />
                        </div>
                        <button type='submit' className='basic-button waves-effect waves-light btn'>Log in</button>
                    </form>
                    <h4>Don't have an account yet? <Link to='/signup' className='link'>Sign up</Link></h4>
                </div>
            </div>
        </div>
        </>
    );
}

export default Login;
