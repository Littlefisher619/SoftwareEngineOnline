<template>
    <div id="score_judge">
        {{this.total}}
        <div class="score_box">
            <el-table
                border
                stripe
                fit
                :data="result">
                <el-table-column
                type="index"
                width="80"
                label="序号">
                </el-table-column>
                <el-table-column
                label="作业类型">
                    <el-tag type="success" v-if="this.homeworktype==0">单人作业</el-tag>
                    <el-tag v-if="this.homeworktype==1">结对作业</el-tag>
                    <el-tag type="warning" v-if="this.homeworktype==2">团队项目</el-tag>
                </el-table-column>
                <el-table-column
                prop="groupname"
                label="团队名称">
                </el-table-column>
                <el-table-column
                prop="id"
                label="团队id">
                </el-table-column>
                <el-table-column
                prop="leader.stuname"
                label="组长">
                    <!-- <el-tag type="info">Admin</el-tag> -->
                </el-table-column>
                <el-table-column
                width="260">
                <template slot="header" slot-scope="scope">
                    <div class="header_search_input">
                        <el-input placeholder="输入关键字搜索"
                         v-model="search"
                         size="small"
                         class="input-with-select"
                         @keyup.enter.native="scoreSearch()">
                            <el-select v-model="type" 
                            slot="prepend">
                            <el-option
                            v-for="item in select"
                            :key="item.value"
                            :label="item.lable"
                            :value="item.value"
                            ></el-option>
                            </el-select>
                            <el-button slot="append" icon="el-icon-search" @click="scoreSearch()"
                            @keyup.enter="scoreSearch()"></el-button>
                        </el-input>
                <!-- <el-input-number :controls="false" v-model="scope.row.name" 
                    :precision="1" :step="0.5" :max="100" :min="0"
                    placeholder="输入评分/100">
                    </el-input-number> -->
                    </div>
                </template>


                <!-- 评分 -->
                <template slot-scope="scope">
                    <el-button type="primary" plain  @click="showpoint(scope.$index)">点击评分</el-button>
                </template>
                </el-table-column>
            </el-table>
            
            <!-- 分页 -->
            <div class="pagination">
                <el-pagination
                background
                layout="prev, pager, next"
                :total="this.pages.count"
                :page-size="20"
                hide-on-single-page
                :current-page="currentpage"
                @current-change="handleCurrentChange"
                >
                </el-pagination>
            </div>
        </div>


        <!-- 评分弹窗 -->
        <el-dialog
        :visible.sync="dialogVisible"
        :append-to-body="true" 
        width="30%">
        <div class="dia_header">
            <div>分点评分</div>
            <div class="score_total">
                <span>总分:</span>
                <span>{{this.totalScore}}</span>
            </div>
        </div>
        <el-table
            :data="scorerules"
            style="width: 100%">
            <el-table-column
            prop="point"
            label="评分点"
            width="100">
            </el-table-column>
            <el-table-column
            prop="description"
            width="280"
            label="评分细则">
            </el-table-column>
            <el-table-column
            label="评分">
            <template slot-scope="scope">
                <el-input v-model="scope.row.score" 
                 @input="numberChange($event,scope.$index)"
                @change="numberChange($event,scope.$index)">
                </el-input>
                /{{scope.row.max}}
            </template>
            </el-table-column>
        </el-table>
        <div class="dia_button">
           <div  class="bonus">
               <div>加成</div>
               <el-input-number size="small" :precision="2" v-model="bonus" :max="1" :min="-1"></el-input-number>
               <div class="bonus_tips">tips:百分数</div>
            </div>
            <button @click="judge()">确定评分</button>
        </div>
        </el-dialog>
    </div>
</template>
<script>
export default {
    name:"scorecouple",
    data(){
        return{
            bonus:0,
            pages:{},
            currentpage:1,
            result:[
            ],
            search: '',
            dialogVisible: false,
            homeworkid:1,
            homeworktype:0,
            scorerule:[],
            homework:{},
            index:"",
            scorerules: [],
            scoredetail: {},
            select:
            [{
                lable:"姓名",
                value:"stuname"
            },
            {
                lable:"学号",
                value:"stuid",
            },
            {
                lable:"id",
                value:"id",
            }
            ],
            type:"1",
        }
    },
    methods:{
        gethomework(){
            this.$api.homework.getlist().then(response=>{
                let res=response.data;
                if(res!=undefined){
                    let homework=res.results.filter(item=>item.id==this.homeworkid)[0];
                    this.homework=JSON.parse(JSON.stringify(homework))
                }
                else{
                    this.homework={};
                }
            })
        },
        getselect(){
            if(this.homeworktype==0){
                this.select=[{
                    lable:"姓名",
                    value:"stuname"
                },
                {
                    lable:"学号",
                    value:"stuid",
                },
                {
                    lable:"UID",
                    value:"uid",
                }
                ];
            }
            else if(this.homeworktype==1||this.homeworktype==2){
                this.select=[{
                    lable:"组长",
                    value:"leader_stuname"
                },
                {
                    lable:"组名",
                    value:"groupname",
                },
                {
                    lable:"GID",
                    value:"gid",
                }
                ];
            }
            this.type=this.select[0].value
        },
        getlist(){
            let param={
                "page":this.currentpage,
            }
            this.$api.homework.tasklist(this.homeworkid,param).then(response=>{
                let res=response.data;
                this.pages={
                    "count": res.count,
                    "next": res.next,
                    "previous": res.previous,
                }
                this.result=res.results
                this.result.map( x=> {return (x.id,x.groupname,x.leader)})
                // this.result=JSON.parse(JSON.stringify(this.result));
            })
        },
        judge(){
            let results=JSON.parse(JSON.stringify(this.scorerules));
            let msg=this.result[this.index];
            for(let item in results){
                delete results[item].max
                delete results[item].description
                results[item].score=parseInt(results[item].score)
            }
            let result={"scorepoints":results,"score":this.score1,"bonus":this.bonus}
            let params={
                "student": this.homeworktype==0?msg.id:null,
                "group":this.homeworktype==0?null:msg.id,
                "homework": parseInt(this.homeworkid),
                "scoredetail":result,
                "totalscore":this.totalScore
            }
            params.scoredetail.score=this.totalScore;
            this.dialogVisible=false
            this.$api.score.createjudge(params).then(responese=>{
                let result=this.result
                result.splice(this.index,1)
                let length=result.length
                this.result=result.slice(0,length);
                for(let item in this.scorerules){
                    this.scorerules[item].score=""
                }
                this.$forceUpdate()
            }).catch(err=>{
                console.log(err)
            })
        },
        showpoint(index){
            this.dialogVisible=true;
            this.index=index
            this.scorerules=this.homework.scorerules
        },
        handleCurrentChange(currentpage){
            this.currentpage=currentpage
            this.getlist();
        },
        getid(){
            this.homeworkid=this.$route.query.homeworkid;
            this.homeworktype=this.$route.query.homeworktype;
            this.getselect();
        },       
        numberChange(val, index) {
            let integer = /^(-|\+)?\d+$/;
            if (integer.test(val)) {
                if(parseInt(val)>=this.scorerules[index].max)
                this.scorerules[index].score=this.scorerules[index].max
            }
        },
        scoreSearch(){
            let obj
            if(this.type=="uid"||this.type=="gid"){
                obj={"id":this.search}
            }
            else{
                let type=this.type
                obj={
                    [type]:this.search
                }
            }
            this.$api.homework.tasklist(this.homeworkid,obj).then(response=>{
                let res=response.data;
                let flag=0;
                for(let i=0;i<this.result.length;i++){
                    if(this.result[i].stuid==res.results[0].stuid){
                        this.result.splice(i,1);
                        flag=1;
                        i=this.result.length
                    }
                }
                this.result.unshift(res.results[0])
                if(flag==0){
                this.result.splice(this.result.length-1,1)}
                // this.result=JSON.parse(JSON.stringify(this.result));
            })
        }

    },
    computed:{
        totalScore:function(){
            let sum=0;
            let data=this.scorerules;
            for(let item in data){
                if(data[item].score!=""&&data[item].score!="-"&&data[item].score!=undefined){
                    sum+=parseInt(data[item].score)
                }
                if(typeof(data[item].score==undefined)){
                    sum+=0;
                }
            }
            // sum*=(1+this.bonus)
            return sum;
        },
        score1:function(){
            let sum=0;
            let data=this.scorerules;
            for(let item in data){
                if(data[item].score!=""&&data[item].score!="-"){
                    sum+=parseInt(data[item].score)
                }
                if(typeof(data[item].score)==undefined){
                    sum+=0;
                }
            }
            sum*=(1+this.bonus)
            return sum;
        },
    },
    created(){
        this.getid()
        this.gethomework();
        this.getlist();
    }
}
</script>
<style scoped>
#score_judge{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding-top: 2%;
    box-sizing: content-box;
}
.score_box{
    width: 94%;
    height: 94%;
}
.dia_button{
    width: 100%;
    height: 35px;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    margin-top: 10px;
}
.dia_button>button{
    width: 20%;
    height: 100%;
    background: #64B0FE;
    color: #ffffff;
    border: 0;
    margin: 20px 0;
}
.bonus{
    position: absolute;
    left: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.bonus>div{
    width: 50px;
    margin-right: 10px;
}
.bonus_tips{
    width: 100px!important;
}
.pagination{
    width: 100%;
    margin-top: 14px;
    margin-bottom: 30px;
}
.header_search_input{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    height: 48px;
}
</style>
<style>
body > div.el-dialog__wrapper > div .el-input{
  width: 80%!important;
}
body > div.el-dialog__wrapper > div .el-input .el-input__inner{
    padding-left: 10px!important;
    padding-right: 0!important;
    text-align: left;
}
body > div.el-dialog__wrapper > div{
    width: 600px!important;
}
body > div.el-dialog__wrapper > div > div.el-dialog__header{
    padding-bottom: 0px!important;
    display: none!important;
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
body > div.el-dialog__wrapper > div > div.el-dialog__body{
    padding-top: 4px!important;
    padding-bottom: 10px;
}
body > div.el-dialog__wrapper > div > div.el-dialog__header > button > i{
    display: none;
}
body > div.el-dialog__wrapper > div > div.el-dialog__body > div.dia_button > div > div.el-input-number.el-input-number--small{
    width: 100px!important;
}
body > div.el-dialog__wrapper > div > div.el-dialog__body > div.dia_button > div > div.el-input-number.el-input-number--small > div > input,
body > div.el-dialog__wrapper > div > div.el-dialog__body > div.dia_button > div > div.el-input-number.el-input-number--small > div{
    width: 100%!important;
}
#score_judge > div.score_box > div.el-table.el-table--fit.el-table--striped.el-table--border.el-table--enable-row-hover.el-table--enable-row-transition > div.el-table__header-wrapper > table > thead > tr > th.el-table_1_column_8.is-leaf > div > div > div > div.el-input-group__prepend{
    width: 10%;
}
#score_judge > div.score_box > div.el-table.el-table--fit.el-table--striped.el-table--border.el-table--enable-row-hover.el-table--enable-row-transition > div.el-table__header-wrapper > table > thead > tr > th.el-table_1_column_8.is-leaf > div > div > div > div.el-input-group__prepend > div > div.el-input.el-input--suffix > span{
    left: 0!important;
}
#score_judge > div.score_box > div.el-table.el-table--fit.el-table--striped.el-table--border.el-table--enable-row-hover.el-table--enable-row-transition > div.el-table__header-wrapper > table > thead > tr > th.el-table_1_column_8.is-leaf{
    padding:0;
}
#score_judge > div.score_box > div.el-table.el-table--fit.el-table--striped.el-table--border.el-table--enable-row-hover.el-table--enable-row-transition > div.el-table__header-wrapper > table > thead > tr > th.el-table_1_column_8.is-leaf > div.cell{
    height: 100%!important;
}
#score_judge > div.score_box > div.el-table.el-table--fit.el-table--striped.el-table--border.el-table--enable-row-hover.el-table--enable-row-transition > div.el-table__body-wrapper.is-scrolling-none > table > tbody > tr > td> div > button{
    width: 60%;
}

body > div.el-dialog__wrapper > div > div.el-dialog__body > div.el-table.el-table--fit.el-table--enable-row-hover.el-table--enable-row-transition > div.el-table__body-wrapper.is-scrolling-none > table > tbody > tr> td> div > div{
    width: 50%!important;
}
#score_judge > div.score_box > div.el-table.el-table--fit.el-table--striped.el-table--border.el-table--enable-row-hover.el-table--enable-row-transition > div.el-table__header-wrapper > table > thead > tr > th.el-table_1_column_8.is-leaf > div > div > div > div.el-input-group__append > button.el-button.el-button--default{
    padding-left: 6px!important;
    padding-right: 6px!important;
}

body .el-table th.gutter {
    display: table-cell !important
}
</style>