import React from "react";
import "./Css/signup.css";
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
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from "yup"

function Signup() {
   
    const navigate = useNavigate()
   
    const schema = yup
    .object({
        email: yup.string().email('Field expects an email address').required('Email is a required Field'),
        password: yup.string()
                    .required('Password is a required Field')
                    .min(8,'Password must be at least 8 characters')
                    .matches(/[A-Z]/,'Password must contain at least one uppercase letter')
                    .matches(/[a-z]/,'Password must contain at least one lowercase letter')
                    .matches(/[0-9]/,'Password must contain at least one number')
                    .matches(/[!@#$%^&*>]/,'password must contain at least one special character'),
        password2:yup.string().required('Password confirmation is a required field')
                    .oneOf([yup.ref('password'),null],'Password doesnot match')

    })
    const {handleSubmit, control} = useForm({resolver:yupResolver(schema)})
    const submission = (data)=>{
        AxiosInstance.post(`register/`,{
                email: data.email,
                password: data.password,
        })
        .then(()=>{
            navigate(`/`)
        })
    }
  return (
    <div className="page-container2">
    <form onSubmit={handleSubmit(submission)}>
    <div className="login-container">
      <button className="back-button">Back</button>

      
      <div className="login-box">
        <h2>Sign in</h2>
          <div className="input-group">
        
            <MyTextField 
                label={"Enter Your Email"}
                name= {"email"}
                control={control} />
          </div>

          <div className="input-group">
            
            <MyPassField 
                label="Enter Your Password"
                name={"password"}
                control={control} />
          </div>

          <div className="input-group">
          
            <MyPassField 
                label="Confirm Password" 
                name ={"password2"}
                control={control}
            />
          </div>
          <Mybutton 
                type={"submit"}
                label ="Sign up"/>
        <div className="options">
          <p>
            Already have an account? <Link to ='/'>Sign in</Link>
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

export default Signup;
