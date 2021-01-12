import './Login.css'
import React, { useState } from 'react'
import { useHistory } from 'react-router-dom'
import Header from './Header'
import axios from 'axios'

function SignUp() {
    const history = useHistory()
    const [ user, setUser] = useState({})

    function handleClick() {
        history.push('/')
    }

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
                console.log(response.data)
            })
            .catch( (error) => {
                console.log(error)
            })
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
                    <h4>Already have an account yet? <button className='link' onClick={handleClick}>Log in</button></h4>
                </form>
            </div>
        </div>
    </>
  );
}

export default SignUp;