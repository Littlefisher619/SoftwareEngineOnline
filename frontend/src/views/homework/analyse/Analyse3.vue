<template>
    <div id="analyse">
        <div class="summary1" v-if="homeworktype!=0">
            <div class="analyse_head">
                <div class="analyse_stuname">
                    <div class="analyse_stuname_welcome">结对作业分析</div>
                    <div class="analyse_stuname_summary">Summary</div>
                </div>
                <!-- <div class="analyse_avater">
                    <el-avatar :size="40" src="https://empty" @error="errorHandler">
                    <img src="https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png"/>
                    </el-avatar>
                </div> -->
            </div>
            <div class="summary_content">
                <div class="summary_content_item score">
                    <div class="max_show">
                        <el-popover
                            placement="top-start"
                            width="100"
                            trigger="hover"
                            >
                            <div>
                                <div>
                                    最高分:{{this.content.max}}
                                </div>
                                <div>
                                    最低分:{{this.content.min}}
                                </div>
                                <div>
                                    平均分:{{this.content.avg}}
                                </div>
                            </div>
                            <el-button slot="reference">得分情况</el-button>
                        </el-popover>
                    </div>
                    <div id="score"></div>
                </div>
                <div class="summary_content_item ai">
                    <div id="aiauto"></div>
                </div>
                <div class="summary_content_item points">
                    <div id="points">
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
            homeworkid:3,
            content:"",
        }
    },
    created(){

    },
    props:{
        // homeworkid
    },
    mounted(){
        // this.getpoints();
        // this.getscore()
    },
    methods:{
        getpoints(arr){
            let xdata=new Array()
            let max=new Array()
            let min=new Array()
            let avg=new Array()
            for(let item in arr){
                xdata.push(arr[item].point)
                max.push(arr[item].max)
                min.push(arr[item].min)
                avg.push(arr[item].avg)
            }
            let ymin=this.getMaximin(min,"min")
            let myChart = this.$echarts.init(document.getElementById("points"));
            let option = {
                title: {
                    text: '评分点得分情况',
                    left: 'center'
                },
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b} : {c}'
                },
                legend: {
                    left: 'left',
                    data: ['最大值','平均值','最小值']
                },
                xAxis: {
                    type: 'category',
                    name: 'points',
                    splitLine: {show: false},
                    data: xdata,
                    axisLabel:{interval: 0}
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                yAxis: {
                    type: 'log',
                    name: 'score',
                    minorTick: {
                        show: true
                    },
                    // scale:true,
                    min:ymin,
                    minorSplitLine: {
                        show: true
                    }
                },
                series: [
                    {
                        name: '最小值',
                        type: 'line',
                        data: min,
                        // itemStyle : {  
                        //     normal : {  
                        //         lineStyle:{  
                        //             color:'#2196F3'  
                        //         }  
                        //     }  
                        // },
                    },
                    {
                        name: '平均值',
                        type: 'line',
                        data: avg,
                        // itemStyle : {  
                        //     normal : {  
                        //         lineStyle:{  
                        //             color:'#2775b6'  
                        //         }  
                        //     }  
                        // },
                    },
                    {
                        name: '最大值',
                        type: 'line',
                        data: max,
                        // itemStyle : {  
                        //     normal : {  
                        //         lineStyle:{  
                        //             color:'#93b5cf'  
                        //         }  
                        //     }  
                        // },
                    }
                ]
            };
            myChart.setOption(option);
        },
        getMaximin(arr,maximin) { 
            if(maximin=="max") { 
                return Math.max.apply(Math,arr); 
            }else if(maximin=="min") { 
                return Math.min.apply(Math, arr); 
            } 
        } ,
        getscore(totalscore){
            let xdata=new Array()
            let ydata=new Array()
            for(let i=1;i<totalscore.length;i++){
                xdata[i-1]=`${totalscore[i].from}~${totalscore[i].to}`
                ydata[i-1]=`${totalscore[i].count}`
            }
            let myChart = this.$echarts.init(document.getElementById("score"));
            // 绘制图表
            let option = {
                color: ['#3398DB'],
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                        type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                legend: { // 图例
                   data: [{name:'累计发现风险设备'},{name:'累计消除风险设备'}]
                 },
                title : {
                    text: "分数区间",//主标题
                    x:'10%',
                    y:'6%',
                    textAlign:'center',
                    textStyle: {
                        fontsize:14,
                        color:"black",
                        align: 'center',
                    },
                },
                xAxis: [
                    {
                        type: 'category',
                        data: xdata,
                        axisTick: {
                            alignWithLabel: true
                        }
                    }
                ],
                yAxis: [
                    {
                        type: 'value'
                    }
                ],
                series: [
                    {
                        name: '分数区间',
                        type: 'bar',
                        barWidth: '60%',
                        data:ydata,
                    }
                ]
            };

            myChart.setOption(option)

        },
        aiAuto(){
            let myChart = this.$echarts.init(document.getElementById("aiauto"));
            // 绘制图表
            let option = {
                title : {
                    text: "自动化实现",//主标题
                    x:'14%',
                    y:'6%',
                    textAlign:'center',
                    textStyle: {
                        fontsize:14,
                        color:"black",
                        align: 'center',
                    },
                },
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b}: {c} ({d}%)'
                },
                legend: {
                    orient: 'vertical',
                    left: '80%',
                    top:"14%",
                    data: ['较差', '较好', '没有', '完美', '一般']
                },
                series: [
                    {
                        name: '自动化程度',
                        type: 'pie',
                        radius: ['50%', '70%'],
                        avoidLabelOverlap: false,
                         itemStyle: {
                            normal: {
                                color:function(params){ 
                                    let colorList=['#3751FE', '#2196F3', '#2775b6','#93b5cf', '#baccd9','#f9f4dc','#fbda41','#867018','#806d9e','#a7535a','#f1939c']; 
                                    return colorList[params.dataIndex % colorList.length];
                                },
                            }
                        },
                        label: {
                            show: false,
                            position: 'center'
                        },
                        emphasis: {
                            label: {
                                show: true,
                                fontSize: '24',
                                fontWeight: 'bold'
                            }
                        },
                        labelLine: {
                            show: false
                        },
                        data: [
                            {value: 8, name: '较差'},
                            {value: 10, name: '较好'},
                            {value: 14, name: '没有'},
                            {value: 3, name: '完美'},
                            {value: 15, name: '一般'}
                        ]
                    }
                ]
            };
            myChart.setOption(option)
        },
        getdata(){
            this.$api.homework.static(this.homeworkid).then(response=>{
                let res=response.data;
                let totalscore=res.totalscore;
                let points=res.points;
                this.getpoints(points)
                this.getscore(totalscore.ranges)
                this.content={
                    "max":totalscore.max,
                    "min":totalscore.min,
                    "avg":totalscore.avg
                }
                this.aiAuto()
            })
        }
    },
    created(){
        this.getdata();
    }
}
</script>
<style scoped>
/* 结对作业 */
.summary1{
    width: 94vw;
    height: 86vh;
    /* margin-top: 0.5%; */
    position: relative;
    overflow-x: hidden;
    background: #EFF6FF;
    overflow-y: auto;
    scrollbar-width: none; /* firefox */
    -ms-overflow-style: none; /* IE 10+ */
    padding:2% 3%;
    border-radius: 20px;
}
.analyse_head{
    height: 10%;
    width: 100%;
    display: flex;
    align-items: flex-start;
    box-sizing: content-box;
    color: black;
}
.analyse_stuname{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    position: relative;
}
.analyse_stuname_welcome{
    font-weight: bold;
    font-size: 18px;
}
.analyse_stuname_summary{
    color: #AEB0B5;
    margin-top: 2px;
}
.analyse_avater{
    position: absolute;
    right: 8%;
}
.summary_content{
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    align-items: flex-start;
    height: 89%;
    margin-top: 1%;
}
.summary_content_item{
    border-radius: 10px;
    background: #ffffff;
}
.summary_content_item>div{
    width: 100%;
    height: 100%;
}
.score{
    width: 58%;
    height: 80%;
    margin-right: 2%;
    position: relative;
}
#score{
    pointer-events:all;
}
.max_show{
    position: absolute;
    right: 16%;
    top: 4%;
    width:20px!important;
    height:20px!important;
    text-align: right;
    z-index: 999;
    pointer-events:all;
}
.ai{
    width: 40%;
    height: 80%;
    /* margin-left: 2%; */
}
#aiauto{
    width: 100%;
    height: 90%;
}
.points{
    width: 100%;
    height: 100%;
    margin-top: 2%;
    padding-top: 2%;
}
#points{
    width: 96%;
    height: 96%;
}
</style>