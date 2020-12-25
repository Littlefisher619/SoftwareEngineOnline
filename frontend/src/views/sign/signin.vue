<template>
    <div id="signin">
        <div class="signin_box">
            <div class="signin_box_inner" @keyup.enter="login()">
                <div class="signin_box_title">软工评测平台</div>
                <div class="signin_box_input"><input placeholder="学号" v-model="studentNum"></div>
                <div class="signin_box_input"><input placeholder="请输入密码" type="password" v-model="password"></div>
                <div class="signin_box_link">
                    <!-- <span class="signin_to_signup"><router-link to="signup">注册账号</router-link></span> -->
                    <span class="signin_forget_psw"><router-link to="/signup">注册账号</router-link></span>
                </div>
                <div class="signin_box_button">
                    <button @click="login()">登录</button>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    data(){
        return{
            studentNum:"",
            password:"",
        }
    },
    methods:{
        login(){
            if(this.email==""||this.eamil==" "){
                this.open4("用户名不能为空")
            }
            else if(this.password==""||this.password==" "){
                this.open4("密码不能为空")
            }
            else{
                let param={"stuid":this.studentNum,"password":this.password}
                this.$api.user.signin(param).then(Response=>{
                    let res=Response.data;
                    localStorage.setItem('JWT_TOKEN',res.token);
                    this.$router.push({
                        path:'/homework/single'
                    })
                }).catch(err=>{
                    let errdata=err.response.data;
                    for(let item in errdata){
                        this.open4(errdata[item][0])
                        break
                    }
                })
            }
        },
        open4(err) {
            this.$message.error(err);
        }
    }
}
</script>
<style scoped>
#signin{
    width: 100%;
    height: 100%;
    background-image: url('../../assets/images/background.jpg');
    background-size: cover;
    background-position:bottom;
    position: relative;
}
.signin_box{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%,-50%);
    width: 30%;
    height: 50%;
    background-color:  rgba(255, 255, 255, 0.6);
    display: flex;
    justify-content: center;
    align-items: center;
    min-width: 340px;
}
.signin_box_inner{
    width: 80%;
    height: 90%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.signin_box_title{
    font-size: 25px;
    font-weight: 600;
    margin-bottom: 2%;
}
.signin_box_input,
.signin_box_link{
    width: 100%;
    height: 12%;
    position: relative;
    margin-top: 4%;
    display: flex;
    align-items: center;
    font-size: 14px;
}
.signin_box_input>input{
    width: 100%;
    height: 100%;
    border: 2px solid #dfd7d7;
    outline: none;
    padding-left: 4px;
}
.signin_to_signup{
    position: absolute;
    left: 0;
}
.signin_forget_psw{
    position: absolute;
    right: 0;
}
.signin_box_button{
    width: 50%;
    height: 14%;
    display: flex;
    align-items: center;
}
.signin_box_button>button{
    width: 100%;
    height: 100%;
    background: #549bf8;
    color: #ffffff;
    border: 0;
    border-radius: 6px;
    font-size: 14px;
    outline: none;
}
</style>