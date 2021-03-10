import './css/Login.css'
import Header from './Header'

function Error() {
  return (
    <>
      <Header />
      <div className='App'>
          <h1>The page you are looking for does not exist.</h1>
      </div>
    </>
  );
}

export default Error;