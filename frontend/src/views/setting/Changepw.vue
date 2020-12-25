<template>
    <div id="changepw">
        <div class="changepw">
            <div class="changepw_head">{{this.$route.meta.name}}</div>
            <div class="changepw_box">
                <div class="change_input">
                    <div class="input_lable">旧密码</div>
                    <input type="password" placeholder="6-16位的密码，区分大小写" v-model="password">
                </div>
                <div class="change_input">
                    <div class="input_lable">新密码</div>
                    <input type="password" placeholder="6-16位的密码，区分大小写" v-model="newpassword">
                </div>
                <div class="change_input">
                    <div class="input_lable">确认新密码</div>
                    <input type="password" placeholder="6-16位的密码，区分大小写" v-model="repassword">
                </div>
                <div class="change_input change_button">
                    <button @click="changePw()">确认修改</button>
                </div>
            </div>
        </div>
        <el-dialog
        :visible.sync="issucess">
        <div class="duigou">
            <duigou :tips="tips"></duigou>
            <button class="sucess_button" @click="shut()">确定</button>
        </div>
        </el-dialog>
    </div>
</template>
<script>
export default {
    data(){
        return{
            issucess:false,
            password:"",
            newpassword:"",
            repassword:"",
            tips:"修改成功"
        }
    },
    methods:{
        changePw(){
            let param={
                "password":this.repassword
            }
            this.$api.user.updatepassword(param).then(response=>{
                let res=response.data;
                console.log(res);
                this.issucess=true
            }).catch(err=>{
                console.log(err)
            })
        },
        shut(){
            this.issucess=false;
        }
    }
}
</script>
<style scoped>
input{
    outline: none;
}
#changepw{
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
}
.changepw{
    width: 100%;
    height: 100%;
    position: absolute;
}
.success_tips{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.3);
}
.duigou{
    width: 200px;
    height: 200px;
    background: #ffffff;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%,-50%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items:center;
}
.sucess_button{
    width: 30%;
    height: 14%;
    border: 0;
    background: #169BD5;
    color: #ffffff;
    border-radius: 3px;
}
.changepw_head{
    width: 100%;
    text-align: left;
    box-sizing: content-box;
    padding-left: 4%;
    font-size: 20px;
    font-weight: 500;
    padding-top: 2%;
}
.changepw_box{
    width: 80%;
    height: 90%;
    margin: 2% auto;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    min-width: 400px;
}
.change_input{
    width:60%;
    display: flex;
    flex-wrap: nowrap;
    align-items: center;
    justify-content: center;
    height: 6.5%;
    margin-top: 3%;
    min-width: 300px;
}
.change_input>.input_lable{
    width: 40%;
    height: 100%;
    text-align: right;
}
.change_input>input{
    width: 55%;
    height: 100%;
    margin-left: 4%;
    border: 1px solid #c4b7b7;
    border-radius: 4px;
    box-sizing: border-box;
    min-width: 200px;
}
.change_button{
    height: 7.5%;
    width: 80%;
}
.change_input>button{
    width: 20%;
    height: 90%;
    background:#63A7FF ;
    border: 0;
    color: #ffffff;
    border-radius: 4px;
    min-width: 100px;
}
</style>
<style>
#changepw > div.el-dialog__wrapper > div{
    width: 300px;
    height: 200px;
}
#changepw > div.el-dialog__wrapper{
    display: flex;
    flex-direction: column;
    justify-content: center;
}
#changepw > div.el-dialog__wrapper > div > div.el-dialog__header > button > i{
    display: none;
}
</style>