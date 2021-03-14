import './css/Login.css'
import './css/Header.css'
import React, { useState, useEffect } from 'react'
import axios from 'axios'
import Modal from 'react-modal'

function Car() {
    const [ car, setCar ] = useState([])
    const [ modalIsOpen, setModalIsOpen ] = useState(false)
    const [ carAdd, setCarAdd ] = useState({})

    function openModal() {
        setModalIsOpen(true)
        setCarAdd({})
    }

    const modalStyle = {
        overlay: {
          position: 'fixed',
          backdropFilter: 'blur(3px)',
          backgroundColor: 'rgba(255, 255, 255, 0.1)'
        },
        content: { 
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

    const handleChangeCar = (e) => {
        const { value, name } = e.target
        setCarAdd({...carAdd, [name]: value})
        console.log(carAdd)
    }

    function submitCar() {
        var details = {
            method: 'post',
            url: 'http://172.105.248.124:8765/evcharge/api/add_car',
            headers: {
            'X-OBSERVATORY-AUTH': JSON.parse(localStorage["tokens"])
            },
            data: carAdd
        }
        axios(details)
            .catch( (error) => {
                alert(error)
                console.log(error)
            })
    }

    useEffect(() => {
        var details = {
            method: 'get',
            url: 'http://172.105.248.124:8765/evcharge/api/get_car_info_from_user',
            headers: {
            'X-OBSERVATORY-AUTH': JSON.parse(localStorage["tokens"])
            }
        }
        axios(details)
            .then( (response) => {
                setCar(response.data["cars"])
                localStorage.setItem("cars", JSON.stringify(response.data["cars"]))
            })
            .catch( (error) => {
                console.log(error)
            })
    }, [])

    return (
        <>
            <div className='profile-div'>
                <h3>Your cars</h3>
            <hr />
            {car.map( (car) => 
                <>
                <div className='profile-left'>
                    <div className="car-div">
                        <h2>Brand:</h2>
                        <h1>   {car["brand"]}</h1>
                    </div>
                    <div className="car-div">
                        <h2>Type:</h2>
                        <h1>{car["car_type"]}</h1>
                    </div>
                    <div className="car-div">
                        <h2>Model:</h2>
                        <h1>{car["car_model"]}</h1>
                    </div>
                    <div className="car-div">
                        <h2>Release year:</h2>
                        <h1>{car["release_year"]}</h1>
                    </div>
                    <div className="car-div">
                        <h2>Variant:</h2>
                        <h1>{car["variant"]}</h1>
                    </div>
                    <div className="car-div">
                        <h2>Usable battery size:</h2>
                        <h1>{car["usable_battery_size"]}</h1>
                    </div>
                </div>
                <hr />
            </>
            )}
            <div className='profile-center'>
                <button onClick={openModal} className='basic-button waves-effect waves-light btn'>Add car</button>
            </div>
        </div>

        <Modal isOpen={modalIsOpen} onRequestClose={() => setModalIsOpen(false)} style={modalStyle}>
        <form className='profile-div inside-modal-div' onSubmit={submitCar}>
                <div className='profile-center'>
                    <h3>Type the information of your car</h3>
                    <hr />
                </div>
                <div className='modal-row first'>
                    <div className='modal-input-div'>
                        <label htmlFor="brand">Type brand*:</label>
                        <input type='brand' name='brand' className='input-city-select modal-input-div' onChange={handleChangeCar} required />
                    </div>
                </div>
                <div className='modal-row'>
                    <div className='modal-input-div'>
                        <label htmlFor="car_type">Type type*:</label>
                        <input type='car_type' name='car_type' className='input-city-select modal-input-div' onChange={handleChangeCar} required />
                    </div>
                </div>
                <div className='modal-row'>
                    <div className='modal-input-div'>
                        <label htmlFor="car_model">Type model*:</label>
                        <input type='car_model' name='car_model' className='input-city-select modal-input-div' onChange={handleChangeCar} required />
                    </div>
                </div>
                <div className='modal-row'>
                    <div className='modal-input-div'>
                        <label htmlFor="variant">Type variant*:</label>
                        <input type='variant' name='variant' className='input-city-select modal-input-div' onChange={handleChangeCar} required />
                    </div>
                </div>
                <div className='modal-row'>
                    <div className='modal-input-div left'>
                        <label htmlFor="release_year">Type release year*:</label>
                        <input type='number' name='release_year' className='input-city-select modal-input-div' onChange={handleChangeCar} required />
                    </div>                
                    <div className='modal-input-div'>
                        <label htmlFor="usable_battery_size">Type usable battery size:</label>
                        <input type='number' name='usable_battery_size' className='input-city-select modal-input-div' onChange={handleChangeCar}/>
                    </div>
                </div>
                <div className='profile-center'>
                    <button type='submit' className='basic-button waves-effect waves-light btn modal-btn'>Add car</button>
                </div>
            </form>             
        </Modal>
        </>
    );
}

export default Car;