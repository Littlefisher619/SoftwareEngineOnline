import base from './base'; // 导入接口域名列表
import axios from '../httpConfig/http.js'; // 导入http中创建的axios实例
// import qs from 'qs'

const user = {
    signin(param) {
        return axios.post(`${base.login}`, param, { headers: { 'Content-Type': 'application/json' } })
    },
    signup(param) {
        return axios.post(`${base.signup}`, param, { headers: { 'Content-Type': 'application/json' } })
    },
    getuser() {
        return axios.get(`${base.user}/`)
    },
    updatepassword(param) {
        return axios.post(`${base.user}/updatepassword/`, param, { headers: { 'Content-Type': 'application/json' } })
    },
    information() {
        return axios.get(`${base.user}/me/`)
    },
    mygroup() {
        return axios.get(`${base.user}/mygroup/`)
    },
    myjudge() {
        return axios.get(`${base.user}/judgements/`)
    }
}
export default user;