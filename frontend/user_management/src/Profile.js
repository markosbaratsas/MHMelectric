import './css/Login.css'
import './css/Header.css'
import { useAuth } from './context/auth'
import React, { useState, useEffect } from 'react'
import axios from 'axios'
import profile from './images/profile-pic.png'

function Profile() {
    const { setAuthTokens } = useAuth();
    const [ user, setUser ] = useState({})

    function logOut() {
        localStorage.clear();
        setAuthTokens();
    }

    useEffect(() => {
        if (localStorage.getItem("username")===null) {
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
                localStorage.setItem("owner_id", response.data["car_owner"]["owner_id"])
                localStorage.setItem("first_name", response.data["car_owner"]["first_name"])
                localStorage.setItem("last_name", response.data["car_owner"]["last_name"])
                localStorage.setItem("birthdate", response.data["car_owner"]["birthdate"].substring(0, 10))
                localStorage.setItem("country", response.data["car_owner"]["country"])
                localStorage.setItem("city", response.data["car_owner"]["city"])
                localStorage.setItem("street", response.data["car_owner"]["street"])
                localStorage.setItem("street_number", response.data["car_owner"]["street_number"])
                localStorage.setItem("postal_code", response.data["car_owner"]["postal_code"])
                localStorage.setItem("bonus_points", response.data["car_owner"]["bonus_points"])
                setUser({"username": localStorage["username"], "email": localStorage["email"], "first_name": localStorage["first_name"], 
                "last_name": localStorage["last_name"], "birthdate": localStorage["birthdate"], 
                "country": localStorage["country"], "city": localStorage["city"], "street": localStorage["street"], 
                "street_number": localStorage["street_number"], "postal_code": localStorage["postal_code"], "bonus_points": localStorage["bonus_points"]})
                })
                .catch( (error) => {
                    console.log(error)
                })
        } else {
            setUser({"username": localStorage["username"], "email": localStorage["email"], "first_name": localStorage["first_name"], 
                "last_name": localStorage["last_name"], "birthdate": localStorage["birthdate"], 
                "country": localStorage["country"], "city": localStorage["city"], "street": localStorage["street"], 
                "street_number": localStorage["street_number"], "postal_code": localStorage["postal_code"], "bonus_points": localStorage["bonus_points"]})
        }
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