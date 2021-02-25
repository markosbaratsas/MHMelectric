import './Login.css'
import Header from './Header'
import { useAuth } from './context/auth'

function Test() {
    // const { setAuthTokens } = useAuth();

    // function logOut() {
    //     setAuthTokens();
    // }

  return (
    <>
      <Header />
      <div className='App'>
        <div className='login'>
          <h1>You are logged in</h1>
        </div>
        {/* <button onClick={logOut()} className='link'>Log out</button> */}
      </div>
    </>
  );
}

export default Test;