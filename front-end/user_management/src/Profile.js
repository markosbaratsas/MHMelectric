import './css/Login.css'
import './css/Header.css'
import { useAuth } from './context/auth'
import React, { useState, useEffect } from 'react'
import axios from 'axios'
import profile from './images/profile-pic.png'
import Modal from 'react-modal'

function Profile() {
    const { setAuthTokens } = useAuth();
    const [ user, setUser ] = useState({})
    const [ modalIsOpen, setModalIsOpen ] = useState(false)
    const [ userEdit, setUserEdit ] = useState({})

    function logOut() {
        localStorage.clear();
        setAuthTokens();
    }

    function submitUser() {
        var details = {
            method: 'post',
            url: 'http://127.0.0.1:8765/evcharge/api/change_user_info',
            headers: {
            'X-OBSERVATORY-AUTH': JSON.parse(localStorage["tokens"])
            },
            data: {...userEdit, "birthdate": userEdit["birthdate"] + ' 00:00:00'}
        }
        axios(details)
            .catch( (error) => {
                alert(error)
                console.log(error)
            })
    }

    const modalStyle = {
        overlay: {
            position: 'fixed',
            backdropFilter: 'blur(3px)',
            backgroundColor: 'rgba(255, 255, 255, 0.1)'
        },
        content: { 
            opacity: '1',
            maxHeight: '76%',
            overflowY: 'auto',
            top: '12%',
            left: '33%',
            right: 'auto',
            bottom: 'auto',
            position: 'absolute', 
            width: '34%', 
            borderWidth: '1px',
            paddingLeft: '30px',
            paddingTop: '0px'
        }}

    function openModal() {
        setUserEdit(user)
        setModalIsOpen(true)
    }

    const handleChangeUser = (e) => {
        const { value, name } = e.target
        setUserEdit({...userEdit, [name]: value})
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
            <div className='profile-center account-buttons'>
                <button onClick={openModal} className='basic-button waves-effect waves-light btn edit'>Edit account</button>
                <button onClick={logOut} className='basic-button waves-effect waves-light btn'>Log out</button>
            </div>
        </div>

        <Modal isOpen={modalIsOpen} onRequestClose={() => setModalIsOpen(false)} style={modalStyle}>
            <form className='profile-div inside-modal-div' onSubmit={submitUser}>
                <div className='profile-center'>
                    <h3>Type the information you want to edit</h3>
                    <hr />
                </div>
                <div className='modal-row first'>
                    <div className='modal-input-div left'>
                        <label htmlFor="first_name">Edit first name:</label>
                        <input type='first_name' value={userEdit["first_name"]} name='first_name' className='input-city-select modal-input-div' onChange={handleChangeUser} required />
                    </div>
                    <div className='modal-input-div'>
                        <label htmlFor="first_name">Edit last name:</label>
                        <input type='last_name' value={userEdit["last_name"]} name='last_name' className='input-city-select modal-input-div' onChange={handleChangeUser} required />
                    </div>
                </div>
                <div className='modal-row'>
                    <div className='modal-input-div'>
                        <label htmlFor="email">Edit email:</label>
                        <input type='email2' value={userEdit["email"]} name='email' className='input-city-select modal-input-div' onChange={handleChangeUser} required />
                    </div>
                </div>
                <div className='modal-row'>
                    <div className='modal-input-div'>
                        <label htmlFor="birthdate">Edit birthdate:</label>
                        <input type='date' value={userEdit["birthdate"]} name='birthdate' className='input-city-select input-city-select-width' onChange={handleChangeUser} required />
                    </div>
                </div>
                <div className='modal-row'>
                    <div className='modal-input-div left street'>
                        <label htmlFor="street">Edit street name:</label>
                        <input type='street' value={userEdit["street"]} name='street' className='input-city-select modal-input-div' onChange={handleChangeUser} required />
                    </div>
                     <div className='modal-input-div left'>
                        <label htmlFor="street_number">Edit street number:</label>
                        <input type='number' value={userEdit["street_number"]} name='street_number' className='input-city-select modal-input-div' onChange={handleChangeUser} required />
                    </div>
                    <div className='modal-input-div'>
                        <label htmlFor="postal_code">Edit postal code:</label>
                        <input type='number' value={userEdit["postal_code"]} name='postal_code' className='input-city-select modal-input-div' onChange={handleChangeUser} required />
                    </div>
                </div>
                <div className='modal-row'>
                    <div className='modal-input-div left'>
                        <label htmlFor="city">Edit city:</label>
                        <input type='city' value={userEdit["city"]} name='city' className='input-city-select modal-input-div' onChange={handleChangeUser} required />
                    </div>
                    <div className='modal-input-div'>
                        <label htmlFor="country">Edit country:</label>
                        <input type='country' value={userEdit["country"]} name='country' className='input-city-select modal-input-div' onChange={handleChangeUser} required />
                    </div>
                </div>
                <div className='profile-center'>
                    <button type='submit' className='basic-button waves-effect waves-light btn modal-btn'>Submit changes</button>
                </div>
            </form>                
       </Modal>
        </>
    );
}

export default Profile;