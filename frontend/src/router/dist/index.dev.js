"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports["default"] = void 0;

var _vue = _interopRequireDefault(require("vue"));

var _vueRouter = _interopRequireDefault(require("vue-router"));

var _store = _interopRequireDefault(require("../store"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

_vue["default"].use(_vueRouter["default"]);

var routes = [{
  path: '/',
  redirect: '/homework'
}, {
  path: '/sign',
  name: 'signin',
  component: function component(resolve) {
    return require(['../views/sign/signin.vue'], resolve);
  },
  meta: {
    keepAlive: true
  }
}, {
  path: '/signup',
  name: 'signup',
  component: function component(resolve) {
    return require(['../views/sign/signup.vue'], resolve);
  },
  meta: {
    keepAlive: true
  }
}, {
  path: '/homework',
  name: '课程作业',
  component: function component(resolve) {
    return require(['../views/homework/Homework.vue'], resolve);
  },
  redirect: '/homework/single',
  children: [// {
  //     path: "blog",
  //     name: "homeworkBlog",
  //     component: resolve => require(['../views/homework/Blog.vue'], resolve),
  //     meta: {
  //         name: "个人博客作业",
  //         parentName: "课程作业"
  //     }
  // },
  {
    path: "single",
    name: "homeworkSingle",
    component: function component(resolve) {
      return require(['../views/homework/Single.vue'], resolve);
    },
    meta: {
      name: "个人作业",
      parentName: "课程作业"
    }
  }, {
    path: "couple",
    name: "homeworkCouple",
    component: function component(resolve) {
      return require(['../views/homework/Couple.vue'], resolve);
    },
    meta: {
      name: "组队作业",
      parentName: "课程作业"
    }
  }, {
    path: "group",
    name: "homeworkGroup",
    component: function component(resolve) {
      return require(['../views/homework/Group.vue'], resolve);
    },
    meta: {
      name: "团队项目",
      parentName: "课程作业"
    }
  }, {
    path: 'detail',
    name: '个人作业详情',
    component: function component(resolve) {
      return require(['../views/homework/Detail.vue'], resolve);
    },
    meta: {
      name: "作业详情",
      parentName: "课程作业"
    }
  }, {
    path: "analyse",
    name: "作业分析",
    component: function component(resolve) {
      return require(['../views/homework/Analyse.vue'], resolve);
    },
    meta: {
      name: "作业分析",
      parentName: "课程作业"
    }
  }]
}, {
  path: '/team',
  name: '我的队伍',
  component: function component(resolve) {
    return require(['../views/team/Team.vue'], resolve);
  },
  redirect: '/team/couple',
  children: [{
    path: 'couple',
    name: 'teamcouple',
    component: function component(resolve) {
      return require(['../views/team/Couple.vue'], resolve);
    },
    meta: {
      name: '组队作业',
      parentName: "我的队伍"
    }
  }, {
    path: 'group',
    name: 'teamgroup',
    component: function component(resolve) {
      return require(['../views/team/Group.vue'], resolve);
    },
    meta: {
      name: '团队项目',
      parentName: "我的队伍"
    }
  }]
}, {
  path: '/score',
  name: '课程评分',
  component: function component(resolve) {
    return require(['../views/score/Score.vue'], resolve);
  },
  redirect: '/score/single',
  children: [{
    path: 'single',
    name: "scoresingle",
    component: function component(resolve) {
      return require(['../views/score/Single.vue'], resolve);
    },
    meta: {
      name: "个人作业",
      parentName: "课程评分"
    }
  }, {
    path: 'couple',
    name: "scorecouple",
    component: function component(resolve) {
      return require(['../views/score/Couple.vue'], resolve);
    },
    meta: {
      name: "组队评分",
      parentName: "课程评分"
    }
  }, {
    path: 'judge',
    name: "scorejudge",
    component: function component(resolve) {
      return require(['../views/score/Judge.vue'], resolve);
    },
    meta: {
      name: "团队作业",
      parentName: "课程评分"
    }
  }, {
    path: 'list',
    name: "scorelist",
    component: function component(resolve) {
      return require(['../views/score/List.vue'], resolve);
    },
    meta: {
      name: "评分列表",
      parentName: "课程评分"
    }
  }, {
    path: 'all',
    name: 'scoreall',
    component: function component(resolve) {
      return require(['../views/score/All.vue'], resolve);
    },
    meta: {
      name: "评分列表",
      parentName: "课程评分"
    }
  }]
}, {
  path: '/setting',
  name: 'setting',
  redirect: '/setting/info',
  component: function component(resolve) {
    return require(['../views/setting/Setting.vue'], resolve);
  },
  children: [{
    path: 'info',
    name: 'setInfo',
    component: function component(resolve) {
      return require(['../views/setting/Infor.vue'], resolve);
    },
    meta: {
      name: "基本设置",
      parentName: "设置"
    }
  }, {
    path: 'changepw',
    name: 'setChangepw',
    component: function component(resolve) {
      return require(['../views/setting/Changepw.vue'], resolve);
    },
    meta: {
      name: "修改密码",
      parentName: "设置"
    }
  }]
}];
var router = new _vueRouter["default"]({
  mode: 'history',
  routes: routes
});
var originalPush = _vueRouter["default"].prototype.push;

_vueRouter["default"].prototype.push = function push(location) {
  return originalPush.call(this, location)["catch"](function (err) {
    return err;
  });
};

router.beforeEach(function (_ref, from, next) {
  var name = _ref.name;

  // 获取 JWT Token
  if (localStorage.getItem('JWT_TOKEN')) {
    // 如果用户在login页面
    if (name === 'signin') {
      next('/homework');
    } else {
      if (name != 'scoreall' && name != 'scorelist') {
        _store["default"].dispatch('setHomeworkName', "");
      }

      next();
    }
  } else {
    if (name === 'signin' || name == "signup") {
      next();
    } else {
      next({
        name: 'signin'
      });
    }
  }
});
var _default = router;
exports["default"] = _default;