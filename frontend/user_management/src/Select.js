import './css/Login.css';
import './css/Header.css';
import './css/Profile.css';
import React, { useState, useEffect } from 'react';
import axios from 'axios'

function Select() {
    const [ dataPost, setDataPost ] = useState({})
    const [ car, setCar ] = useState([])
    const [ station, setStation ] = useState([])
    const [ point, setPoint ] = useState([])
    const [ bill, setBill ] = useState([])
    const [ chargeProgram, setChargeProgram ] = useState([])
    const [ provider, setProvider ] = useState([])
    const [ city, setCity ] = useState()

    const handleChange = (e) => {
        const { value, name } = e.target
        setDataPost({...dataPost, [name]: value})
        console.log(dataPost)
    }

    const handleChangeInt = (e) => {
        const { value, name } = e.target
        setDataPost({...dataPost, [name]: parseInt(value)})
    }

    const handleChangeCity = (e) => {
        const { value } = e.target
        setCity(value)
    }

    const handleChangeStation = (e) => {
        const { value, name } = e.target
        setDataPost({...dataPost, [name]: parseInt(value)})
        setPoint([])
        var details = {
            method: 'get',
            url: 'http://127.0.0.1:8765/evcharge/api/get_charging_points_from_station/'+value,
            headers: {
            'X-OBSERVATORY-AUTH': JSON.parse(localStorage["tokens"])
            }
        }
        axios(details)
            .then( (response) => {
                setPoint(response.data["charging_points"])
                setDataPost({...dataPost, 'charging_point': response.data["charging_points"][0]['charging_point_id']})
            })
            .catch( (error) => {
                console.log(error)
            })
    }

    function searchStation() {
        setPoint([])
        setStation([])
        var details = {
            method: 'get',
            url: 'http://127.0.0.1:8765/evcharge/api/get_stations_from_city/'+city,
            headers: {
            'X-OBSERVATORY-AUTH': JSON.parse(localStorage["tokens"])
            }
        }
        axios(details)
            .then( (response) => {
                setStation(response.data["stations"])
                setDataPost({...dataPost, 'station': response.data["stations"][0]['station_id']})
            })
            .catch( (error) => {
                console.log(error)
            })
    }

    function sendPost() {
        console.log(dataPost)
        var details = {
            method: 'post',
            url: 'http://127.0.0.1:8765/evcharge/api/add_session',
            headers: {
            'X-OBSERVATORY-AUTH': JSON.parse(localStorage["tokens"])
            },
            data: dataPost
        }
        axios(details)
            .then( (response) => {
                console.log(response.data)
                alert(response.data["response"])
                window.location.reload(false)
            })
            .catch( (error) => {
                console.log(error)
            })
    }

    useEffect(() => {
        setCar(JSON.parse(localStorage.getItem("cars")))
        if(JSON.parse(localStorage.getItem("cars")).length!==0) setDataPost({'car_owner': JSON.parse(localStorage.getItem('owner_id')), 'car': parseInt(JSON.parse(localStorage.getItem("cars"))[0]['car_id'])})
        if (localStorage.getItem("bill")===null) {
            var details = {
                method: 'get',
                url: 'http://127.0.0.1:8765/evcharge/api/get_periodic_bills_of_user',
                headers: {
                'X-OBSERVATORY-AUTH': JSON.parse(localStorage["tokens"])
                }
            }
            axios(details)
                .then( (response) => {
                setBill(response.data["periodic_bills"])
                localStorage.setItem("bill", JSON.stringify(response.data["periodic_bills"]))
                })
                .catch( (error) => {
                    console.log(error)
                })
        } else {
          setBill(JSON.parse(localStorage.getItem("bill")))
        }
        if (localStorage.getItem("charge_programs")===null) {
            details = {
                method: 'get',
                url: 'http://127.0.0.1:8765/evcharge/api/get_charge_programs',
                headers: {
                'X-OBSERVATORY-AUTH': JSON.parse(localStorage["tokens"])
                }
            }
            axios(details)
                .then( (response) => {
                setChargeProgram(response.data["charge_programs"])
                localStorage.setItem("charge_programs", JSON.stringify(response.data["charge_programs"]))
                })
                .catch( (error) => {
                    console.log(error)
                })
        } else {
          setChargeProgram(JSON.parse(localStorage.getItem("charge_programs")))
        }
        if (localStorage.getItem("providers")===null) {
            details = {
                method: 'get',
                url: 'http://127.0.0.1:8765/evcharge/api/get_providers',
                headers: {
                'X-OBSERVATORY-AUTH': JSON.parse(localStorage["tokens"])
                }
            }
            axios(details)
                .then( (response) => {
                setProvider(response.data["providers"])
                localStorage.setItem("providers", JSON.stringify(response.data["providers"]))
                })
                .catch( (error) => {
                    console.log(error)
                })
        } else {
            setProvider(JSON.parse(localStorage.getItem("providers")))
        }
    }, [])

    return (
        <>
            <label htmlFor="car">Choose car:</label>
            <select name="car" id="car" onChange={handleChangeInt} className='select-div'>
                <option disabled selected value>-</option>
                {car.map( (car) => 
                <option value={car['car_id']}>{car["brand"]}, {car["type"]}, {car["model"]}, {car["release_year"]}</option>)}
            </select>
            <label htmlFor="city">Choose city:</label>
            <div className='input-city'>
                <input placeholder='Type city' type='city' name='city' id='city' onChange={handleChangeCity} className='input-city-select' required />
                <button className='basic-button waves-effect waves-light btn city-button' onClick={searchStation}>Search stations</button>
            </div>
            <label htmlFor="station">Choose station:</label>
            <select name="station" id="station" className='select-div' onChange={handleChangeStation}>
                <option disabled selected value>-</option>
                {station.map( (station) => 
                <option value={station['station_id']}>{station["street"]} {station["street_number"]}, {station["postal_code"]}, {station["city"]}, {station["country"]}</option>)}
            </select>
            <label htmlFor="charging_point">Choose charging point:</label>
            <select name="charging_point" id="charging_point" onChange={handleChangeInt} className='select-div'>
                <option disabled selected value>-</option>
                {point.map( (point) => 
                <option value={point['charging_point_id']}>{point['charging_point_id_given']}</option>)}
            </select>
            <label htmlFor="periodic_bill">Choose periodic bill:</label>
            <select name="periodic_bill" id="periodic_bill" onChange={handleChangeInt} className='select-div'>
                <option disabled selected value>-</option>
                {bill.map( (bill) => 
                <option value={bill['periodic_bill_id']}>Periodic bill {bill['periodic_bill_id']} published on {bill["published_on"].substring(0, 10)}</option>)}
            </select>
            <label htmlFor="charge_program">Choose charge program:</label>
            <select name="charge_program" id="charge_program" onChange={handleChangeInt} className='select-div'>
                <option disabled selected value>-</option>
                {chargeProgram.map( (chargeProgram) => 
                <option value={chargeProgram['charge_program_id']}>{chargeProgram['description']}, price: {chargeProgram["price"]}‎€, duration: {chargeProgram["duration"]} min</option>)}
            </select>
            <label htmlFor="provider">Choose provider:</label>
            <select name="provider" id="provider" onChange={handleChangeInt} className='select-div'>
                <option disabled selected value>-</option>
                {provider.map( (provider) => 
                <option value={provider['provider_id']}>{provider['title']}</option>)}
            </select>
            <label htmlFor="connection_time">Provide connection time in yy-mm-dd hh:mm:ss format:</label>
            <input placeholder='Type connection time' type='connection_time' name='connection_time' id='connection_time' 
                                    onChange={handleChange} className='input-city-select-width' required />
            <label htmlFor="disconnection_time">Provide disconnection time in yy-mm-dd hh:mm:ss format:</label>
            <input placeholder='Type disconnection time' type='disconnection_time' name='disconnection_time' id='disconnection_time' 
                                    onChange={handleChange} className='input-city-select-width' required />
            <label htmlFor="done_charging_time">Provide done charging time in yy-mm-dd hh:mm:ss format:</label>
            <input placeholder='Type done charging time' type='done_charging_time' name='done_charging_time' id='done_charging_time' 
                                    onChange={handleChange} className='input-city-select-width' required />
            <label htmlFor="user_payment_method">Type payment method:</label>
            <input placeholder='Type payment method' type='user_payment_method' name='user_payment_method' id='user_payment_method' 
                                    onChange={handleChange} className='input-city-select-width' required />
                <div className='profile-right'>
                    <button className='basic-button waves-effect waves-light btn pay' onClick={sendPost}>Charge</button>
                </div>
        </>
    );
}

export default Select;