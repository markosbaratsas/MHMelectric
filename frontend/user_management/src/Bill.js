import './css/Header.css';
import './css/Profile.css';
import './css/Login.css';
import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Link } from 'react-router-dom';
import Modal from 'react-modal'

Modal.setAppElement('#root')

function Bill() {
  const [ bill, setBill ] = useState([])
  const [ session, setSession ] = useState([])
  const [ modalIsOpen, setModalIsOpen ] = useState(false)
  const [ refresh, setRefresh ] = useState(false)

  const modalStyle = {
                        overlay: {
                          position: 'fixed',
                          backdropFilter: 'blur(3px)',
                          backgroundColor: 'rgba(255, 255, 255, 0.1)'
                        },
                        content: { 
                          top: '10%',
                          left: '30%',
                          right: 'auto',
                          bottom: 'auto',
                          position: 'absolute', 
                          width: '40%', 
                          borderWidth: '1px',
                          paddingLeft: '60px',
                          paddingTop: '60px'
                        }}


  useEffect(() => {
    if (localStorage.getItem("bill")===null || refresh) {
        setRefresh(false)
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
            console.log(response.data["periodic_bills"])
            localStorage.setItem("bill", JSON.stringify(response.data["periodic_bills"]))
            })
            .catch( (error) => {
                console.log(error)
            })
    } else {
      setBill(JSON.parse(localStorage.getItem("bill")))
    }
}, [refresh])




  return (
    <>
    <div className="background-wrapper">
      <nav>
        <div className="nav-wrapper">
          <a href="#!" className="brand-logo center">MHMelectric</a>
          <ul className="left hide-on-med-and-down">
            <li><a href="/account">Account</a></li>
            <li className="active"><Link to='/bill'>Periodic Bill</Link></li>
            <li><a href="#!">Previous Charges</a></li>
            <li><a href="#!">Charge</a></li>
          </ul>
        </div>
      </nav>
      <div className='profile-wrapper'>
        <div className='profile-div'>
          <div className='profile-center'>
            <h3>Your bills</h3>
          <hr />
          </div>

          {bill.map( (bill) => 
                  <>
                  <div className='profile-left'>
                      <div className="car-div">
                          <h2>published_on:</h2>
                          <h1>{bill["published_on"].substring(0, 10)}</h1>
                      </div>
                      <div className="car-div">
                          <h2>total:</h2>
                          <h1>{bill["total"]}</h1>
                      </div>
                      <div className="car-div">
                          <h2>discount:</h2>
                          <h1>{bill["discount"]}</h1>
                      </div>
                  </div>
                  <div className='profile-left'>
                    <button className='link' onClick={() => {
                                                  console.log(bill["periodic_bill_id"])

                                                  var details = {
                                                    method: 'get',
                                                    url: 'http://127.0.0.1:8765/evcharge/api/get_sessions_of_periodic_bill/'+bill["periodic_bill_id"],
                                                    headers: {
                                                    'X-OBSERVATORY-AUTH': JSON.parse(localStorage["tokens"])
                                                    }
                                                }
                                                axios(details)
                                                    .then( (response) => {                                      
                                                      setSession(response.data["sessions"])
                                                      setModalIsOpen(true); 
                                                      console.log(response.data)
                                                    })
                                                    .catch( (error) => {
                                                        console.log(error)
                                                    })
                                                }
                                              }>
                    See sessions</button>
                  </div>
                  <div className='profile-center'>
                    <button className={'basic-button waves-effect waves-light btn pay '+JSON.stringify(bill["paid"])} onClick={() => {
                      if(!bill["paid"]){
                      var details = {
                        method: 'get',
                        url: 'http://127.0.0.1:8765/evcharge/api/pay_periodic_bill/'+bill["periodic_bill_id"],
                        headers: {
                        'X-OBSERVATORY-AUTH': JSON.parse(localStorage["tokens"])
                        }
                      }
                      axios(details)
                        .then( (response) => {       
                          console.log(response)
                          setRefresh(true)
                          alert("Bill paid!")
                        })
                        .catch( (error) => {
                            console.log(error)
                        })
                      }
                      else{
                        alert("This bill is already paid!")
                      }
                    }}>Pay</button>
                  </div>
                 
                 
                 
                 
                    <Modal isOpen={modalIsOpen} onRequestClose={() => setModalIsOpen(false)} style={modalStyle}>
                      
                    { session.map( (session) => 
                          <>
                          <div className='profile-left'>
                              <div className="car-div">
                                  <h2>Car charged:</h2>
                                  <h1>{session["car"]["brand"]}, {session["car"]["model"]}, {session["car"]["type"]}, {session["car"]["release_year"]}</h1>
                              </div>
                               <div className="car-div">
                                  <h2>Charging program:</h2>
                                  <h1>{session["charge_program"]["description"]}</h1>
                              </div>
                              <div className="car-div">
                                  <h2>Charging station:</h2>
                                  <h1>{session["station"]["street"]} {session["station"]["street_number"]}, {session["station"]["postal_code"]}, {session["station"]["city"]}, {session["station"]["country"]}</h1>
                              </div>
                              <div className="car-div">
                                  <h2>Charging point:</h2>
                                  <h1>{session["charging_point"]}</h1>
                              </div>
                              <div className="car-div">
                                  <h2>Date:</h2>
                                  <h1>{session["connection_time"].substring(0, 10)}</h1>
                              </div>
                              <div className="car-div">
                                  <h2>Connection time:</h2>
                                  <h1>{session["connection_time"].substring(11, 19)}</h1>
                              </div>
                              <div className="car-div">
                                  <h2>Disconnection time:</h2>
                                  <h1>{session["disconnection_time"].substring(11, 19)}</h1>
                              </div>
                              <div className="car-div">
                                  <h2>Done charging:</h2>
                                  <h1>{session["done_charging_time"].substring(11, 19)}</h1>
                              </div>
                              <div className="car-div">
                                  <h2>kWh delivered:</h2>
                                  <h1>{session["kWh_delivered"]}</h1>
                              </div>
                              <div className="car-div">
                                  <h2>Protocol:</h2>
                                  <h1>{session["protocol"]}</h1>
                              </div>
                              <div className="car-div">
                                  <h2>Payment method:</h2>
                                  <h1>{session["user_payment_method"]}</h1>
                              </div>
                              <div className="car-div">
                                  <h2>Wh per mile:</h2>
                                  <h1>{session["user_Wh_per_mile"]}</h1>
                              </div>
                              <div className="car-div">
                                  <h2>kWh requested:</h2>
                                  <h1>{session["user_kWh_requested"]}</h1>
                              </div>
                              <div className="car-div">
                                  <h2>Miles requested:</h2>
                                  <h1>{session["user_miles_requested"]}</h1>
                              </div>
                              <div className="car-div">
                                  <h2>Minutes available:</h2>
                                  <h1>{session["user_minutes_available"]}</h1>
                              </div>
                              <div className="car-div">
                                  <h2>Requested departure:</h2>
                                  <h1>{session["user_requested_departure"].substring(11, 19)}</h1>
                              </div>
                              <div className="car-div">
                                  <h2>Provider:</h2>
                                  <h1>{session["provider"]["title"]}, {session["provider"]["primary_phone"]}, {session["provider"]["email"]}</h1>
                              </div>
                          </div>
                          <hr />
                      </>
                      )}



                      <div className='profile-right'>
                        <button className='basic-button waves-effect waves-light btn pay' onClick={() => {
                                                                                                    setModalIsOpen(false); 
                                                                                                    setSession([])
                                                                                                    }}>
                        Close</button>
                      </div>
                    </Modal>
                  <hr />
              </>
              )}
        </div>
      </div>
    </div>
    </>
  );
}

export default Bill;
