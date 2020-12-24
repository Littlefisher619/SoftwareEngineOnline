<template>
    <div id="analyse">
        <div class="analyse_box">
            <div class="analyse_header">
                {{this.homeworkname}}数据分析
            </div>
            <div class="analyse_content">
                <div class="analyse_table">
                    <el-table
                        :data="points"
                        border
                        stripe
                        style="width: 100%">
                        <el-table-column
                        prop="point"
                        label="评分点"
                        width="180">
                        </el-table-column>
                        <el-table-column
                        prop="max"
                        label="最高分"
                        width="180">
                        </el-table-column>
                        <el-table-column
                        prop="min"
                        label="最低分">
                        </el-table-column>
                        <el-table-column
                        prop="avg"
                        label="平均分">
                        </el-table-column>
                    </el-table>
                </div>
                <div class="analyse_item">
                    <div id="score"></div>
                </div>
                <div class="analyse_item">
                    <div id="future"></div>
                </div>
                <div class="analyse_item">
                    <div id="myChart"></div>
                </div>
                <div class="analyse_item">
                    <div id="word"></div>
                </div>
                <div class="analyse_item">
                    <div id="time"></div>
                </div>
                <div class="analyse_item">
                    <div id="restaurant"></div>
                </div>
                <div class="analyse_item cloud">
                    <wordcloud
                    :data="hotword"
                    nameKey="name"
                    valueKey="value"
                    :color="myColors"
                    :showTooltip="true"
                    :wordClick="wordClickHandler">
                    </wordcloud>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import words from '../../assets/json/words.js'
import hot from '../../assets/json/hot_words.js'
import wordcloud from 'vue-wordcloud'
import totalscore from '../../assets/json/totalscore_and_points.js'
export default {
    data(){
        return{
            homeworkname:"个人编程作业",
            homeworkid:1,
            totalscore:[],
            year: "2018-10-20",
            time: "10:05:03",
            hotword:[],
            myColors: ['#1f77b4', '#629fc9', '#94bedb', '#c9e0ef'],
            points:[],
        }
    },
    mounted(){
        this.getwords();
        this.restr()
        this.gethot()
        this.getscoret()
    },
    components:{
        wordcloud
    },
    methods:{
        wordClickHandler(name, value, vm) {
            console.log('wordClickHandler', name, value, vm);
        },
        //绘制图的方法
        drawLine(id,title,x=null,serie=null,) {
            let myChart = this.$echarts.init(document.getElementById(`${id}`));
            let option={
                title: { 
                    text: title,
                    x:'50%',
                    y:'top',
                    textAlign:'center'
                },
                tooltip: {},
                xAxis: x,
                yAxis: {},
                series: serie
            }
            myChart.setOption(option);
        },
        bingtu(xname=null,xdata=null,id) {
            // 基于准备好的dom，初始化echarts实例
           let myChart = this.$echarts.init(document.getElementById(id));
            // 绘制图表
            let option={
                title : {
                    text: '未来的道路选择',//主标题
                    x:'center',
                    y:'10%',
                    textAlign:'center'
                },
                tooltip : {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                legend: {
                    orient: 'horizontal', // 布局方式，默认为水平布局，可选为：'horizontal' ¦ 'vertical'
                    // 水平安放位置，默认为左侧，可选为：'center' | 'left' | 'right' | {number}（x坐标，单位px）
                    x: 'center',
                    // 垂直安放位置，默认为全图顶端，可选为：'top' | 'bottom' | 'center' | {number}（y坐标，单位px）
                    y: '20%',
                    data: xname
                },
                series : [
                    {
                        name: '未来方向',
                        type: 'pie',
                        radius : '55%',
                        center: ['50%', '60%'],
                        data:xdata,
                        itemStyle: {
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }
                ]
            };
            myChart.setOption(option)
        },
        //绘制图的方法
        getwords() {
            let word=words.score.word.ranges
            let time=words.score.time.ranges
            let start=new Array()
            let count=new Array()
            let tstart=new Array()
            let tcount=new Array()
            for(let i=0;i<word.length;i++){
                if(word[i].to==null){
                    start[i]=start[i-1]+500
                }
                else{
                    start[i]=word[i].to
                }
                count[i] =word[i].count
            }
            for(let i=0;i<time.length;i++){
                if(word[i].to==null){
                    tstart[i]=tstart[i-1]+5
                }
                else{
                    tstart[i]=time[i].to
                }
                tcount[i] =time[i].count
            }
            let sseries={
                    name:"字数",
                    type:'line',
                    data:count
            }
            let sxAxis={
                data:start
            }
            this.drawLine("word","人数与博客字数区间折线图",sxAxis,sseries)
            let tseries={
                    name:"时间",
                    type:'line',
                    data:tcount
            }
            let txAxis={
                data:tstart
            }
            this.drawLine("time","人数与预估学习时间统计图",txAxis,tseries)
        },
        //餐厅双层饼图
        restr(){
            let myecharts =this.$echarts.init(document.getElementById('restaurant'));
            let option = {
                title : {
                    text: '最喜爱的餐厅排行',//主标题
                    x:'center',
                    y:'top',
                    textAlign:'center'
                },
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b}: {c} ({d}%)'
                },
                legend: {
                    orient: 'vertical',
                    left: 10,
                    top:'15%',
                    data: ['一楼', '二楼', '玫瑰', '丁香', '紫荆', '朝阳', '京元', '玫瑰', '丁香', '紫荆', '朝阳', '京元']
                },
                series: [
                    {
                        name: '楼层',
                        type: 'pie',
                        selectedMode: 'single',
                        radius: [0, '30%'],

                        label: {
                            position: 'inner'
                        },
                        labelLine: {
                            show: false
                        },
                        data: [
                            {value: 49, name: '一楼'},
                            {value: 57, name: '二楼'},
                        ]
                    },
                    {
                        name: '餐厅选择',
                        type: 'pie',
                        radius: ['40%', '55%'],
                        label: {
                            formatter: '{a|{a}}{abg|}\n{hr|}\n  {b|{b}：}{c}  {per|{d}%}  ',
                            backgroundColor: '#eee',
                            borderColor: '#aaa',
                            borderWidth: 1,
                            borderRadius: 4,
                            rich: {
                                a: {
                                    color: '#999',
                                    lineHeight: 22,
                                    align: 'center'
                                },
                                hr: {
                                    borderColor: '#aaa',
                                    width: '100%',
                                    borderWidth: 0.5,
                                    height: 0
                                },
                                b: {
                                    fontSize: 16,
                                    lineHeight: 33
                                },
                                per: {
                                    color: '#eee',
                                    backgroundColor: '#334455',
                                    padding: [2, 4],
                                    borderRadius: 2
                                }
                            }
                        },
                        data: [
                            {value: 41, name: '玫瑰'},
                            {value: 1, name: '紫荆'},
                            {value: 3, name: '丁香'},
                            {value: 3, name: '京元'},
                            {value: 1, name: '朝阳'},
                            {value: 27, name: '玫瑰'},
                            {value: 22, name: '紫荆'},
                            {value: 2, name: '丁香'},
                            {value: 4, name: '京元'},
                            {value: 2, name: '朝阳'},
                        ]
                    }
                ]
            };
            myecharts.setOption(option);
        },
        getscore(){
            this.$api.homework.static(this.homeworkid).then(response=>{
                //分数统计
                let score=response.data.totalscore
                this.totalscore=[score.max,score.min,score.avg]
                let xAxis={
                    data: ["最高分","最低分","平均分"]
                }
                let series=[{
                    name: '分数',
                    type: 'bar',
                    data:this.totalscore
                }]
                this.drawLine("myChart","成绩柱状图",xAxis,series);


                //未来意向
                let xname=["考研","考公","出国","工作","没有明确的意向"]
                let xdata=[
                    {value:81,name:"考研"},
                    {value:3,name:"考公"},
                    {value:5,name:"出国"},
                    {value:36,name:"工作"},
                    {value:7,name:"没有明确的意向"},
                ]
                this.bingtu(xname,xdata,"future")
            })
        },

        gethot(){
            let hotword=new Array();
            let hots=hot.hot
            for(let item in hots){
                let obj={"name":item,"value":hots[item]}
                hotword.push(obj)
            }
            this.hotword=hotword
        },

        // 总分的区间
        getscoret(){
            let score=totalscore.totalscore.ranges
            console.log(score)
            let start=new Array()
            let count=new Array()
            for(let i=0;i<score.length-1;i++){
                if(score[i+1].to==null){
                    start[i]=start[i+1]+500
                }
                else{
                    start[i]=score[i+1].to
                }
                count[i] =score[i+1].count
            }
            let sseries={
                    name:"字数",
                    type:'bar',
                    data:count
            }
            let sxAxis={
                data:start
            }
            this.drawLine("score","分数区间人数分布直方图",sxAxis,sseries)
        },
        getpoint(){
            let score=totalscore.totalscore
            let obj={"point":"总分",
            "max": score.max,
            "min": score.min,
            "avg": score.avg}
            let points=totalscore.points
            points.unshift(obj)
            this.points=points
            console.log(points)
        }
    },
    created(){
        this.getscore();
        this.getpoint()
    },
    computed:{
    }

}
</script>
<style scoped>
#analyse{
    width: 100%;
    background: #ffffff!important;
}
.analyse_box{
    width: 100%;
    height: auto;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 2%;
    box-sizing: content-box;
}
.analyse_header{
    width: 100%;
    height: 30px;
    font-size: 22px;
    font-weight: bold;
}
.analyse_content{
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.analyse_item{
    width: 80%;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.analyse_item>div{
    width: 80%;
    height: 80vh;
    display: flex;
    justify-content: center;
}
#myChart{
    width: 70%;
}
.analyse_item>div> div:nth-child(1){
    width: 100%;
    height: 100%;
}
.cloud{
    width:80%;
    height: 80vh;
}
.analyse_table{
    width: 80%;
    margin-top: 3%;
    margin-bottom: 3%;
}
</style>
<style>
body > div.tooltip{
    display: none;
}
#analyse > div > div.analyse_content > div.analyse_item.cloud > div > svg{
    transform: translate(0,-15%);
}
</style>