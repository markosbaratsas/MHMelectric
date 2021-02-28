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
                setAuthTokens(response.data["token"]);
                setLoggedIn(true);


                var details = {
                    method: 'get',
                    url: 'http://127.0.0.1:8765/evcharge/api/get_user_info',
                    headers: {
                      'X-OBSERVATORY-AUTH': JSON.parse(localStorage["tokens"])
                    }
                  }
                axios(details)
                    .then( (response) => {
                    console.log(response.data)
                    localStorage.setItem("username", response.data["username"])
                    localStorage.setItem("email", response.data["email"])
                    localStorage.setItem("first_name", response.data["car_owner"]["first_name"])
                    localStorage.setItem("last_name", response.data["car_owner"]["last_name"])
                    localStorage.setItem("birthdate", response.data["car_owner"]["birthdate"])
                    localStorage.setItem("country", response.data["car_owner"]["country"])
                    localStorage.setItem("city", response.data["car_owner"]["city"])
                    localStorage.setItem("street", response.data["car_owner"]["street"])
                    localStorage.setItem("street_number", response.data["car_owner"]["street_number"])
                    localStorage.setItem("postal_code", response.data["car_owner"]["postal_code"])
                    localStorage.setItem("bonus_points", response.data["car_owner"]["bonus_points"])
                    console.log(localStorage)
                    })
                    .catch( (error) => {
                        console.log(error)
                    })



            })
            .catch( (error) => {
                console.log(error)
            })
    }

    if (isLoggedIn) {
        // return <Redirect to={referer} />
        return <Redirect to='/home' value='hey'/>
    }

    return (
        <>
        <Header />
        <div className='App'>
            <div className='login'>
                <h1>Welcome! Please log in to continue.</h1>
                <form onSubmit={handleSubmit}>
                    <div className='input-div'>
                        <input placeholder='username*' type='text' name='username' id='username' onChange={handleChange} required />
                    </div>
                    <div className='input-div'>
                        <input placeholder='password*' type='password' name='password' id='password' onChange={handleChange} required />
                    </div>
                    <button type='submit' className='basic-button waves-effect waves-light btn'>Log in</button>
                </form>
                <h4>Don't have an account yet? <Link to='/signup' className='link'>Sign up</Link></h4>
            </div>
        </div>
        </>
    );
}

export default Login;
