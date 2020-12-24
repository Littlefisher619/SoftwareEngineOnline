import base from './base'; // 导入接口域名列表
import axios from '../httpConfig/http.js'; // 导入http中创建的axios实例
// import qs from 'qs'

const team = {
    getlist(param) {
        return axios.get(`${base.group}/`, {
            params: param
        })
    },
    createTeam(param) {
        return axios.post(`${base.group}/create/`, param, { headers: { 'Content-Type': 'application/json' } })
    },
    joinTeam(groupid) {
        return axios.get(`${base.group}/${groupid}/join/`)
    }
}
export default team;