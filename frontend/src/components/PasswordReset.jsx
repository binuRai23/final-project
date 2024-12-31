import React, { useState } from "react";
import "./Css/password.css";
import MyPassField from "./forms/MyPassField";
import Mybutton from "./forms/Mybutton";
import { useParams} from "react-router-dom";
import {useForm} from 'react-hook-form'
import AxiosInstance from "./AxiosInstance";
import { useNavigate} from "react-router-dom";
import MyMessage from "./MyMessage";

const PasswordReset =()=> {
    const {handleSubmit, control} = useForm()
    const navigate = useNavigate()
    const{token} = useParams()
    console.log(token)

    const [ShowMessage,setShowMessage] = useState(false)

    const submission = (data)=>{
        AxiosInstance.post(`api/password_reset/confirm/`,{
                password: data.password,
                token: token ,
        })
        .then((response)=>{
            setShowMessage(true)
            setTimeout(()=> {

              navigate('/')
            },6000)

        })
    }
    return(
    <div className="page-container3">
        <form onSubmit={handleSubmit(submission)}>
    {ShowMessage ? <MyMessage text={"your password reset was successful!!"} color={'#008000'}/>: null}
    <div className="reset-container">
        
      {/* <button className="back-button"><Link to='/'>Back</Link></button> */}
      <div className="reset-box">
        <h2>Reset password</h2>

          <div className="input-group">
              <MyPassField 
                          label="Enter Your Password"
                          name={"password"}
                          control={control} />
          </div>

          <div className="input-group">
              <MyPassField 
                          label="Confirm Your Password"
                          name={"password2"}
                          control={control} />
          </div>

          <Mybutton 
          label ="Reset password"
          type={"submit"}
          />
    </div>
    </div>
    </form>
    </div>
  );
}
export default PasswordReset