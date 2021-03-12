import './css/Login.css'
import './css/Header.css'
import React, { useState, useEffect } from 'react'
import axios from 'axios'

function Car() {
    const [ car, setCar ] = useState([])



    useEffect(() => {
        if (localStorage.getItem("cars")===null) {
            var details = {
                method: 'get',
                url: 'http://127.0.0.1:8765/evcharge/api/get_car_info_from_user',
                headers: {
                'X-OBSERVATORY-AUTH': JSON.parse(localStorage["tokens"])
                }
            }
            axios(details)
                .then( (response) => {
                    console.log(response.data)
                    setCar(response.data["cars"])
                    localStorage.setItem("cars", JSON.stringify(response.data["cars"]))
                })
                .catch( (error) => {
                    console.log(error)
                })
        } else {
            setCar(JSON.parse(localStorage.getItem("cars")))
        }
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
        </div>
        </>
    );
}

export default Car;