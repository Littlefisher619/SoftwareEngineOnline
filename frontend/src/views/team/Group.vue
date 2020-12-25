<template>
    <div id="team_group">
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
                    <!-- <button @click="tokenvisible=true">查看信息</button> -->
                    <button @click="hwSelect()" v-if="this.homeworkList.length>1">选择作业</button>
                    <!-- <button @click="hwSelect()">选择作业</button> -->
                    <!-- <button @click="homeworkVisible=true">选择作业</button> -->
                    <!-- <button v-show="isleader" @click="rateVisible=true">组内评分</button> -->
                    <!-- <button @click="invite()">邀请成员</button> -->
                </div>
            </div>
            <div class="team_body">
                <el-table
                    :data="result"
                    :max-height="maxheight"
                    height="auto"
                    border
                    stripe
                    fit
                    style="width: 100%">
                    <el-table-column
                    type="index"
                    label="序号"
                    width="100">
                    </el-table-column>
                    <el-table-column
                    label="团队分工"
                    width="140">
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
                    prop="username"
                    label="用户名">
                    </el-table-column>
                    <el-table-column
                    v-if="israte"
                    prop="rate"
                    label="权重">
                    </el-table-column>
                </el-table>
            </div>
            <div class="team_footer" v-if="!israte&&role!=0">
                <div class="team_footer_inner">
                    <div class="tips">Tips:当前作业仍未对小组成员进行评分,请组长进行评分</div>
                    <button class="pingfen_button" @click="rateVisible=true">立即评分</button>
                </div>
            </div>
        </div>
        <!-- 创建团队 -->
        <el-dialog
        title="创建团队"
        :visible.sync="createvisible"
        width="30%">
        <input class="team_create_input" v-model="teamname" placeholder="输入队伍名称">
        <div class="create_tips">注:创建队伍将成为团队队长且不能更改,可通过链接邀请他人加入队伍</div>
        <button class="create_button" @click="createTeam()">确认创建</button>
        </el-dialog>
        <!-- 加入队伍 -->
        <el-dialog
        title="加入团队"
        :visible.sync="joinvisible"
        width="30%">
        <input class="team_create_input" placeholder="输入队伍id" v-model="groupid">
        <button class="create_button" @click="handleClose">确认加入</button>
        </el-dialog>

        <!-- 生成链接 -->
        <el-dialog
        :title="result[0]?result[0].groupname:1"
        :visible.sync="invitedia"
        width="30%">
        <div class="success_tips">链接生成成功，快去邀请其他人加入</div>
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

        
        <!-- 组内评分 -->
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
                    class="rate_input"
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

        <!-- 作业选择弹窗 -->
        <el-dialog
        :append-to-body="true" 
        class="team_couple"
        :visible.sync="homeworkVisible">
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
        <el-dialog
        :visible.sync="taskVisible"
        width="30%"
        class="homework_list">
        <task-swiper :result="homeworkList" @childFn="parentFn"></task-swiper>
        </el-dialog>
    </div>
</template>
<script>
import {getUrlKey} from '../../assets/utils.js'
import taskSwiper from '../../components/TaskSwiper.vue'
import { Loading } from 'element-ui';
export default {
    components:{
        'task-swiper':taskSwiper,
    },
    data(){
        return{
            result:[],
            createvisible:false,
            joinvisible:false,
            teamname:"",
            homeworkName:"",
            teamlink:"圆圆圆",
            groupname:"",
            maxheight:"90%",
            groupid:"",
            invitedia:false,
            tokenvisible:false,
            token:"",
            rateVisible:false,
            isleader:false,
            memberscore:[],
            homeworkVisible:false,
            taskVisible:false,
            homeworkList:[],
            nowHomework:"",
            israte:false,
            loading:"",
            homeworktype:2,
        }
    },
    methods:{
        getlist(){
            this.loading= Loading.service({ fullscreen: true })
            this.$api.homework.getlist(this.homeworktype).then(response=>{
                let res=response.data;
                if(res!=undefined){
                    this.homeworkList=res.results.filter(item=>item.homeworktype==2);
                    this.nowHomework=this.homeworkList[0].id;
                }
                else{
                    this.homeworkList=[];
                }
                this.getteam();
            })
        },
        showcreate(){
            this.createvisible=true
        },
        showjoin(){
            this.joinvisible=true
        },
        createTeam(){
            let param={
                "grouptype": 2,
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
                    let str=`https://seonline.littlefisher.me/team/group?${param}`
                    this.teamlink=str
                    this.getteam();
                }
            })
        },
        onCopy() {
            this.$message({
                message: '复制成功',
                type: 'success'
            });
        },
        onError() {
        this.$message.error('复制失败');
        },
        getteam(){
            this.result=[];
            this.israte=false;
            this.maxheight="90%"
            this.loading= Loading.service({ fullscreen: true })
            this.$api.user.mygroup().then(response=>{
                let res=response.data.big
                this.groupid=res.id
                this.memberscore=[];
                let param={
                    "group":this.groupid,
                }
                if(this.nowHomework!=""){
                    param.homework=this.nowHomework;
                    let result=this.homeworkList
                    let homeworkName=result.filter(x=>x.id==this.nowHomework)
                }
                this.$api.score.getrate(param).then(response=>{
                    this.loading.close();
                    let res1=[];
                    if(response.data.results[0]){
                        res1=response.data.results[0].ratedetail
                        this.israte=true;
                        console.log(this.israte)
                        this.maxheight="100%"
                    }
                    this.groupname=res.groupname;
                    this.groupid=res.id
                    let leader=res.leader
                    if(leader.stuid==this.$store.getters.stuid&&leader.id==this.$store.getters.id&&leader.stuname==this.$store.getters.stuname){
                        this.isleader=true
                    }
                    this.token=res.token
                    let result=res.member_detail
                    result.unshift(leader)
                    this.result=result
                    result.forEach(item => {
                        let obj={...item,"rate":""}
                        this.memberscore.push(obj);
                    });
                    if(res1.length>0){
                        for(let i in res1){
                            for(let j in this.result){
                                if(this.result[j].id==res1[i].member){
                                    if(res1[i].rate!=null){
                                        this.israte=true
                                    }
                                    else{
                                        this.israte=false
                                        this.maxheight="90%"
                                    }
                                    this.result[j].rate=res1[i].rate
                                }
                            }
                        }
                    }
                })
            })
        },
        hwSelect(){
            this.taskVisible=true;
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
                    "homework": this.nowHomework,
                    "group":this.groupid,
                    "ratedetail":arr
                }
                console.log(param)
                this.$api.score.rateCreate(param).then(res=>{
                    console.log(res);
                    this.rateVisible=false;
                    this.getteam();
                }).catch(err=>{
                    console.log(err.response)
                })
            }
        },
        invite(){
            let param=encodeURIComponent(`join=1&groupid=${this.groupid}`)
            let str=`https://seonline.littlefisher.me/team/group?${param}`
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
            this.$message.error(str);
        },
        open4(str) {
            this.$message.error(str);
        },
        open2(str) {
            this.$message({
            message: str,
            type: 'success'
            });
        },

        numberChange(val, index) {
            let integer = /^(-|\+)?\d+$/;
            if (integer.test(val)) {
                if(parseInt(val)>=this.scorerules[index].max)
                this.scorerules[index].score=this.scorerules[index].max
            }
        },

        parentFn(homeworkid){
            if(homeworkid!=this.homeworkid){
                console.log(homeworkid)
                this.nowHomework=homeworkid
                this.getteam();
            }
            this.taskVisible=false;
        }
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
        },
        role(){
            return this.$store.getters.role;
        }
    },
    created(){
        let join= getUrlKey('join')
        let groupid=getUrlKey('groupid')
        if(join==null||groupid==null){
            this.getlist();
            // this.getteam();
            // this.$forceUpdate();
        }
        else if(join==1&&groupid!=null){
            this.groupid=groupid
            this.joinvisible=true
        }
    },

}
</script>
<style scoped>
button{
    cursor: pointer;
}
#team_group{
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
    position: relative;
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
/* 表格 */
.team_body{
    width: 96%;
    box-sizing: border-box;
    margin-top: 1.5%;
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

/* 底部评分 */
.team_footer{
    width: 100%;
    height: 8%;
    position: absolute;
    bottom: 3%;
    box-sizing: content-box;
}
.team_footer_inner{
    width: 100%;
    height: 100%;
    position: relative;
    display: flex;
    padding-left: 4%;
    align-items: center;
    box-sizing:content-box;
}
.pingfen_button{
    background: #159BD5;
    color: white;
    border: 0;
    width: 120px;
    height: 34px;
    position: absolute;
    right: 8%;
}
</style>
<style>
#team_group > div.el-dialog__wrapper{
    display: flex;
    justify-content: center;
    align-items: center;
}
#team_group > div.el-dialog__wrapper > div > div.el-dialog__body{
    padding: 0!important;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
#team_group > div.el-dialog__wrapper > div > div.el-dialog__header{
    height: 50px!important;
    padding: 0!important;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: center;
}
#team_group > div.el-dialog__wrapper > div > div.el-dialog__body{
    height: 150px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    box-sizing: content-box;
    padding-top: 4%!important;
    align-items: center;
}
#team_group > div.el-dialog__wrapper > div > div.el-dialog__header > button > i{
    display: none;
}
#team_group > div > div > div.el-dialog__header > span{
    font-weight: bold;
}
.el-input-number .el-input__inner{
    padding-left: 10px!important;
    padding-right: 0!important;
    text-align: left;
}
#team_group > div:nth-child(5) > div > div.el-dialog__header,
#team_group > div.el-dialog__wrapper.homework_list > div > div.el-dialog__header{
    display: none;
}
#team_group > div:nth-child(5) > div > div.el-dialog__body{
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
#team_group > div.el-dialog__wrapper.homework_list > div > div.el-dialog__body{
    padding-top: 0!important;
    height: 100%!important;
}
#team_group > div.team_group_list > div.team_body{
    height: 84%!important;
    /* overflow-y: scroll;
    overflow-x: hidden; */
}
.rate_input{
    width: 80%!important;
}
#task_swiper > div.homework_list > div > div.swiper-wrapper{
    /* background: #f8f8f8; */
    width: 300px!important;
    height: 200px!important;
}
#task_swiper > div.homework_list > div> div.swiper-wrapper>div{
    width: 100%;
    height: 100%;
}
</style>