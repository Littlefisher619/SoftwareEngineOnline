<template>
    <div id="team_couple">
        <div class="team_group_box" v-if="!result[0]">
            <c-head></c-head>
            <div class="team_group_none">
                <div><i class="iconfont icon-tuanduisvg"></i></div>
                <button @click="showcreate()">立即创建</button>
                <button @click="showjoin()">加入队伍</button>
            </div>
        </div>
        <div class="team_group_list" v-if="result[0]">
            <div class="team__head">
                <div class="team__head_line"></div>
                <div class="team_head_route">
                    {{this.$route.meta.parentName}}-{{this.groupname}}
                </div>
                <div class="team_head_button">
                    <button @click="tokenvisible=true">查看信息</button>
                    <!-- <button @click="invite">邀请成员</button> -->
                    <!-- <button v-show="isleader" @click="rateVisible=true">组内评分</button> -->
                </div>
            </div>
            <div class="team_body">
                <el-table
                    :data="result"
                    border
                    stripe
                    fit
                    style="width: 100%">
                    <el-table-column
                    type="index"
                    label="序号"
                    width="80">
                    </el-table-column>
                    <el-table-column
                    label="团队分工"
                    width="120">
                    <template slot-scope="scope">
                        <el-tag type="success" v-if="scope.$index==0">组长</el-tag>
                        <el-tag v-if="scope.$index!=0">组员</el-tag>
                    </template>
                    </el-table-column>
                    <el-table-column
                    prop="stuname"
                    label="姓名"
                    width="160">
                    </el-table-column>
                    <el-table-column
                    prop="stuid"
                    label="学号">
                    </el-table-column>
                    <el-table-column
                    prop=".username"
                    label="用户名">
                    </el-table-column>
                </el-table>
            </div>
        </div>
        <!-- 创建团队 -->
        <el-dialog
        title="创建团队"
        :visible.sync="createvisible"
        width="30%">
        <input class="team_create_input" v-model="teamname" placeholder="输入队伍名称">
        <div class="create_tips">注:创建队伍将成为团队队长且不能更改,可通过链接邀请他人加入队伍</div>
        <!-- <button class="create_button" @click="createTeam()">确认创建</button> -->
        </el-dialog>
        <!-- 加入队伍 -->
        <el-dialog
        title="加入团队"
        :visible.sync="joinvisible"
        width="30%">
        <input class="team_create_input" placeholder="输入队伍名称"  v-model="groupid">
        <button class="create_button" @click="handleClose">确认加入</button>
        </el-dialog>

        <!-- 生成链接 -->
        <el-dialog
        :title="result[0]?result[0].groupname:1"
        :visible.sync="invitedia"
        width="30%">
        <div class="success_tips">链接生成成功，快去分享吧</div>
        <div class="create_success_link"><input  v-model="teamlink" readonly="true">
        <button
        v-clipboard:copy="teamlink" 
        v-clipboard:success="onCopy"
        v-clipboard:error="onError">复制链接</button>
        </div>
        </el-dialog>
        <!-- 查看token -->
        <el-dialog
        :visible.sync="tokenvisible"
        width="30%">
        <div class="success_tips team_info_head">队伍信息</div>
        <div class="create_success_link"><input  v-model="token" readonly="true">
        <button
        v-clipboard:copy="token" 
        v-clipboard:success="onCopy"
        v-clipboard:error="onError">复制token</button>
        </div>
        <div class="create_success_link"><input  v-model="groupid" readonly="true">
        <button
        v-clipboard:copy="groupid" 
        v-clipboard:success="onCopy"
        v-clipboard:error="onError">复制id</button>
        </div>
        </el-dialog>


        <el-dialog
        :append-to-body="true" 
        class="team_couple"
        :visible.sync="rateVisible">
        <div class="dia_header">
            <div>组内评分</div>
            <div class="score_total">
                <span>剩余权重:</span>
                <span>{{rateLeft}}</span>
            </div>
        </div>
            <el-table
                :data="memberscore"
                border
                style="width: 100%">
                <el-table-column
                label="团队分工">
                <template slot-scope="scope">
                    <el-tag type="success" v-if="scope.$index==0">组长</el-tag>
                    <el-tag v-if="scope.$index!=0">组员</el-tag>
                </template>
                </el-table-column>
                <el-table-column
                prop="stuname"
                label="姓名">
                </el-table-column>
                <el-table-column
                prop="stuid"
                label="学号">
                </el-table-column>
                <el-table-column
                width="180"
                label="权重">
                <template slot-scope="scope" class="rate_input">
                    <el-input v-model="scope.row.rate" 
                    placeholder="百分数"
                    @input="numberChange($event,scope.$index)"
                    @change="numberChange($event,scope.$index)">
                    </el-input>
                    /%
                </template>
                </el-table-column>
            </el-table>
            <div class="team_inside_rate_footer">
                <button class="team_rate_button" @click="createRate()">确认评分</button>
            </div>
        </el-dialog>
    </div>
</template>
<script>
import {getUrlKey} from '../../assets/utils.js'
export default {
    data(){
        return{
            result:[],
            createvisible:false,
            joinvisible:false,
            teamname:"",
            teamlink:"圆圆圆",
            groupname:"",
            groupid:"",
            invitedia:false,
            tokenvisible:false,
            token:"",
            isleader:false,
            rateVisible:false,
            memberscore:[],
        }
    },
    methods:{
        showcreate(){
            this.createvisible=true
        },
        showjoin(){
            this.joinvisible=true
        },
        open4(str) {
            this.$message.error(str);
        },
        createTeam(){
            let param={
                "grouptype": 1,
                "groupname": this.teamname
            }
            this.$api.team.createTeam(param).then(response=>{
                let res=response.data;
                if(res.success==false){
                    this.open4(res.message)
                }
                else if(res.success==true){
                    this.createvisible=false
                    this.groupid=res.data.id
                    this.open2("创建成功")
                    this.invitedia=true
                    let param=encodeURIComponent(`join=1&groupid=${this.groupid}`)
                    let str=`https://seonline.littlefisher.me/team/couple?${param}`
                    this.teamlink=str
                    this.getteam();
                }
            })
        },
        createRate(){
            if(this.rateLeft!=0){
                this.open4("请确保权重之和为100哦")
            }
            else{
                let arr=new Array();
                for(let item in this.memberscore){
                    let obj={
                        "member":this.memberscore[item].id,
                        "rate":parseInt(this.memberscore[item].rate)
                    }
                    arr.push(obj)
                }
                let param={
                    "homework": 2,
                    "group":this.groupid,
                    "ratedetail":arr
                }
                console.log(param)
                this.$api.score.rateCreate(param).then(res=>{
                    console.log(response)
                }).catch(err=>{
                    console.log(err.response)
                })
            }
        },
        onCopy() {
        this.$message({
            message: '复制成功',
            type: 'success',
        });
        },
        onError() {
        this.$message.error('复制失败');
        },
        getteam(){
            this.$api.user.mygroup().then(response=>{
                let res=response.data.double;
                this.groupname=res.groupname;
                let leader=res.leader
                if(leader.stuid==this.$store.getters.stuid&&leader.id==this.$store.getters.id&&leader.stuname==this.$store.getters.stuname){
                    this.isleader=true
                }
                leader.role=1;
                this.token=res.token
                let result=res.member_detail
                this.groupid=res.id
                result.unshift(leader)
                this.result=result;
                // 群成员存入评分点
                result.forEach(item => {
                let obj={...item,"rate":""}
                    this.memberscore.push(obj);
                });
                })
        },
        numberChange(val, index) {
            let integer = /^(-|\+)?\d+$/;
            if (integer.test(val)) {
                if(parseInt(val)>=100)
                this.memberscore[index].rate=100;
            }
        },
        invite(){
            let param=encodeURIComponent(`join=1&&groupid=${this.groupid}`)
            let str=`https://seonline.littlefisher.me/team/couple?${param}`
            this.teamlink=str
            this.invitedia=true
        },
        join(){
            this.$api.team.joinTeam(this.groupid).then(response=>{
                let res=response.data;
                if(res.success==false){
                    this.open4(res.message)
                }
                else if(res.success==true){
                    this.joinvisible=false
                    this.open2("加入成功")
                    this.getteam();
                }
            })
        },
        handleClose(done) {
            this.$confirm('确认加入该队伍？')
            .then(_ => {
                done();
            })
            .catch(_ => {
                this.join()
            });
        },
        open4(str) {
            this.$message. error(str);
        },
        open2(str) {
            this.$message({
            message: str,
            type: 'success'
            });
        },

    },
    computed:{
        rateLeft(){
            let rateLeft=100;
            let data=this.memberscore;
            for(let item in data){
                if(data[item].rate!=""&&data[item].rate!="-"){
                    rateLeft-=parseInt(data[item].rate)
                }
                if(typeof(data[item].rate)==undefined){
                    rateLeft-=0;
                }
            }
            return rateLeft
        }
    },
    created(){
        let join= getUrlKey('join')
        let groupid=getUrlKey('groupid')
        if(join==null||groupid==null){
            this.getteam();
        }
        else if(join==1&&groupid!=null){
            this.groupid=groupid
            this.joinvisible=true
        }
    }
}
</script>
<style scoped>
#team_couple{
    height: 100%;
    width: 100%;
}
.team_group_box,
.team_group_list{
    width: 100%;
    height: 100%;
    position: absolute;
    box-sizing: content-box;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.team_group_none{
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    height: 92%;
}
.icon-tuanduisvg{
    font-size: 160px;
    color: #BFBFBF;
    margin-top: 60px;
}
.team_group_none>button{
    width: 120px;
    height: 40px;
    margin-top: 10px;
    background: #169BD5;
    color: #ffffff;
    border: 0;
}
/* 创建队伍弹窗 */
.team_create_input{
    height: 20%;
    box-sizing: border-box;
    width: 80%;
    border: 0;
    outline: none;
}
.create_tips{
    font-size: 9px!important;
    /* transform: scale(0.9); */
    text-align: left;
    margin-top: 3%;
    color: rgb(121,121,121);
    transform: scale(0.9);
}
.create_button{
    height: 20%;
    width: 25%;
    border: 0;
    background: #63a7ff;
    color: #ffffff;
    border-radius: 5px;
    margin-top: 16px;
}
.dia_header{
    display: flex;
    align-items: center;
    height: 50px;
    position: relative;
    justify-content: flex-start;
    font-weight: bold;
    font-size: 16px;
}
.dia_header>.score_total{
    position: absolute;
    right: 40px;
}
/* 表格 */
.team__head{
    width: 100%;
    display: flex;
    height: 8%;
    align-items: flex-end;
    position: relative;
    box-sizing: content-box;
    padding-left: 3%;
    max-height: 48px;
}
.team__head_line{
    width: 4px;
    height: 60%;
    background: #01284D;
    position: absolute;
    top: 40%;
    border-radius: 1.5px;
}
.team_head_route{
    margin-left: 10px;
    font-size: 18px;
    color: #01284D;
    font-weight: 600;
}
.team_head_button{
    position: absolute;
    right: 6%;
    width: 260px;
    height: 32px;
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
}
.team_head_button>button{
    width: 40%;
    height: 100%;
    background: #159BD5;
    color: #ffffff;
    border: 0;
    outline: none;
    margin-left: 5%;
}

/* 表格 */
.team_body{
    width: 96%;
    box-sizing: border-box;
    margin-top: 1.5%;
}

.success_tips{
    width: 80%;
    height: 20%;
    color: black;
}
.create_success_link{
    width: 80%;
    display: flex;
    align-items: center;
    height: 20%;
    justify-content: center;
    margin-bottom: 10px;
}
.team_info_head{
    font-size: 16px;
    margin-bottom: 4px;
    font-weight: bold;
}
.create_success_link>input{
    width: 60%;
    height: 100%;
    box-sizing: border-box;
}
.create_success_link>button{
    background: #3f3f3f;
    border: 0;
    color: #ffffff;
    width: 25%;
    height: 100%;
    box-sizing: border-box;
    margin-left: 1%;
    cursor: pointer;
}

.team_inside_rate_footer{
    width: 100%;
    height: 20%;
    text-align: right;
    margin-top: 4%;
}
.team_rate_button{
    background: #108DE9;
    height: 100%;
    width:100px;
    min-height: 34px;
    color: #ffffff;
    border: 0;
}
</style>
<style>
#team_couple> div.el-dialog__wrapper{
    display: flex;
    justify-content: center;
    align-items: center;
}
#team_couple > div.el-dialog__wrapper > div{
    background: #f8f8f8;
    min-width: 380px;
    height: 200px;
}
#team_couple > div.el-dialog__wrapper > div > div.el-dialog__body{
    padding: 0!important;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
#team_couple > div.el-dialog__wrapper > div > div.el-dialog__header{
    height: 50px!important;
    padding: 0!important;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: center;
}
#team_couple > div.el-dialog__wrapper > div > div.el-dialog__body{
    height: 150px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    box-sizing: content-box;
    padding-top: 4%!important;
    align-items: center;
}
#team_couple > div.el-dialog__wrapper > div > div.el-dialog__header > button > i{
    display: none;
}
#team_couple > div > div > div.el-dialog__header > span{
    font-weight: bold;
}
span.el-input-number__decrease,
span.el-input-number__increase{
    display: none!important;
}
.el-input-number .el-input__inner{
    padding-left: 10px!important;
    padding-right: 0!important;
    text-align: left;
}
#team_couple > div:nth-child(5) > div > div.el-dialog__header{
    display: none;
}
#team_couple > div:nth-child(5) > div > div.el-dialog__body{
    display: flex;
    flex-direction: column;
    justify-content: center;
}
body > div.el-dialog__wrapper.team_couple > div > div.el-dialog__header{
    display: none;
}
body > div.el-dialog__wrapper.team_couple > div > div.el-dialog__body{
    padding-top: 10px;
    padding-bottom: 20px;
}
body > div.el-dialog__wrapper.team_couple > div{
    min-width:500px;
    width: 50%;
}
body > div.el-dialog__wrapper.team_couple > div > div.el-dialog__header > button > i{
    display: none;
}
body > div.el-dialog__wrapper.team_couple > div > div.el-dialog__body > div.el-table.el-table--fit.el-table--border.el-table--enable-row-hover.el-table--enable-row-transition > div.el-table__body-wrapper.is-scrolling-none > table > tbody > tr > td.el-table_2_column_9 > div > div{
    width: 80%!important;
    height: 60%!important;
}
body > div.el-dialog__wrapper.team_couple > div > div.el-dialog__body > div.el-table.el-table--fit.el-table--border.el-table--scrollable-x.el-table--enable-row-hover.el-table--enable-row-transition > div.el-table__body-wrapper.is-scrolling-left > table > tbody > tr > td.el-table_2_column_9 > div > div > input{
    width: 80%!important;
    height: 60%!important;
}
</style>