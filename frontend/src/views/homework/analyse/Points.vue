<template>
    <div id="points_line">
        <div class="points_inner">
            <div id="points"></div>
        </div>
    </div>
</template>
<script>
export default {
    data(){
        return{
        }
    },
    props:{
        homeworkid:Number
    },
    methods:{
        getscore(){
            this.$api.homework.static(this.homeworkid).then(response=>{
                let points=response.data.points
                this.drawpoints(points)
            })
        },
        drawpoints(arr){
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
            let myChart = this.$echarts.init(document.getElementById('points'));
            let option={
                tooltip : {
                    trigger : 'axis',
                    //指示器
                    axisPointer : {
                        type : 'line',
                        lineStyle : {
                            color:'#7171C6'
                        }
                    }
                },
                title: { 
                    text: "评分点得分率分布图",
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
                xAxis: [{
                    data:xdata
                }],
                yAxis: {},
                dataZoom: [{
                    type: 'inside'
                }],
                series: [
                    {
                        name: '最大值',
                        type: 'line',
                        itemStyle : {  
                            normal : {  
                                lineStyle:{  
                                    color:'#ed556a'  
                                }  
                            }  
                        },
                        data: max
                    },
                    {
                        name: '平均值',
                        type: 'line',
                        itemStyle : {  
                            normal : {  
                                lineStyle:{  
                                    color:'#45b787'  
                                }  
                            }  
                        },
                        data: avg
                    },
                    {
                        name: '最小值',
                        type: 'line',
                        data: min,
                        itemStyle : {  
                            normal : {  
                                lineStyle:{  
                                    color:'#eed045'  
                                }  
                            }  
                        },
                    },
                ]
            }
            myChart.setOption(option);
        }
    },
    created(){
        this.getscore()
    }
}
</script>
<style scoped>
#points_line{
    width: 100%;
    height: 100%;
}
.points_inner{
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}
#points{
    width: 80%;
    height: 84%;
}
</style>