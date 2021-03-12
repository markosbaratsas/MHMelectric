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
  const [ previousBill, setPreviousBill ] = useState([])
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
                          maxHeight: '60%',
                          overflowY: 'auto',
                          top: '20%',
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
        localStorage.setItem("bill", JSON.stringify(response.data["periodic_bills"]))
        const billArray = []
        const previousBillArray = []

        for(let i=0; i<response.data["periodic_bills"].length; i++){
          if(response.data["periodic_bills"][i]['paid']!==true) {
            billArray.push(response.data["periodic_bills"][i])
          } else {
            previousBillArray.push(response.data["periodic_bills"][i])
          }
        }
        setBill(billArray)
        setPreviousBill(previousBillArray)
        })
        .catch( (error) => {
            console.log(error)
        })
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
            <li><Link to='/charge'>Charge</Link></li>
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
                          <h1>{bill["total"]} ‎€</h1>
                      </div>
                      <div className="car-div">
                          <h2>discount:</h2>
                          <h1>{bill["discount"]} ‎€</h1>
                      </div>
                  </div>
                  <div className='profile-left'>
                    <button className='link' onClick={() => {
                                                  var details = {
                                                    method: 'get',
                                                    url: 'http://127.0.0.1:8765/evcharge/api/get_sessions_of_periodic_bill/'+bill["periodic_bill_id"],
                                                    headers: {
                                                    'X-OBSERVATORY-AUTH': JSON.parse(localStorage["tokens"])
                                                    }
                                                }
                                                axios(details)
                                                    .then( (response) => {
                                                      for(let i = 0; i < response.data["sessions"].length; i++) {       
                                                        if(response.data["sessions"][i]["charge_program"]===null) 
                                                          response.data["sessions"][i]["charge_program"] = {'description': ''}
                                                        if(response.data["sessions"][i]["connection_time"]!==null) 
                                                          response.data["sessions"][i]["Date"] = response.data["sessions"][i]["connection_time"].substring(0, 10)
                                                        if(response.data["sessions"][i]["connection_time"]!==null) 
                                                          response.data["sessions"][i]["connection_time"] = response.data["sessions"][i]["connection_time"].substring(11, 19)
                                                        if(response.data["sessions"][i]["disconnection_time"]!==null) 
                                                          response.data["sessions"][i]["disconnection_time"] = response.data["sessions"][i]["disconnection_time"].substring(11, 19)
                                                        if(response.data["sessions"][i]["done_charging_time"]!==null) 
                                                          response.data["sessions"][i]["done_charging_time"] = response.data["sessions"][i]["done_charging_time"].substring(11, 19)
                                                        if(response.data["sessions"][i]["user_requested_departure"]!==null) 
                                                          response.data["sessions"][i]["user_requested_departure"] = response.data["sessions"][i]["user_requested_departure"].substring(11, 19)
                                                        if(response.data["sessions"][i]["provider"]===null) 
                                                          response.data["sessions"][i]["provider"] = {'title': '', 'primary_phone': '', 'email': ''}
                                                        if(response.data["sessions"][i]["station"]===null)
                                                          response.data["sessions"][i]["station"] = {'street': '', 'street_number': '', 'postal_code': '', 'city': '', 'country': ''}
                                                        if(response.data["sessions"][i]["car"]===null)
                                                          response.data["sessions"][i]["car"] = {'brand': '', 'model': '', 'type': '', 'release_year': ''}
                                                      }        
                                                      setSession(response.data["sessions"])
                                                      setModalIsOpen(true);
                                                    })
                                                    .catch( (error) => {
                                                        console.log(error)
                                                    })
                                                }
                                              }>
                    See sessions</button>
                  </div>
                  <div className='profile-center'>
                    <button id={bill["periodic_bill_id"]} className={'basic-button waves-effect waves-light btn pay '+JSON.stringify(bill["paid"])} onClick={() => {
                      if(!bill["paid"]){
                      var details = {
                        method: 'get',
                        url: 'http://127.0.0.1:8765/evcharge/api/pay_periodic_bill/'+bill["periodic_bill_id"],
                        headers: {
                        'X-OBSERVATORY-AUTH': JSON.parse(localStorage["tokens"])
                        }
                      }
                      axios(details)
                        // .then( (response) => {
                        .then( () => {
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
                  <hr />
              </>
              )}
          <div className='profile-center'>
            <h3>Previous bills</h3>
          <hr />
          </div>

          {previousBill.map( (previousBill) => 
                  <>
                  <div className='profile-left'>
                      <div className="car-div">
                          <h2>published_on:</h2>
                          <h1>{previousBill["published_on"].substring(0, 10)}</h1>
                      </div>
                      <div className="car-div">
                          <h2>total:</h2>
                          <h1>{previousBill["total"]} ‎€</h1>
                      </div>
                      <div className="car-div">
                          <h2>discount:</h2>
                          <h1>{previousBill["discount"]} ‎€</h1>
                      </div>
                  </div>
                  <div className='profile-left'>
                    <button className='link' onClick={() => {
                                                  var details = {
                                                    method: 'get',
                                                    url: 'http://127.0.0.1:8765/evcharge/api/get_sessions_of_periodic_bill/'+previousBill["periodic_bill_id"],
                                                    headers: {
                                                    'X-OBSERVATORY-AUTH': JSON.parse(localStorage["tokens"])
                                                    }
                                                }
                                                axios(details)
                                                    .then( (response) => {
                                                      for(let i = 0; i < response.data["sessions"].length; i++) {       
                                                        if(response.data["sessions"][i]["charge_program"]===null) 
                                                          response.data["sessions"][i]["charge_program"] = {'description': ''}
                                                        if(response.data["sessions"][i]["connection_time"]!==null) 
                                                          response.data["sessions"][i]["Date"] = response.data["sessions"][i]["connection_time"].substring(0, 10)
                                                        if(response.data["sessions"][i]["connection_time"]!==null) 
                                                          response.data["sessions"][i]["connection_time"] = response.data["sessions"][i]["connection_time"].substring(11, 19)
                                                        if(response.data["sessions"][i]["disconnection_time"]!==null) 
                                                          response.data["sessions"][i]["disconnection_time"] = response.data["sessions"][i]["disconnection_time"].substring(11, 19)
                                                        if(response.data["sessions"][i]["done_charging_time"]!==null) 
                                                          response.data["sessions"][i]["done_charging_time"] = response.data["sessions"][i]["done_charging_time"].substring(11, 19)
                                                        if(response.data["sessions"][i]["user_requested_departure"]!==null) 
                                                          response.data["sessions"][i]["user_requested_departure"] = response.data["sessions"][i]["user_requested_departure"].substring(11, 19)
                                                        if(response.data["sessions"][i]["provider"]===null) 
                                                          response.data["sessions"][i]["provider"] = {'title': '', 'primary_phone': '', 'email': ''}
                                                        if(response.data["sessions"][i]["station"]===null)
                                                          response.data["sessions"][i]["station"] = {'street': '', 'street_number': '', 'postal_code': '', 'city': '', 'country': ''}
                                                        if(response.data["sessions"][i]["car"]===null)
                                                          response.data["sessions"][i]["car"] = {'brand': '', 'model': '', 'type': '', 'release_year': ''}
                                                      }
                                                      setSession(response.data["sessions"])
                                                      setModalIsOpen(true);
                                                    })
                                                    .catch( (error) => {
                                                        console.log(error)
                                                    })
                                                }
                                              }>
                    See sessions</button>
                  </div>
                  <hr />
              </>
              )}

        </div>
      </div>
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
                                  <h1>{session["station"]["street"]} {session["station"]["street_number"]}, {session["station"]["postal_code"]}, {session["station"]["city"]}, 
                                    {session["station"]["country"]}</h1>
                              </div>
                              <div className="car-div">
                                  <h2>Charging point:</h2>
                                  <h1>{session["charging_point"]}</h1>
                              </div>
                              <div className="car-div">
                                  <h2>Date:</h2>
                                  <h1>{session["Date"]}</h1>
                              </div>
                              <div className="car-div">
                                  <h2>Connection time:</h2>
                                  <h1>{session["connection_time"]}</h1>
                              </div>
                              <div className="car-div">
                                  <h2>Disconnection time:</h2>
                                  <h1>{session["disconnection_time"]}</h1>
                              </div>
                              <div className="car-div">
                                  <h2>Done charging:</h2>
                                  <h1>{session["done_charging_time"]}</h1>
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
                                  <h1>{session["user_requested_departure"]}</h1>
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
    </>
  );
}

export default Bill;
