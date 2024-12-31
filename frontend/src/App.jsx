
import { Routes,Route, useLocation, BrowserRouter } from 'react-router-dom'
import Home from './components/Home'
import Login from './components/Login'
import Signup from './components/Signup'
import Navbar from './components/Navbar'
import About from './components/About'
import ProtectedRoutes from './components/ProtectedRoutes'
import PasswordResetRequest from './components/PasswordResetRequest'
import PasswordReset from './components/PasswordReset'
import Timeline from './components/Timeline'
import Post from './components/Post'

import Detail from "./Blogcore/Postdetail";
import Search from "./Blogcore/Search";
import Category from "./Blogcore/Topic";
import Dashboard from "./Blogsite/Dashboard";
import Posts from "./Blogsite/Posts";
import AddPost from "./Blogsite/AddPost";
import EditPost from "./Blogsite/EditPost";
import Comments from "./Blogsite/Comments";
import Notifications from "./Blogsite/Notifications";
import Profile from "./Blogsite/Profile";

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
            <Route path="/dashboard/" element={<Dashboard />} />
                    

          </Route>
          <Route>
              <Route path="/timeline" element={<Timeline/>}/>
              <Route path="/post/" element={<Posts />} />
              <Route path="/createpost/" element={<AddPost />} />
              <Route path="/updatepost/" element={<EditPost />} />
              <Route path="/comment/" element={<Comments />} />
              <Route path="/notif/" element={<Notifications />} />
              <Route path="/profile/" element={<Profile />} />
              <Route path="/topic/" element={<Topic />} />
              <Route path="/search/" element={<Search />} />
            </Route>
      </Routes>

      }
    />
    }
    
    
    
    </>
  )
}

export default App
