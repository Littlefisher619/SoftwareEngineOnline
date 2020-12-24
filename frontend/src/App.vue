<template>
  <div id="app">
    <div v-if="!$route.meta.keepAlive" class="nav_keeplive">
        <navLeft class="nav_bar_left"></navLeft>
        <div class="right_body">
          <nav-top class="nav_top"></nav-top>
          <div class="right_content"><router-view class="view_content"></router-view></div>
        </div>
    </div>
    <router-view :key="$route.path + $route.query.t" v-if="$route.meta.keepAlive" class="routerView" />
  </div>
</template>
<script>
import navLeft from './components/NavLeft.vue'
import navTop from './components/NavTop'
export default {
    components:{
      'navLeft':navLeft,
      'nav-top':navTop,
    },
    data(){
      return{
      }
    },
    methods:{
      getme(){
        if(this.$route.name!='signin'&&this.$route.name!='signup'){
          this.$api.user.information().then(response=>{
                let res=response.data;
                this.$store.dispatch('setinfo',res);
            }).catch(err=>{
                console.log(err.response)
            })
          }
        }
    },
    created(){
      this.getme();
    }
}
</script>
<style>
body,html{
  margin: 0;
  padding: 0;
  color: #314659;
  font-family: Lato,"PingFang SC","Microsoft YaHei",sans-serif;
  font-size: 14px;
  font-weight: 300;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  width: 100vw;
  height: 100vh;
}

#nav {
  padding: 30px;
}

a {
  color: #2c3e50;
  text-decoration: none;
}
button{
  outline: none;
  cursor: pointer;
  border: 0;
}
button:hover{
  opacity:0.8;
}
.nav_keeplive{
  display: flex;
  flex-direction: row;
  height: 100%;
}
.nav_bar_left{
  position: absolute;
  width: 14%;
  min-width: 200px;
  height: 100%;
  min-height: 578px;
  left: 0;
  top: 0;
  background-color: #f6f6f6;
}
.right_body{
  width: 86%;
  height: 100%;
  min-height: 578px;
  position: relative;
  margin-left: 14%;
  background: #f0f2f5;
  overflow-x: hidden;
}
@media screen and (max-width: 1430px) {
    .right_body{
      margin-left: 200px;
    }
}
.nav_top{
  width: 100%;
  height: 7.5%;
  min-height: 58px;
  position: relative;
  background: #ffffff;
}
.right_content{
  position: relative;
  width: 100%;
  height: 92.5%;
  background: #f5F5F5;
  display: flex;
  justify-content: center;
  align-items: center;
}
.view_content{
  position: absolute;
  width: 98%;
  box-sizing: content-box;
  height: 96%;
  background-color: #ffffff;
}
@media screen and (max-height:773.4px) {
  .right_content{
      height: 89%;
    }
}
</style>
<style>
.el-input-number{
  width: 80%!important;
}
.el-input-number .el-input__inner{
    padding-left: 10px!important;
    padding-right: 0!important;
    text-align: left;
}
span.el-input-number__decrease,
span.el-input-number__increase{
    display: none!important;
}
</style>
