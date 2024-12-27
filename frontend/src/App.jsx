
import { Routes,Route, useLocation } from 'react-router-dom'
import Home from './components/Home'
import Login from './components/Login'
import Signup from './components/Signup'
import Navbar from './components/Navbar'
import About from './components/About'
import ProtectedRoutes from './components/ProtectedRoutes'
import PasswordResetRequest from './components/PasswordResetRequest'
import PasswordReset from './components/PasswordReset'
import Blogsite from './components/Blogsite'
import Post from './components/Post'

function App() {
  const location=useLocation()
  const noNavbar = location.pathname==="/signup"|| location.pathname ==="/"|| location.pathname.includes("password")
  
  return (
    <>

    {
      noNavbar ? 

      <Routes>
        <Route path="/" element={<Login/>}/>
        <Route path="/signup" element={<Signup/>}/>
        <Route path="/request/password_reset" element={<PasswordResetRequest/>}/>
        <Route path="/password-reset/:token" element={<PasswordReset/>}/>
       
      </Routes>

      :

      <Navbar
      content={
        <Routes>
          <Route element={<ProtectedRoutes/>}>
            <Route path="/home" element={<Home/>}/>
            <Route path="/about" element={<About/>}/>
          </Route>
          <Route>
              <Route path="/blogsite" element={<Blogsite/>}/>
              <Route path="/create-post" element={<Post/>} />
            </Route>
      </Routes>

      }
    />
    }
    
    
    
    </>
  )
}

export default App
