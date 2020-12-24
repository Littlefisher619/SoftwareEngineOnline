import base from './base'; // 导入接口域名列表
import axios from '../httpConfig/http.js'; // 导入http中创建的axios实例
import qs from 'qs'

const homework = {
    getlist(homeworktype = 0) {
        let param = {
            "homeworktype": homeworktype
        }
        return axios.get(`${base.homework}`, {
            params: param
        });
    },
    tasklist(taskid, params) {
        return axios.get(`${base.homework}${taskid}/tasklist/`, {
            params: params
        })
    },
    static(taskid) {
        return axios.get(`${base.homework}${taskid}/statistics/`)
    }
}
export default homework;