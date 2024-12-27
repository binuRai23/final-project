import React, { useState } from "react";
import "./login.css";
import FacebookIcon from "@mui/icons-material/Facebook";
import InstagramIcon from "@mui/icons-material/Instagram";
import TwitterIcon from "@mui/icons-material/Twitter";
import MyTextField from "./forms/MyTextField";
import MyPassField from "./forms/MyPassField";
import Mybutton from "./forms/Mybutton";
import { Link } from "react-router-dom";
import {useForm} from 'react-hook-form'
import AxiosInstance from "./AxiosInstance";
import { useNavigate } from "react-router-dom";
import MyMessage from "./MyMessage";

function Login() {
  const {handleSubmit, control} = useForm()
  const navigate = useNavigate()
  const [ShowMessage,setShowMessage]=useState(false)
   
  const submission = (data)=>{
    AxiosInstance.post(`login/`,{
            email: data.email,
            password: data.password,
    })
    .then((response)=>{
        console.log(response)
        localStorage.setItem('Token',response.data.token)
        navigate(`/home`)
    })
    .catch((error)=>{
      setShowMessage(true)
      console.error('Error during login',error)
    })
  }
  
  return (
    <div className="page-container">
      {ShowMessage ? <MyMessage text={"Login has failed.please try again or reset your password"}color={'#ED4337'}/>: null}
    <form onSubmit={handleSubmit(submission)}>
    <div className="login-container">
      <button className="back-button">Back</button>
      <div className="login-box">
        <h2>Sign in</h2>

          <div className="input-group">
            
            <MyTextField 
              label="Enter Your Email"
              name= {"email"}
              control={control} />
          </div>

          <div className="input-group">
            
            <MyPassField 
              label="Enter Your Password"
              name={"password"}
              control={control} />
          </div>

          <Mybutton 
          label ="login"
          type={"submit"}
          />
        <div className="options">
          <p>
            Don't have an account? <Link to ='/signup'>Create account</Link>
          </p>
          <p>
            <Link to='/request/password_reset'>Forgot password?</Link>
          </p>
        </div>
        <div className="social-links">
          <p>Follow us on</p>
          <div className="social-icons">
            <a href="#" className="icon facebook">
              <FacebookIcon />
            </a>
            <a href="#" className="icon instagram">
              <InstagramIcon />
            </a>
            <a href="#" className="icon twitter">
              <TwitterIcon />
            </a>
          </div>
        </div>
      </div>
      <div className="illustration">
        <img src="images/signin.svg" alt="Illustration" />
      </div>
    
    </div>
    </form>
    </div>
  );
}

export default Login;
