<template>
    <div id="score_judge">
        <div class="score_box">
            <el-table
            ref="table"
                border
                stripe
                fit
                :data="result"
                @sort-change="sortChange">
                <el-table-column
                prop="uid"
                sortable="custom"
                width="100"
                label="评分id">
                </el-table-column>
                <el-table-column
                width="100"
                label="作业类型">
                    <el-tag type="success" v-if="this.homeworktype==0">单人作业</el-tag>
                    <el-tag v-if="this.homeworktype==1">结对作业</el-tag>
                    <el-tag type="warning" v-if="this.homeworktype==2">团队项目</el-tag>
                </el-table-column>
                <el-table-column
                prop="stuname"
                v-if="this.homeworktype==0"
                label="姓名">
                </el-table-column>
                <el-table-column
                prop="stuid"
                sortable="custom"
                v-if="this.homeworktype==0"
                label="学号">
                </el-table-column>

                <!-- 团队作业 -->
                <el-table-column
                v-if="this.homeworktype!=0"
                prop="groupname"
                width="120"
                label="团队名称">
                </el-table-column>
                <el-table-column
                v-if="this.homeworktype!=0"
                prop="id"
                label="团队id">
                </el-table-column>
                <el-table-column
                v-if="this.homeworktype!=0"
                prop="leader.stuname"
                label="组长">
                </el-table-column>


                <el-table-column
                prop="totalscore"
                label="总分"
                sortable="custom">
                </el-table-column>
                <el-table-column
                width="120"
                label="博客">
                <template slot-scope="scope">
                    <el-button @click="linkToBlog(scope.row.blog)" type="info"><a style="color:#ffffff;width:100%;height:100%" target="view_window" :href="scope.row.blog">查看博客</a></el-button>
                </template>
                </el-table-column>
                <el-table-column
                width="240">
                <template slot="header" slot-scope="scope">
                    <div class="header_search_input">
                        <el-input placeholder="输入关键字搜索"
                         v-model="search"
                         size="small"
                         class="input-with-select"
                         @keyup.enter.native="scoreSearch()">
                            <el-button slot="append" icon="el-icon-search"
                             @click="scoreSearch()"
                            @keyup.enter="scoreSearch()"></el-button>
                        </el-input>
                    </div>
                </template> -->


                <!-- 评分 -->
                <template slot-scope="scope">
                    <el-button type="primary" plain  @click="showpoint(scope.$index)">查看评分</el-button>
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
                <span v-if="inputdis">{{this.score}}</span>
                <span v-if="!inputdis">{{this.score1}}</span>
            </div>
        </div>
        <el-table
            :data="scoredetail"
            style="width: 100%">
            <el-table-column
            prop="point"
            label="评分点"
            width="100">
            </el-table-column>
            <el-table-column
            width="280"
            label="评分细则">
            <template slot-scope="scope">
                <div v-if="scorerule[0]!=undefined">{{scorerule[scope.$index].description}}</div>
            </template>
            </el-table-column>
            <el-table-column
            label="评分">
            <template slot-scope="scope">
                <el-input v-model="scope.row.score" 
                :disabled="inputdis"
                 @input="numberChange($event,scope.$index)"
                @change="numberChange($event,scope.$index)">
                </el-input>
                /&nbsp;&nbsp;{{scorerule[scope.$index].max}}
            </template>
            </el-table-column>
        </el-table>
        <div class="dia_button">
           <div  class="bonus">
               <div>加成</div>
               <el-input-number :disabled="inputdis" size="small" :precision="2" v-model="bonus" :max="1" :min="-1"></el-input-number>
               <div class="bonus_tips">tips:百分数</div>
            </div>
            <button v-if="this.role==2" @click="inputdis=false">更新</button>
            <button @click="dialogVisible=false" v-if="inputdis">确定</button>
            <button v-if="!inputdis" @click="update()">确认更新</button>
        </div>
        </el-dialog>
    </div>
</template>
<script>
import HomeworkVue from '../homework/Homework.vue';
export default {
    name:"scorecouple",
    data(){
        return{
            bonus:0,
            pages:{},
            currentpage:1,
            result:[],
            search: '',
            dialogVisible: false,
            homeworkid:0,
            homeworktype:0,
            homework:{},
            scorerule:[],
            index:0,
            scorerules:[],
            scoredetails: [],
            inputdis:true,
            order:"",
        }
    },
    methods:{
        gethomework(){
            this.$api.homework.getlist(this.homeworktype).then(response=>{
                console.log(response)
                let res=response.data;
                if(res!=undefined){
                    let homework=res.results.filter(item=>item.id==this.homeworkid)[0];
                    this.homework=JSON.parse(JSON.stringify(homework))
                    this.scorerule=JSON.parse(JSON.stringify(this.homework.scorerules))
                }
                else{
                    this.homework={};
                }
            })
        },
        getparam(){
            let param={
                "page":this.currentpage,
                "homework":this.homeworkid
            }
            if(this.order!=""){
                param.ordering=this.order
            }
            this.getlist(param)
        },
        getlist(param){
            this.$api.score.judgement(param).then(response=>{
                let res=response.data;
                this.pages={
                    "count": res.count
                }
                this.result=[]
                this.scoredetails=[]
                if(this.homeworktype==0){
                    res.results.forEach(item=>{
                        item.student={...item.student,"uid":item.id,"totalscore":item.totalscore,"bonus":item.scoredetail.bonus,"blog":item.blogurl}
                        this.result.push(item.student)
                        this.scoredetails.push(item.scoredetail)
                    })
                }
                else{
                    res.results.forEach(item=>{
                        item.group={...item.group,"uid":item.id,"totalscore":item.totalscore,"bonus":item.scoredetail.bonus,"blog":item.blogurl}
                        this.result.push(item.group)
                        this.scoredetails.push(item.scoredetail)
                    })
                }
            })
        },
        update(){
            let results=JSON.parse(JSON.stringify(this.scoredetail));
            let msg=this.result[this.index];
            let id=msg.uid
            console.log(msg)
            for(let item in results){
                results[item].score=parseInt(results[item].score)
            }
            let scoredetail={"scorepoints":results,"score":this.totalScore,"bonus":this.bonus}
            let result={"scoredetail":scoredetail}
            console.log(result)
            this.$api.score.update(id,result).then(response=>{
                let res=response.data
                this.result[this.index].totalscore=res.totalscore
                this.result[this.index].bonus=res.scoredetail.bonus
                this.scoredetails[this.index]=res.scoredetail.scorepoints
                this.dialogVisible=false
                this.open2("更新成功")
            }).catch(err=>{
                this.open4("只能更新自己评分的内容")
            })
        },
        linkToBlog(url){
            window.open(url);
        },
        //打开评分时显示
        showpoint(index){
            this.dialogVisible=true;
            this.index=index;
            this.inputdis=true
            this.bonus=this.result[this.index].bonus
        },
        handleCurrentChange(currentpage){
            this.currentpage=currentpage
            this.getparam();
        },
        getid(){
            this.homeworkid=this.$route.query.homeworkid;
            this.homeworktype=this.$route.query.homeworktype;
        },       
        numberChange(val, index) {
            let integer = /^(-|\+)?\d+$/;
            let max=this.scorerule[index].max
            if (integer.test(val)) {
                if(parseInt(val)>=max)
                this.scorerules[index].score=max
            }
        },
        scoreSearch(){
            let obj=
            {
                "search":this.search,
                "homework":this.homeworkid
            }
            this.getlist(obj);
        },
        //排序
        sortChange(column) {
            let name=column.prop
            if(name=="stuid"){
                name="student__stuid"
            }
            else if(name=="uid"){
                name="id"
            }
            else if(name=="id"){
                name="student"
            }
            if(column.order=="descending"){
                name=`-${name}`
                console.log(name)
            }
            if(column.order!=null){
                this.order=name
                let obj={
                    "ordering":name,
                    "page":this.currentpage,
                    "homework":this.homeworkid
                    }
                this.getlist(obj)
            }
            else if(column.order==null){
                this.getparam();
            }
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
    },
    computed:{
        totalScore:function(){
            let sum=0;
            let data=this.scoredetail;
            for(let item in data){
                if(data[item].score!=""&&data[item].score!="-"&&data[item].score!=undefined){
                    sum+=parseInt(data[item].score)
                }
                if(typeof(data[item].score==undefined)){
                    sum+=0;
                }
            }
            return sum;
        },
        score1:function(){
            let sum=0;
            let data=this.scoredetail;
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
        score:function(){
            if(this.result[0]!=undefined){
                return this.result[this.index].totalscore
            }else{
                return 0
            }
        },
        scoredetail:function(){
            if(this.scoredetails[0]!=undefined){
                return this.scoredetails[this.index].scorepoints
            }
        },
        role:function(){
            return this.$store.getters.role
        },
    },
    created(){
        this.getid()
        this.gethomework();
        this.getparam();
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
    background: #ffffff;
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
    width: 15%;
    height: 100%;
    background: #64B0FE;
    color: #ffffff;
    border: 0;
    margin: 20px 0;
    margin-left: 10px;
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
  width: 60%!important;
}
body > div.el-dialog__wrapper > div .el-input .el-input__inner{
    padding-left: 10px!important;
    padding-right: 0!important;
    text-align: left;
    width: 100%!important;
}
body > div.el-dialog__wrapper > div{
    width: 600px!important;
}
body > div.el-dialog__wrapper > div > div.el-dialog__header{
    padding-bottom: 0px!important;
    display: none!important;
}
#score_judge > div.score_box > div.el-table.el-table--fit.el-table--striped.el-table--border.el-table--enable-row-hover.el-table--enable-row-transition > div.el-table__body-wrapper.is-scrolling-none > table > tbody > tr> td> div > button.el-button.el-button--info{
    width: 90%!important;
    text-align: center!important;
    padding-left: 0!important;
    padding-right: 0!important;
    color: #ffffff!important;
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

body > div.el-dialog__wrapper > div > div.el-dialog__body > div.el-table.el-table--fit.el-table--enable-row-hover.el-table--enable-row-transition > div.el-table__body-wrapper.is-scrolling-none > table > tbody > tr.el-table__row{
    height: 30px!important;
}
body > div.el-dialog__wrapper > div > div.el-dialog__body > div.el-table.el-table--fit.el-table--enable-row-hover.el-table--enable-row-transition > div.el-table__body-wrapper.is-scrolling-none > table > tbody > tr> td{
    padding: 10px 0!important;
}
body > div.el-dialog__wrapper > div > div.el-dialog__body > div.el-table.el-table--fit.el-table--enable-row-hover.el-table--enable-row-transition > div.el-table__body-wrapper.is-scrolling-none > table > tbody > tr > td> div > div{
    width: 60%!important;
    margin-right: 4px;
}
</style>