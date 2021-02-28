import './Login.css'
import './Header.css'
import { useAuth } from './context/auth'
// import React, { useState, useEffect } from 'react'
// import axios from 'axios'
import profile from './context/profile-pic.png'

function Profile() {
    const { setAuthTokens } = useAuth();
    const user = {"username": localStorage["username"], "email": localStorage["email"], "first_name": localStorage["first_name"], 
                    "last_name": localStorage["last_name"], "birthdate": localStorage["birthdate"], 
                    "country": localStorage["country"], "city": localStorage["city"], "street": localStorage["street"], 
                    "street_number": localStorage["street_number"], "postal_code": localStorage["postal_code"], "bonus_points": localStorage["bonus_points"]}

    function logOut() {
        setAuthTokens();
    }

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