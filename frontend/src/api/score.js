import base from './base'; // 导入接口域名列表
import axios from '../httpConfig/http.js'; // 导入http中创建的axios实例
// import qs from 'qs'

const score = {
    judgement(param) {
        return axios.get(`${base.judgement}/`, {
            params: param,
        })
    },
    createjudge(param) {
        return axios.post(`${base.judgement}/create/`, param, { headers: { 'Content-Type': 'application/json' } })
    },
    //更新评分
    update(id, param) {
        return axios.patch(`${base.judgement}/${id}/`, param, { headers: { 'Content-Type': 'application/json' } })
    },
    //组内评分
    rateCreate(param) {
        return axios.post(`${base.rate}/create/`, param, { headers: { 'Content-Type': 'application/json' } })
    },
    //排行榜
    rank() {
        return axios.get(`${base.user}/rank/`)
    },
    getrate(param){
        return axios.get(`${base.rate}/`,{
            params: param,
        })
    }
}
export default score;