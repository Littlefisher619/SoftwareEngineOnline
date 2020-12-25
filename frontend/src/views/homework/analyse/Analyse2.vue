<template>
    <div id="Analyse2">
        <div class="Analyse2">
            <div class="content_left">
                <div class="content_left_inner">
                    <div class="program_language">
                        <div id="languageChoice"></div>
                        <div id="algorithmChoice"></div>
                    </div>
                    <div class="algorithm">
                        <div id="syntheticAlgorithm"></div>
                        <div class="syntheticAlgorithm">
                            <div class="syntheticAlgorithm_item">
                                <div class="led_lable">采用</div>
                                <div class="lednum">{{this.use}}</div>
                            </div>
                            <div class="syntheticAlgorithm_item">
                                <div class="led_lable">不采用</div>
                                <div class="lednum">{{this.notuse}}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="content_right">
                <div class="content_right_inner">
                    <swiper :options="swiperOption" ref="mySwiper" >
                    <swiper-slide v-if="totalscore.ranges"><score :homeworkid="homeworkid" :totalscore="totalscore.ranges"></score></swiper-slide>
                    <swiper-slide><points :homeworkid="homeworkid"></points></swiper-slide>
                    <swiper-slide><div id="homeworkTime" class="switem"></div></swiper-slide>
                    <swiper-slide><div id="timeConsum" class="switem"></div></swiper-slide>
                    <swiper-slide><div id="timeRatio" class="switem"></div></swiper-slide>
                    <swiper-slide>
                        <div>
                            <el-table
                                :data="tabledata"
                                border
                                style="width: 100%">
                                <el-table-column
                                prop="name"
                                label="类型">
                                </el-table-column>
                                <el-table-column
                                prop="max"
                                label="最大值">
                                </el-table-column>
                                <el-table-column
                                prop="min"
                                label="最小值">
                                </el-table-column>
                                <el-table-column
                                prop="avg"
                                label="平均值">
                                </el-table-column>
                            </el-table>
                        </div>

                    </swiper-slide>
                    <div class="swiper-pagination" slot="pagination"></div>
                    <div class="swiper-button-prev swiper-button-white" slot="button-prev"></div>
                    <div class="swiper-button-next swiper-button-white" slot="button-next"></div>
                    </swiper>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import score from './Score.vue'
import points from './Points.vue'
import all from '../../../assets/json/statistics.js'
import '../../../assets/font/font.css'
import { totalscore } from '../../../assets/json/totalscore_and_points'
export default {
    components:{
        score,
        points,
    },
    data(){
        return{
            homeworkid:2,
            use:"",
            notuse:"",
            totalscore:{},
            points:{},
            table:[],
            swiperOption: {
                loop: false,
                effect : 'flip',
                autoplay: {
                delay: 300000,
                stopOnLastSlide: false,
                disableOnInteraction: false
                },
                // 显示分页
                pagination: {
                el: ".swiper-pagination",
                clickable: true //允许分页点击跳转
                },
                // 设置点击箭头
                navigation: {
                    nextEl: ".swiper-button-next",
                    prevEl: ".swiper-button-prev",
                },
            }
        }
    },
    computed: {
        swiper() {
            return this.$refs.mySwiper.swiper;
        }
    },
    methods:{
        drawLine(id,title,x=null,serie=null,yname="") {
            let myChart = this.$echarts.init(document.getElementById(`${id}`));
            let option={
                title: { 
                    text: title,
                    x:'50%',
                    y:'top',
                    textAlign:'center',
                    textStyle: {
                        fontsize:14,
                        color:"#ffffff",
                        align: 'center',
                    },
                },
                tooltip: {},
                xAxis: x,
                yAxis: {
                    name:yname
                },
                series: serie
            }
            myChart.setOption(option);
        },
        pie(id,title,xname,name,data,show=true) {
            // 基于准备好的dom，初始化echarts实例
           let myChart = this.$echarts.init(document.getElementById(`${id}`));
            // 绘制图表
            let option={
                title : {
                    text: title,//主标题
                    x:'54%',
                    y:'6%',
                    textAlign:'center',
                    textStyle: {
                        fontsize:14,
                        color:"#98d1e7",
                        align: 'center',
                    },
                },
                tooltip : {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                legend: {
                    orient: 'vertical', // 布局方式，默认为水平布局，可选为：'horizontal' ¦ 'vertical'
                    // 水平安放位置，默认为左侧，可选为：'center' | 'left' | 'right' | {number}（x坐标，单位px）
                    x: 'left',
                    // 垂直安放位置，默认为全图顶端，可选为：'top' | 'bottom' | 'center' | {number}（y坐标，单位px）
                    y: 'top',
                    data: xname,
                    textStyle: {
                        color: '#fffff',
                    },
                },
                series :[
                    {
                        name: name,
                        type: 'pie',
                        radius : '55%',
                        center: ['55%', '60%'],
                        data:data,
                        itemStyle: {
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            },
                            normal: {
                                color:function(params){ 
                                    let colorList=['#61a0a8', '#d48265', '#91c7ae','#749f83', '#ca8622','#f9f4dc','#fbda41','#867018','#806d9e','#a7535a','#f1939c']; 
                                    return colorList[params.dataIndex % colorList.length];
                                },
                                label : {
                                    show : show   //隐藏标示文字
                                },
                                labelLine : {
                                    show :show   //隐藏标示线
                                }
                            }
                        },
                    },
                ]
            };
            myChart.setOption(option)
        },
        drawpie(id,arr,title="",xname="",show=true){
            let name=new Array()
            let data=new Array()
            for(let item in arr){
                name.push(item)
                let obj={"value":arr[item],"name":item}
                data.push(obj)
            }
            this.pie(id,title,name,xname,data,show)
        },
        drawbar(id,title,name,arr,yname=""){
            console.log(title)
            let xdata=new Array()
            let ydata=new Array()
            for(let i=0;i<arr.length;i++){
                if(arr[i].to==null){
                    xdata[i]=`>${arr[i].from}`
                }
                else{
                    xdata[i]=`${arr[i].from}~${arr[i].to}`
                }
                ydata[i]=`${arr[i].count}`
            }
            let series={
                    name:name,
                    type:'bar',
                    data:ydata,
                    itemStyle: {
                        normal: {
                            color:function(params){ 
                                let colorList = ['#c23531','#2f4554', '#61a0a8', '#d48265', '#91c7ae','#749f83', '#ca8622']; 
                                return colorList[params.dataIndex % colorList.length];
                            }
                        }
                    }
            }
            let xAxis={
                data:xdata
            }
            console.log("yes")
            this.drawLine(id,title,xAxis,series,yname)
        },
        getnum(){
            let arr=all.syntheticAlgorithm
            let data=new Array()
            for(let item in arr){
                let obj={"value":arr[item]}
                data.push(obj)
            }
            this.use=data[0].value
            this.notuse=data[1].value
        },
        getscore(){
            this.$api.homework.static(this.homeworkid).then(response=>{
                this.totalscore=response.data.totalscore
                let obj={"name":"总得分","max":totalscore.max,"min":totalscore.min,"avg":totalscore.avg}
                this.table.push(obj)
                this.points=response.data.points
            })
        },
        getdata(name,pro){
            let obj={"name":name,"max":pro.max,"min":pro.min,"avg":pro.avg}
            this.table.push(obj)
        }
    },
    created(){
        this.getscore()
        this.getdata("开发耗时",all.timeConsum)
        this.getdata("作业耗时",all.homeworkTime)
        this.getdata("开发耗时占比",all.timeRatio)
        console.log(this.table)
    },
    computed:{
        tabledata(){
            return this.table
        }
    },
    updated(){
        this.drawpie("languageChoice",all.language,"","编程语言")
        this.drawpie("algorithmChoice",all.algorithm,"","算法",false)
        this.drawpie("syntheticAlgorithm",all.syntheticAlgorithm,"综合算法","综合算法")
        this.drawbar("timeConsum","开发耗时分布","开发耗时",all.timeConsum.ranges,"单位：人")
        this.drawbar("homeworkTime","作业耗时分布","作业耗时",all.homeworkTime.ranges,"单位：人")
        this.drawbar("timeRatio","开发耗时与作业总耗时比值分布","开发耗时占比",all.timeRatio.ranges,"单位：人")
        this.getnum()
        // this.swiper.slideTo(1, 100000, false);
    }
}
</script>
<style scoped>
#Analyse2{
    width: 100%;
    height: 100%;
}
.Analyse2{
    width: 100%;
    height: 100%;
}
.content_left{
    width: 60%;
    height: 100%;
    position: absolute;
    left: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.content_right{
    width: 40%;
    height: 100%;
    position: relative;
    margin-left: 60%;
    box-sizing: content-box;
}
.content_right_inner{
    width: 94%;
    height: 94%;
    border: 1.5px solid #4087f1;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%,-50%);
    border-radius: 4px;
    /* background-color: rgba(59, 128, 207, 0.2); */
     background-image: linear-gradient(rgba(59, 128, 207, 0.8),rgba(255,255,255,0.5));
    /* background-color: rgba(255,255,255,0.2); */
}
.content_left_inner{
    width: 96%;
    height: 96%;
    position: relative;
}
.program_language{
    height: 46%;
    width: 100%;
    position: absolute;
    top: 0;
    display: flex;
    align-items: flex-start;
    justify-content: flex-start;
}
#languageChoice{
    width: 50%;
    height: 100%;
}
#algorithmChoice{
    width: 50%;
    height: 100%;
}
.algorithm{
    height: 54%;
    width: 100%;
    border: 1.5px solid #4087f1;
    position: absolute;
    top: 46%;
    margin-bottom: 0;
    border-radius: 6px;
    box-sizing: border-box;
    display: flex;
}
#syntheticAlgorithm{
    width:50%;
    height: 100%;
}
.syntheticAlgorithm{
    width: 50%;
    height: 100%;
    display: flex;
    align-items: center;
}
.syntheticAlgorithm_item{
    width: 50%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items:flex-start;
    padding-top: 8%;
}
.switem{
    width: 84%;
    height: 84%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.led_lable{
    font-size: 20px;
    color: #98d1e7;
    width: 100%;
    text-align: center;
}
.lednum{
    font-size: 100px;
    font-family: "DSDIGT";
    color: #ffffff;
    width: 100%;
    text-align: center;
}
</style>
<style>
#Analyse2 > div > div.content_right > div > div{
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding-left: 1%;
}
.swiper-slide{
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.swiper-button-white{
    opacity: 0;
    transition: all 0.6s ease-in-out;
}
.swiper-container:hover .swiper-button-white{
    opacity: 1;
}
</style>