import axios from 'axios'
import { Loading, Message } from 'element-ui'; //项目已经全局引入element的话可以不单独引入
//整理数据
axios.defaults.transformRequest = function(data) {
    data = JSON.stringify(data);
    return data;
};
axios.defaults.withCredentials = true;

//实例化axios
var instance = axios.create({
    timeout: 1000 * 12,
    withCredentials: true
});
let loadinginstace
instance.interceptors.request.use(
    config => {
        if (localStorage.getItem('JWT_TOKEN')) { // 判断是否存在token，如果存在的话，则每个http header都加上token
            config.headers.Authorization = `Bearer ${localStorage.getItem('JWT_TOKEN')}`;
        }
        loadinginstace = Loading.service({ fullscreen: true })
        return config;
    },
    err => {
        return Promise.reject(err);
        loadinginstace.close();
        console.log(err);
    });
instance.interceptors.response.use((response) => {
    loadinginstace.close();
    return response;
}, err => {
    loadinginstace.close();
    console.log(err)
    if (err.response.data.non_field_errors) {
        Message.error(`${err.response.data.non_field_errors}`)
    } else {
        if (err && err.response) {
            switch (err.response.status) {
                case 400:
                    Message.error("Error: 400 错误请求")
                    break;
                case 401:
                    Message.error("Error: 401 未授权请重新登陆")
                    localStorage.clear();
                    router.push({
                        path: "/sign"
                    });
                    break;
                case 403:
                    Message.error("Error: 403 拒绝访问")
                    break;
                case 404:
                    Message.error("Error: 404 请求错位,未找到该资源")
                    break;
                case 405:
                    Message.error("Error: 405 请求方法未允许")
                    break;
                case 500:
                    Message.error("Error: 500 服务端错误")
                    break;
                case 501:
                    Message.error("Error: 501 网络未实现")
                    break;
                case 502:
                    Message.error("Error: 502 网络错误")
                    break;
                case 503:
                    Message.error("Error: 503 服务不可用")
                    break;
                case 504:
                    Message.error("Error: 504 网络超时")
                    break;
                case 505:
                    Message.error("Error: 505 http不支持该请求")
                    break;
                default:
                    Message.error(`连接错误${err.response.status}`)
            }

        } else {
            Message.error("未知错误")
        }
    }
    return Promise.reject(err)
});
export default instance;