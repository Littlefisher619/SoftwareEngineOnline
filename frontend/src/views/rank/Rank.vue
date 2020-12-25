<template>
    <div id="rank">
        <div class="rank_box">
            <div class="rank_header_sails">
                <div class="left_icon">
                    <<< <<<
                </div>
                <div class="sails_entrance">
                    <span>千帆竞技图<span class="to_sails" @click="toSails()">（点击进入）</span></span>
                </div>
                <div class="right_icon">
                    >>> >>>
                </div>
            </div>
            <div class="rank_table">
                <el-table
                    :data="rank"
                    style="width: 100%">
                    <el-table-column
                    type="index"
                    width="120"
                    label="排名">
                    </el-table-column>
                    <el-table-column
                    prop="stuid"
                    label="学号">
                    </el-table-column>
                    <el-table-column
                    prop="stuname"
                    label="姓名">
                    </el-table-column>
                    <el-table-column
                    prop="totalscore"
                    label="总分（加权后）">
                    </el-table-column>
                    <el-table-column
                    label="查看详情">
                    <template slot-scope="scope">
                        <button class="rank_show_details" @click="showDia(scope.$index)">查看详情</button>
                    </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>
        <el-dialog
        :visible.sync="detailVisible"
        @open="open()"
        width="30%">
        <div id="detailLine"></div>
        </el-dialog>
    </div>
</template>
<script>
export default {
    data(){
        return{
            rank:[],
            scoreDetails:[],
            detailVisible:false,
            index:0,
        }
    },
    methods:{
        getrank(){
            this.$api.score.rank().then(response=>{
                this.rank=response.data
            })
        },
        showDia(index){
            console.log(index)
            this.index=index;
            this.detailVisible=true
        },
        showDetails(){
            let index=this.index
            this.detailVisible=true
            let scoreDetails=this.rank[index].scoredetail;
            let myChart = this.$echarts.init(document.getElementById("detailLine"));
            let sum=0;
            let xAxis=new Array();
            let yAxis=new Array();
            for(let item in scoreDetails){
                if(scoreDetails[item].score!=null){
                    let xname=`${scoreDetails[item].homework}`
                    xAxis.push(xname)
                    sum+=scoreDetails[item].score
                    yAxis.push(sum)
                }
            }
            let option={
                //标题
                title:{
                // text:'生鲜销量统计'
                },
                toolbox:{
                    show:true,
                    feature:{
                        saveAsImage:{
                            show:true
                        }
                    }
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross',
                        crossStyle: {
                            color: '#999'
                        }
                    },
                },
                legend:{
                    xAxis
                },
                //x轴
                xAxis:{
                    data:xAxis,
                    boundaryGap: false
                },
                //y轴没有显式设置，根据值自动生成y轴
                yAxis:{},
                //数据-data是最终要显示的数据
                series:[{
                    name:'前n次得分之和',
                    type:'line',
                    data:yAxis
                }]
            };
            myChart.setOption(option);
        },
        open() {
            this.$nextTick(() => {
                this.showDetails()
            })
        },
        toSails(){
            const { href } = this.$router.resolve({
                path: `/sails`,
            });
            window.open(href, "_blank");
        }
    },
    created(){
        this.getrank()
    }
}
</script>
<style scoped>
#rank{
    width: 100%;
    height: 98%;
    background: #ffffff;
    overflow-y: scroll;

}
.rank_box{
    width: 100%;
    height: 100%;
    padding-top: 2%;
    box-sizing: content-box;
    display: flex;
    flex-direction: column;
    align-items: center;
    background: #ffffff;
}
.rank_header_sails{
    width: 96%;
    height: 50px;
    padding: 10px 0;
    border-radius: 5px;
    border: 1.5px dashed #EBEBEB;
    background: linear-gradient(white,white) padding-box,
    repeating-linear-gradient(-45deg,#ccc 0, #ccc 0.4em,white 0,white 0.75em);
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: bold;
    font-size: 16px;
}
.to_sails{
    color: #108DE9;
    cursor: pointer;
}
.sails_entrance{
    margin-left:10px;
    margin-right:10px;
}
.rank_table{
    width: 92%;
}
.rank_show_details{
    width: 50%;
    height: 100%;
    border: 0;
    color: #ffffff;
    background: #108DE9;
    cursor: pointer;
}
#detailLine{
    width: 380px;
    height: 300px;
    display: flex;
    flex-direction: column;
    align-items: center;
}
</style>
<style>
#rank > div > div.rank_table > div > div.el-table__body-wrapper.is-scrolling-none > table > tbody > tr> td.el-table_1_column_5{
    padding-top: 8px!important;
    padding-bottom: 8px!important;
}
#rank > div > div.rank_table > div > div.el-table__body-wrapper.is-scrolling-none > table > tbody > tr > td.el-table_1_column_5 > div.cell{
    height: 30px!important;
}
#rank > div.el-dialog__wrapper > div > div.el-dialog__header > button > i{
    display: none;
}
#rank > div.el-dialog__wrapper > div{
    width: 450px!important;
    padding-left: 20px;
    padding-right: 20px;
}
</style>