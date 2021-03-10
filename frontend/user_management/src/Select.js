import './css/Login.css';
import './css/Header.css';
import './css/Profile.css';
import React, { useState, useEffect } from 'react';
import axios from 'axios'

function Select() {
    const [ data, setData ] = useState({})
    const [ car, setCar ] = useState([])
    const [ station, setStation ] = useState([])
    const [ point, setPoint ] = useState([])
    const [ bill, setBill ] = useState([])
    const [ chargeProgram, setChargeProgram ] = useState([])
    const [ provider, setProvider ] = useState([])
    const [ city, setCity ] = useState()

    const handleChange = (e) => {
        const { value, name } = e.target
        setData({...data, [name]: value})
        console.log(data)
    }

    const handleChangeInt = (e) => {
        const { value, name } = e.target
        setData({...data, [name]: parseInt(value)})
    }

    const handleChangeCity = (e) => {
        const { value } = e.target
        setCity(value)
    }

    const handleChangeStation = (e) => {
        const { value, name } = e.target
        setData({...data, [name]: parseInt(value)})
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
                setData({...data, 'charging_point': response.data["charging_points"][0]['charging_point_id']})
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
                setData({...data, 'station': response.data["stations"][0]['station_id']})
            })
            .catch( (error) => {
                console.log(error)
            })
    }

    function sendPost() {
        var details = {
            method: 'post',
            url: 'http://127.0.0.1:8765/evcharge/api/add_session/'+city,
            headers: {
            'X-OBSERVATORY-AUTH': JSON.parse(localStorage["tokens"])
            },
            data: {
                'car': '',
                'car_owner': '',
                'charging_point': '',
                'station': '',
                'periodic_bill': '',
                'charge_program': '',
                'provider': '',
                'connection_time': '',
                'disconnection_time': '',
                'done_charging_time': '',
                'user_payment_method': '',
            }
        }
        axios(details)
            .then( (response) => {
                alert(response.data)
            })
            .catch( (error) => {
                console.log(error)
            })
    }

    useEffect(() => {
        setCar(JSON.parse(localStorage.getItem("cars")))
        setData({...data, 'car': parseInt(JSON.parse(localStorage.getItem("cars"))[0]['car_id'])})
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
                setData({...data, 'periodic_bill': response.data["periodic_bills"][0]['periodic_bill_id']})
                })
                .catch( (error) => {
                    console.log(error)
                })
        } else {
          setBill(JSON.parse(localStorage.getItem("bill")))
          setData({...data, 'periodic_bill': JSON.parse(localStorage.getItem("bill"))[0]['periodic_bill_id']})
        }
        // if (localStorage.getItem("charge_programs")===null) {
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
                setData({...data, 'charge_program': response.data["charge_programs"][0]['charge_program_id']})
                })
                .catch( (error) => {
                    console.log(error)
                })
        // } else {
        //   setChargeProgram(JSON.parse(localStorage.getItem("charge_programs")))
        //   setData({...data, 'charge_program': JSON.parse(localStorage.getItem("charge_programs"))[0]['charge_program_id']})
        // }
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
                setData({...data, 'provider': response.data["providers"][0]['provider_id']})
                })
                .catch( (error) => {
                    console.log(error)
                })
        } else {
            setProvider(JSON.parse(localStorage.getItem("providers")))
            setData({...data, 'provider': JSON.parse(localStorage.getItem("providers"))[0]['provider_id']})
        }
        // setData({'provider': JSON.parse(localStorage.getItem("providers"))[0]['provider_id'], 
        //             'charge_program': JSON.parse(localStorage.getItem("charge_programs"))[0]['charge_program_id'], 
        //             'periodic_bill': JSON.parse(localStorage.getItem("bill"))[0]['periodic_bill_id']})
    }, [])

    return (
        <>
            <label htmlFor="car">Choose car:</label>
            <select name="car" id="car" onChange={handleChangeInt} className='select-div'>
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
                {station.map( (station) => 
                <option value={station['station_id']}>{station["street"]} {station["street_number"]}, {station["postal_code"]}, {station["city"]}, {station["country"]}</option>)}
            </select>
            <label htmlFor="point">Choose charging point:</label>
            <select name="point" id="point" onChange={handleChangeInt} className='select-div'>
                {point.map( (point) => 
                <option value={point['charging_point_id']}>{point['charging_point_id_given']}</option>)}
            </select>
            <label htmlFor="bill">Choose periodic bill:</label>
            <select name="bill" id="bill" onChange={handleChangeInt} className='select-div'>
                {bill.map( (bill) => 
                <option value={bill['periodic_bill_id']}>Periodic bill {bill['periodic_bill_id']} published on {bill["published_on"].substring(0, 10)}</option>)}
            </select>
            <label htmlFor="chargeProgram">Choose charge program:</label>
            <select name="chargeProgram" id="chargeProgram" onChange={handleChangeInt} className='select-div'>
                {chargeProgram.map( (chargeProgram) => 
                <option value={chargeProgram['charge_program_id']}>{chargeProgram['description']}, price: {chargeProgram["price"]}‎€, duration: {chargeProgram["duration"]} min</option>)}
            </select>
            <label htmlFor="provider">Choose provider:</label>
            <select name="provider" id="provider" onChange={handleChangeInt} className='select-div'>
                {provider.map( (provider) => 
                <option value={provider['provider_id']}>{provider['title']}</option>)}
            </select>
            <label htmlFor="connection_time">Provide connection time:</label>
            <input placeholder='Type connection time' type='connection_time' name='connection_time' id='connection_time' 
                                    onChange={handleChange} className='input-city-select-width' required />
            <label htmlFor="disconnection_time">Provide disconnection time:</label>
            <input placeholder='Type disconnection time' type='disconnection_time' name='disconnection_time' id='disconnection_time' 
                                    onChange={handleChange} className='input-city-select-width' required />
            <label htmlFor="done_charging_time">Provide done charging time:</label>
            <input placeholder='Type done charging time' type='done_charging_time' name='done_charging_time' id='done_charging_time' 
                                    onChange={handleChange} className='input-city-select-width' required />
            <label htmlFor="payment_method">Type payment method:</label>
            <input placeholder='Type payment method' type='payment_method' name='payment_method' id='payment_method' 
                                    onChange={handleChange} className='input-city-select-width' required />
                <div className='profile-right'>
                    <button className='basic-button waves-effect waves-light btn pay' onClick={sendPost}>Charge</button>
                </div>
        </>
    );
}

export default Select;