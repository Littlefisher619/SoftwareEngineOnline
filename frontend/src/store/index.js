import Vue from 'vue';
import Vuex from 'vuex';
import * as getters from './getter.js'
import * as mutations from './mutation'
import * as actions from './action'
import homework from '../api/homework.js';
Vue.use(Vuex);
const state = { //要设置的全局访问的state对象
    user: {
        "id": 1,
        "username": "用户名",
        "stuid": "学号",
        "stuname": "姓名",
        "role": 0,
    },
    homework: {
        "homeworkname": "",
        "groupid": "",
    }
};

const store = new Vuex.Store({
    state,
    mutations,
    actions,
    getters,
});

export default store;