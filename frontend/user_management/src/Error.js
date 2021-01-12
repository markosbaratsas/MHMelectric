import './Login.css'
import Header from './Header'

function Error() {
  return (
    <>
      <Header />
      <div className='App'>
        <div className='login'>
          <h1>The page you are looking for does not exist.</h1>
        </div>
      </div>
    </>
  );
}

export default Error;