import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store'
Vue.use(VueRouter);
const routes = [{
        path: '/',
        redirect: '/homework'
    },
    {
        path: '/sign',
        name: 'signin',
        component: resolve => require(['../views/sign/signin.vue'], resolve),
        meta: {
            keepAlive: true,
        },
    },
    {
        path: '/signup',
        name: 'signup',
        component: resolve => require(['../views/sign/signup.vue'], resolve),
        meta: {
            keepAlive: true,
        },
    },
    {
        path: '/homework',
        name: '课程作业',
        component: resolve => require(['../views/homework/Homework.vue'], resolve),
        redirect: '/homework/single',
        children: [{
                path: "single",
                name: "homeworkSingle",
                component: resolve => require(['../views/homework/Single.vue'], resolve),
                meta: {
                    name: "个人作业",
                    parentName: "课程作业"
                },
            },
            {
                path: "couple",
                name: "homeworkCouple",
                component: resolve => require(['../views/homework/Couple.vue'], resolve),
                meta: {
                    name: "结对作业",
                    parentName: "课程作业"
                },
            },
            {
                path: "group",
                name: "homeworkGroup",
                component: resolve => require(['../views/homework/Group.vue'], resolve),
                meta: {
                    name: "团队项目",
                    parentName: "课程作业"
                }
            },
            {
                path: 'detail',
                name: '个人作业详情',
                component: resolve => require(['../views/homework/Detail.vue'], resolve),
                meta: {
                    name: "作业详情",
                    parentName: "课程作业"
                }
            },
            {
                path: "analyse",
                name: "作业分析",
                component: resolve => require(['../views/homework/Analyse.vue'], resolve),
                meta: {
                    name: "作业分析",
                    parentName: "课程作业"
                }
            },
            {
                path: "summary",
                name: "作业总结",
                component: resolve => require(['../views/homework/Summary.vue'], resolve),
                meta: {
                    name: "作业总结",
                    parentName: "课程作业",
                    keepAlive: true,
                },
            }
        ]
    },
    {
        path: '/team',
        name: '我的队伍',
        component: resolve => require(['../views/team/Team.vue'], resolve),
        redirect: '/team/couple',
        children: [{
                path: 'couple',
                name: 'teamcouple',
                component: resolve => require(['../views/team/Couple.vue'], resolve),
                meta: {
                    name: '结对作业',
                    parentName: "我的队伍",
                }
            },
            {
                path: 'group',
                name: 'teamgroup',
                component: resolve => require(['../views/team/Group.vue'], resolve),
                meta: {
                    name: '团队项目',
                    parentName: "我的队伍",
                }
            }
        ]
    },
    {
        path: '/score',
        name: '课程评分',
        component: resolve => require(['../views/score/Score.vue'], resolve),
        redirect: '/score/single',
        children: [{
                path: 'single',
                name: "scoresingle",
                component: resolve => require(['../views/score/Single.vue'], resolve),
                meta: {
                    name: "个人作业",
                    parentName: "课程评分",
                },
            },
            {
                path: 'couple',
                name: "scorecouple",
                component: resolve => require(['../views/score/Couple.vue'], resolve),
                meta: {
                    name: "结对作业",
                    parentName: "课程评分",
                }
            },
            {
                path: 'judge',
                name: "scorejudge",
                component: resolve => require(['../views/score/Judge.vue'], resolve),
                meta: {
                    name: "团队作业",
                    parentName: "课程评分",
                }
            },
            {
                path: 'list',
                name: "scorelist",
                component: resolve => require(['../views/score/List.vue'], resolve),
                meta: {
                    name: "评分列表",
                    parentName: "课程评分",
                }
            },
            {
                path: 'lists',
                name: "groupScoreList",
                component: resolve => require(['../views/score/Clist.vue'], resolve),
                meta: {
                    name: "评分列表",
                    parentName: "课程评分",
                }
            },
            {
                path: 'all',
                name: 'scoreall',
                component: resolve => require(['../views/score/All.vue'], resolve),
                meta: {
                    name: "评分列表",
                    parentName: "课程评分"
                }
            }
        ]
    },
    {
        path: '/rank',
        name: 'rank',
        component: resolve => require(['../views/rank/Rank.vue'], resolve),
        meta: {
            name: "排行榜",
            parentName: "成绩情况"
        }
    },
    {
        path: '/sails',
        name: '千帆竞技图',
        component: resolve => require(['../views/rank/Sails.vue'], resolve),
        meta: {
            name: "千帆竞技图",
            keepAlive: true,
        }
    },
    {
        path: '/setting',
        name: 'setting',
        redirect: '/setting/info',
        component: resolve => require(['../views/setting/Setting.vue'], resolve),
        children: [{
                path: 'info',
                name: 'setInfo',
                component: resolve => require(['../views/setting/Infor.vue'], resolve),
                meta: {
                    name: "基本设置",
                    parentName: "设置"
                }
            },
            {
                path: 'changepw',
                name: 'setChangepw',
                component: resolve => require(['../views/setting/Changepw.vue'], resolve),
                meta: {
                    name: "修改密码",
                    parentName: "设置",
                }
            }
        ]
    }
]

const router = new VueRouter({
    mode: 'history',
    routes
})
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(err => err)
}

router.beforeEach(({ name }, from, next) => {
    // 获取 JWT Token
    if (localStorage.getItem('JWT_TOKEN')) {
        // 如果用户在login页面
        if (name === 'signin') {
            next('/homework');
        } else {
            if (name != 'scoreall' && name != 'scorelist' && name != "groupScoreList") {
                store.dispatch('setHomeworkName', "");
            }
            next();
        }
    } else {
        if (name === 'signin' || name == "signup") {
            next();
        } else {
            next({ name: 'signin' });
        }
    }
});
export default router