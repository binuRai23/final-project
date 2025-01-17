import axios, { Axios } from 'axios'

const baseUrl = 'http://127.0.0.1:8000/'

const AxiosInstance = axios.create({
    baseURL: baseUrl,
    timeout: 10000,
    headers:{
        "Content-Type" : "application/json",
        accept: "application/json"

    }

})

AxiosInstance.interceptors.request.use(
    (config)=> {
        const token =localStorage.getItem('Token')
        if(token){
            config.headers.Authorization=`Token ${token}`
        }
        else{
            config.headers.Authorization=``
        }
        return config;
    }
)

AxiosInstance.interceptors.response.use(
    (response)=> {
        return response
    },
    (error)=> {
        if (error.response && error.response.status === 401){
            localStorage.removeItem('Token')
            // window.location.href='/'
        }
    }
)
export const getPosts = () => AxiosInstance.get('/djangoapp/postlist/');
export const getPostDetail = (slug) => AxiosInstance.get(`/djangoapp/postdetail/${slug}/`);

export const getTopics = () => AxiosInstance.get('djangoapp/topics/');
export const postComment = (data) => AxiosInstance.post('djangoapp/comments/', data);
export default AxiosInstance