<template>
    <div id="navleft">
        <el-menu
        :default-active="$route.path"
        class="el-menu-vertical-demo"
        @select="handleSelect"
        background-color="#3E3E3E"
        text-color="rgba(255,255,255,0.45)"
        active-text-color="#ffffff"
        :default-openeds="openeds">
        <div class="menu_head">软工评测平台</div>
        <el-submenu index="/homework">
            <template slot="title">
            <i class="el-icon-s-order"></i>
            <span>课程作业</span>
            </template>
            <el-menu-item index="/homework/single">个人作业</el-menu-item>
            <el-menu-item index="/homework/couple">结对作业</el-menu-item>
            <el-menu-item index="/homework/group">团队项目</el-menu-item>
        </el-submenu>
        <el-submenu index="/team">
            <template slot="title">
            <i class="el-icon-s-custom"></i>
            <span>我的队伍</span>
            </template>
            <el-menu-item index="/team/couple">结对作业</el-menu-item>
            <el-menu-item index="/team/group">团队项目</el-menu-item>
        </el-submenu>
        <el-submenu index="/score">
            <template slot="title">
            <i class="el-icon-s-marketing"></i>
            <span>课程评分</span>
            </template>
            <el-menu-item index="/score/single">个人作业</el-menu-item>
            <el-menu-item index="/score/couple">结对作业</el-menu-item>
            <el-menu-item index="/score/judge">团队评分</el-menu-item>
        </el-submenu>
        <el-menu-item index="/rank"><i class="iconfont icon-huangguanguanjun"></i>排行榜</el-menu-item>
        </el-menu>
    </div>
</template>
<script>
export default {
    data(){
        return{
            openeds:[
                '/homework',
                '/team',
                '/score',
            ]
        }
    },
    methods:{
        handleSelect(key) {
        this.$router.push({
                path: key,
            })
      },
    }
}
</script>
<style scoped>
.navleft{
    height: 100%;
    width: 100%;
}
.menu_head{
    background: #979797;
    color: #ffffff;
    margin-top: 10px;
    width: 70%;
    height: 30px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-bottom: 10%;
    border-radius: 4px;
}
.el-icon-s-custom{
    font-size: 12px;
}
.icon-huangguanguanjun{
    font-size: 20px;
    margin-right: 6px;
}
</style>
<style>
#navleft > ul{
    width: 100%!important;
    min-width: 200px;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    font-size: 12px;
}  
#navleft > ul > li.el-submenu,
#navleft > ul > li.el-menu-item{
    width: 100%;
    font-size: 12px;
}
#navleft > ul > li.el-submenu > div,
#navleft > ul > li.el-menu-item{
    width: 100%;
    display: flex;
    justify-content:flex-start!important;
    align-items: center;
    height: 30px;
}
#navleft > ul > li.el-menu-item{
    padding-left:50px;
    font-size: 14px;
}
#navleft > ul > li > div > span{
    margin-left: 0;
}
#navleft > ul > li > ul > li,
#navleft > ul > li.el-submenu.is-active.is-opened > ul > li > ul > li{
    font-size: 12px;
    text-align: left;
    height: 30px;
    display: flex;
    align-items: center;
    padding-left: 49px!important;
}
#navleft > ul > li.el-submenu.is-active.is-opened > ul > li.el-menu-item.is-active,
#navleft > ul > li.el-submenu.is-active.is-opened > ul > li.el-submenu.is-active.is-opened > ul > li.el-menu-item.is-active{
    background-color:#108DE9!important ;
}
#navleft > ul > li> div > i.el-icon-s-custom,
#navleft > ul > li:nth-child(2) > div > i.el-icon-s-order,
#navleft > ul > li.el-submenu.is-active.is-opened > div > i.el-icon-s-marketing{
    font-size: 17px!important;
}
#navleft > ul > li.el-submenu.is-active.is-opened > ul > li.el-submenu,
#navleft > ul > li:nth-child(2) > ul > li.el-submenu{
    display: flex;
    flex-direction: column;
    height: auto;
    padding-left: 0!important;
}
#navleft > ul > li:nth-child(2) > ul > li.el-submenu> ul > li,
#navleft > ul > li:nth-child(2) > ul > li.el-submenu > div{
    height: 30px!important;
    width: 100%!important;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    padding-left: 49px!important;
    font-size: 12px;
    text-align: left;
    height: 30px;
    display: flex;
    align-items: center;
    padding-left: 49px!important;
}
#navleft > ul > li.el-menu-item{
    padding-left: 22px!important;
}
</style>