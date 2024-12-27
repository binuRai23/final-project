import React, { useState } from "react";
import "./password.css";
import MyTextField from "./forms/MyTextField";
import Mybutton from "./forms/Mybutton";
import { Link } from "react-router-dom";
import {useForm} from 'react-hook-form'
import AxiosInstance from "./AxiosInstance";
import { useNavigate } from "react-router-dom";
import MyMessage from "./MyMessage";

const PasswordResetRequest =()=> {
    const {handleSubmit, control} = useForm()
    const navigate = useNavigate()

    const [ShowMessage,setShowMessage] = useState(false)

    const submission = (data)=>{
        AxiosInstance.post(`api/password_reset/`,{
                email: data.email,
        })
        .then((response)=>{
            setShowMessage(true)
        })
    }
    return(
      <div className="page-container3">
        <form onSubmit={handleSubmit(submission)}>
    {ShowMessage ? <MyMessage text={"Please Check your email to see the instructions on how to reset your password"}color={'#008000'}/>: null}
    <div className="reset-container">
        
      {/* <button className="back-button"><Link to='/'>Back</Link></button> */}
      <div className="reset-box">
        <h2>Reset password</h2>

          <div className="input-group">
            
            <MyTextField 
              label="Enter Your Email"
              name= {"email"}
              control={control} />
          </div>

          <Mybutton 
          label ="Request Password reset"
          type={"submit"}
          />
    </div>
    </div>
    </form>
    </div>
  );
}
export default PasswordResetRequest