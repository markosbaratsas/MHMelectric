import './Login.css'
import Header from './Header'

function Error() {
  return (
    <>
      <Header />
      <div className='App'>
        <div className='login'>
          <h1>You are logged in</h1>
        </div>
      </div>
    </>
  );
}

export default Error;