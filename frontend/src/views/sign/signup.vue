<template>
    <div id="signup">
        <div class="signup_box">
            <div class="signup_box_inner" @keyup.enter="signup">
                <div class="signup_box_title">软工评测平台</div>
                <div class="signup_box_input">
                    <div class="signup_input_lable">用户名：</div>
                    <input v-model="form.username">
                </div>
                <div class="signup_box_input">
                    <div class="signup_input_lable">姓名：</div>
                    <input v-model="form.stuname">
                </div>
                <div class="signup_box_input">
                    <div class="signup_input_lable">学号：</div>
                    <input v-model="form.stuid">
                </div>
                <div class="signup_box_input">
                    <div class="signup_input_lable" placeholder="">邮箱：</div>
                    <input v-model="form.email">
                </div>
                <div class="signup_box_input">
                    <div class="signup_input_lable">设置密码：</div>
                    <input v-model="form.password" type="password">
                </div>
                <div class="signup_box_input">
                    <div class="signup_input_lable">再次确认：</div>
                    <input v-model="form.repassword" type="password"
                    >
                </div>

                <div class="signup_box_link">
                    <router-link to="/sign">已有账号，登陆</router-link>
                </div>
                <div class="signup_box_button">
                    <button @click="signup()">确认注册</button>
                </div>
            </div>
            <!-- <el-alert
                title="注册成功"
                type="success">
            </el-alert> -->
        </div>
    </div>
</template>
<script>
export default {
    data(){
        return{
            form:{
                username:"",
                password:"",
                email:"",
                stuid:"",
                stuname:"",
                repassword:"",
            }
        }
    },
    methods:{
        signup(){
            let result=this.form
            let flag=1;
            for(let item in result){
                if(result[item]==""||result[item]==" "){
                    flag=0
                }
            }
            if(result.password!=result.repassword){
                flag=2
            }
            if(flag==1){
                let param={
                    "username":this.form.username,
                    "password":this.form.password,
                    "email":this.form.email,
                    "stuid":this.form.stuid,
                    "stuname":this.form.stuname,
                }
                this.$api.user.signup(param).then(Response=>{
                    let res=Response.data;
                    this.$router.push({
                        path:'/sign'
                    })
                }).catch(err=>{
                    let errData=err.response.data;
                    for(let item in errData){
                        if(errData[item][0]=="请输入合法的邮件地址。"){
                            this.open4("请确保输入合法的邮箱地址");
                            break;
                        }
                        if(errData[item][0]=="请确保这个字段至少包含 6 个字符。")
                        {
                            this.open4("请确保密码至少包含 6 个字符。")
                            break;
                        }
                        if(errData[item][0]=="用户名已经被注册了"){
                            this.open4("用户名已经被注册了")
                            break
                        }
                        if(errData[item][0]=="邮箱已经被注册了"){
                            this.open4("邮箱已经被注册了")
                            break
                        }
                }
                })
            }
            else if(flag==0){
                this.open4("请确认信息都已填写")
            }
            else if(flag==2){
                this.open4("两次输入的密码不一致")
            }
            
        },
        open4(err) {
            this.$message.error(err);
        }
    }
}
</script>
<style scoped>
#signup{
    width: 100%;
    height: 100%;
    background-image: url('../../assets/images/background.jpg');
    background-size: cover;
    -webkit-background-size: cover;
    -moz-background-size: cover;
    -o-background-size: cover;
    background-position: bottom;
    background-repeat: no-repeat;
    position: relative;
}
.signup_box{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%,-50%);
    width: 30%;
    height: 70%;
    background-color:  rgba(255, 255, 255, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    min-width: 340px;
}
.signup_box_inner{
    width: 90%;
    height: 90%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.signup_box_title{
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 2%;
}
.signup_box_input{
    height: 8%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    margin-top: 2%;
}
.signup_input_lable{
    width: 25%;
    text-align: right;
    height: 100%;
    font-size: 15px;
    min-width: 80px;
}
.signup_box_input>input{
    height: 100%;
    width: 65%;
    background-color: rgba(255, 255, 255, 0.2);
    border: 1px solid rgb(227, 227, 227);
    box-sizing:border-box;
    outline: none;
}
.verification_code{
    height: 100%;
    width: 65%;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}
.verification_code>input{
    background-color: rgba(255, 255, 255, 0.2);
    width: 60%;
    height: 100%;
    border: 1px solid rgb(227, 227, 227);
    box-sizing:border-box;
    outline: none;
}
.verification_code>button{
    margin-left: 2%;
    width: 38%;
    height: 100%;
    background-color: #139CD4;
    color: #ffffff;
    border: 0;
    padding: 0;
    outline: none;
}
.signup_box_link{
    width: 80%;
    font-size: 13px;
    margin-top: 1%;
    margin-bottom: 2%;
    text-align: right;
}
.signup_box_button{
    width: 100%;
    height: 9%;
}
.signup_box_button>button{
    background-color: #139CD4;
    color: #ffffff;
    border: 0;
    width: 30%;
    height: 100%;
    font-size: 13px;
    border-radius: 4px;
    outline: none;
}
.signup_box_input>.err_input{
    /* border: 1px solid red; */
}

.err_input::placeholder{
    /* color: red; */
}
</style>