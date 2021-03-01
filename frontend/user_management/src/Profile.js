import './Login.css'
import './Header.css'
import { useAuth } from './context/auth'
import React, { useState, useEffect } from 'react'
import axios from 'axios'
import profile from './context/profile-pic.png'

function Profile() {
    const { setAuthTokens } = useAuth();
    const [ user, setUser ] = useState({})

    function logOut() {
        localStorage.clear();
        setAuthTokens();
    }

    useEffect(() => {
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
            setUser({"username": response.data["username"], "email": response.data["email"], "first_name": response.data["car_owner"]["first_name"], 
            "last_name": response.data["car_owner"]["last_name"], "birthdate": response.data["car_owner"]["birthdate"].substring(0, 10), 
            "country": response.data["car_owner"]["country"], "city": response.data["car_owner"]["city"], "street": response.data["car_owner"]["street"], 
            "street_number": response.data["car_owner"]["street_number"], "postal_code": response.data["car_owner"]["postal_code"], "bonus_points": response.data["car_owner"]["bonus_points"]})
            console.log(localStorage)
            })
            .catch( (error) => {
                console.log(error)
            })
    }, [])

    return (
        <>
        <div className='profile-div'>
            <div className='profile-center'>
                <img src={profile} alt="profile pic" />
                <h1>{user["username"]}</h1>
            </div>
            <hr />
            <div className='profile-left'>
                <h2> Name</h2>
                <h1>{user["first_name"]} {user["last_name"]}</h1> 
            </div>
            <hr />
            <div className='profile-left'>
                <h2> e-mail</h2>
                <h1>{user["email"]}</h1> 
            </div>
            <hr />
            <div className='profile-left'>
                <h2> Birthdate</h2>
                <h1>{user["birthdate"]}</h1> 
            </div>
            <hr />
            <div className='profile-left'>
                <h2> Address</h2>
                <h1>{user["street"]} {user["street_number"]}, {user["postal_code"]}, {user["city"]}, {user["country"]}</h1> 
            </div>
            <hr />
            <div className='profile-left'>
                <h2> Bonus points</h2>
                <h1>{user["bonus_points"]}</h1> 
            </div>
            <hr />
            <div className='profile-center'>
                <button onClick={logOut} className='basic-button waves-effect waves-light btn'>Log out</button>
            </div>
        </div>
        </>
    );
}

export default Profile;