<template>
    <div id="detail">
        <div class="detail_box">
            <div class="title_box">
                <div class="detail_header"><span>{{homework.title}}</span></div>
                <a class="title_link" target="view_window" :href="homework.blogurl">题目链接：{{homework.blogurl}}</a>
                <div class="detail_scorerules">
                     <div class="scorerules_content">
                         <el-table
                            :data="this.homework.scorerules"
                            stripe
                            style="width: 100%">
                            <el-table-column
                            prop="point"
                            label="评分点">
                            </el-table-column>
                            <el-table-column
                            prop="description"
                            label="描述">
                            </el-table-column>
                            <el-table-column
                            label="得分">
                            <template slot-scope="scope">
                                <span v-show="scope.row.score!=undefined" >{{scope.row.score}}</span>
                                <span v-show="scope.row.score===undefined" >-&nbsp;</span>
                                <span>/{{scope.row.max}}</span>
                            </template>
                            </el-table-column>
                         </el-table>
                         <div class="score_result">
                            <div class="bonus">
                                <div class="score_lable">附加分：</div>
                                <div class="score_scores">{{this.bonus}}(百分数)</div>
                            </div>
                            <div class="totalscore">
                                <div class="score_lable">总分：</div>
                                <div class="score_scores">{{this.totalscore}}(包含附加分)</div>
                            </div>
                         </div>
                     </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    data(){
        return{
            title:{},
            homework:{
                "scorerules": [
                    {
                        "point":"1.1",
                        "description":"第一个得分点",
                        "max":10,
                    },
                ]
            },
            result:[],
            homeworktype:0,
            homeworkid:1,
        }
    },
    methods:{
        getid(){
            this.homeworkid=this.$route.query.homeworkid;
            this.homeworktype=this.$route.query.homeworktype;    
        },
        getdetail(){
            let p1 = new Promise((resolve, reject) => {
                this.$api.user.myjudge().then(res=>{
                    resolve(res)
                }).catch(err=>{
                    reject(err)
                })
            });
            let p2 = new Promise((resolve, reject) => {
                this.$api.homework.getlist(this.homeworktype).then(res=>{
                    resolve(res)
                }).catch(err=>{
                    reject(err)
                })
            });
            Promise.all([p2,p1]).then(response=>{
                let res1=response[0].data;
                let result1=res1.results.filter(item=>item.id==this.homeworkid);
                console.log(result1)
                this.homework=result1[0];

                // 分数
                let res=response[1].data;
                if(this.homeworktype==0){
                    res=res.single;
                }
                else if(this.homeworktype==1){
                    res=res.double;
                }
                else if(this.homeworktype==2){
                    res=res.big;
                }
                console.log(res)
                let results=res.filter(item=>item.homework==this.homeworkid);
                console.log(results)
                if(results[0]!=undefined)
                {
                    let result=results[0]
                    let scoredetail=result.scoredetail
                    this.homework={...this.homework,"totalscore":result.totalscore,"bonus":scoredetail.bonus}
                    let len=scoredetail.scorepoints.length;
                    console.log(len)
                    let scorepoints=this.homework.scorerules;
                    for(let i=0;i<len;i++){
                        let obj=scorepoints[i]
                        scorepoints[i]={...obj,"score":scoredetail.scorepoints[i].score}
                    }
                    this.homework.scorerules=JSON.parse(JSON.stringify(scorepoints));
                    // this.$forceUpdate();
                }
            })
        },
    },
    computed:{
        scoredetail:function(){
            return JSON.parse(JSON.stringify(this.homework.scorerules))
        },
        bonus:function(){
            if(this.homework.bonus==0) {return "0%"}
            if(this.homework.bonus===undefined) {return "0%"}
            return this.homework.bonus.toFixed(2)*100+'%' 
        },
        totalscore:function(){
            if(this.homework.totalscore===undefined){return 0}
            else return this.homework.totalscore
        }
    },
    created() {
        this.getid();
        this.getdetail();
    },
}
</script>
<style scoped>
.detail_box{
    width: 100%;
    height: 100%;
    margin: auto;
    box-sizing: content-box;
    padding-top: 2%;
    background: #ffffff;
    box-sizing: content-box;
    padding-bottom: 100px;
}
.title_box{
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.detail_header{
    font-size: 21px;
    font-weight: 300;
    font-weight: bold;
}
.detail_content{
    font-size: 16px;
    word-break: break-word;
    text-align: left;
    text-indent: 2rem;
}
#iframeContain{
      width: 100%;
      height: 800px;
    }
a.title_link{
    color:#1491a8;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 20px;
    font-size: 16px;
    margin-bottom: 20px;
}
.detail_score{
    width: 80%;
    margin-top: 4%;
}
.detail_scorerules{
    width: 84%;
    display: flex;
    position: relative;
    flex-direction: column;
    box-sizing: content-box;
    justify-content: center;
    align-items: center;
}
.detail_scorerules_header{
    text-align: center;
    font-size: 18px;
    width: 100%;
}
.scorerules_content{
    width: 100%!important;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.score_result{
    width: 100%;
    height: 40px;
    display: flex;
    align-items: center;
    position: relative;
    font-size: 18px;
    margin-top: 10px;
}
.bonus{
    position: absolute;
    left: 13%;
    height: 100%;
    display: flex;
    align-items: center;

}
.totalscore{
    position: absolute;
    right: 10%;
    height: 100%;
    display: flex;
    align-items: center;
}
.score_lable{
    font-weight: bold;
    line-height: 40px;
}
.score_scores{
    line-height: 40px;
    margin-left: 10px;
}
</style>
<style>
#detail div.cell{
    text-align: center!important;
}

.el-table .warning-row {
    background: oldlace;
}

.el-table .success-row {
    background: #f0f9eb;
}
</style>