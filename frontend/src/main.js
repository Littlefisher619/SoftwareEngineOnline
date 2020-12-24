import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui';
import store from './store'
import api from './api' // 导入api接口
import VueLazyLoad from 'vue-lazyload'
import 'element-ui/lib/theme-chalk/index.css';
import VueClipboard from 'vue-clipboard2';
import './assets/font/iconfont.css'
import './assets/font/font.css'
import less from 'less'
Vue.use(less)
    // 走马灯
import VueAwesomeSwiper from 'vue-awesome-swiper'

// require styles
import "swiper/dist/css/swiper.css";

Vue.use(VueAwesomeSwiper, /* { default global options } */ )
    // 引入 ECharts 主模块
let echarts = require('echarts/lib/echarts');
// 引入折线图/柱状图等组件
require('echarts/lib/chart/line')
require('echarts/lib/chart/pie')
require('echarts/lib/chart/bar')
require('echarts/lib/chart/radar')
require('echarts-wordcloud');
import 'echarts/theme/macarons.js'
// 引入提示框和title组件，图例
require('echarts/lib/component/tooltip')
require('echarts/lib/component/title')
require('echarts/lib/component/legend')
require('echarts/lib/component/legendScroll') //图例滚动
    //vue全局注入echarts
Vue.prototype.$echarts = echarts



Vue.use(VueClipboard);

import ConHead from './components/ContentHead.vue'
import Duigou from './components/Duigou.vue'
Vue.use(ElementUI);
Vue.use(VueLazyLoad, {
        preLoad: 1.3,
        error: 'https://cdn.jsdelivr.net/gh/honjun/cdn@1.6/img/other/image-404.png', //加载错误图片
        loading: 'https://cdn.jsdelivr.net/gh/honjun/cdn@1.6/img/loader/orange.progress-bar-stripe-loader.svg', //正在加载图片
        attempt: 1
    })
    // Vue.http.options.xhr = { withCredentials: true };
Vue.config.silent = true
Vue.component('c-head', ConHead)
Vue.component('duigou', Duigou)
Vue.prototype.$api = api;
new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')