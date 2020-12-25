<template>
    <div id="setting">
        <div class="setting_nav">
            <el-menu
            default-active="/setting/info"
            class="setting_navbar"
            @open="handleOpen"
            @close="handleClose"
            active-text-color="#ffffff"
            router>
            <el-menu-item index="/setting/info">
                <span slot="title">基本设置</span>
            </el-menu-item>
            <el-menu-item index="changepw">
                <span slot="title">修改密码</span>
            </el-menu-item>
            </el-menu>
        </div>
        <div class="setting_content">
            <router-view></router-view>
        </div>
    </div>
</template>
<script>
export default {
    data(){
        return{

        }
    },
    methods: {
      handleOpen(key, keyPath) {
        console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      }
    }
}
</script>
<style scoped>
.setting_nav{
    position: absolute;
    width: 180px;
    left: 0;
    height: 100%;
}
.setting_content{
    position: relative;
    margin-left: 180px;
    height: 100%;
}
</style>
<style>
#setting > div.setting_nav > ul{
    height: 100%;
}
#setting > div.setting_nav > ul > li.el-menu-item.is-active{
    background: #55AEEE;
    border-right: 3px solid #108DE9;
}
#setting > div.setting_nav > ul > li.el-menu-item{
    text-align: left;
    padding-left: 40px!important;
}
</style>