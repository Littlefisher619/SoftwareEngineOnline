<template>
    <div id="score_summary">
        <div class="score_inner">
            <div id="scoreBar"></div>
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
        homeworkid:Number,
        totalscore:{
            type:Array
        }
    },
    methods:{
        drawLine(id,title,x=null,serie=null,) {
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
                yAxis: {},
                series: serie
            }
            myChart.setOption(option);
        },
        // getscore(){
        //     this.$api.homework.static(this.homeworkid).then(response=>{
        //         let totalscore=response.data.totalscore
        //         let points=response.data.points
        //         this.drawscore(totalscore.ranges)
        //     })
        // },
        drawscore(totalscore){
            let xdata=new Array()
            let ydata=new Array()
            if(totalscore[0]){

            }
            for(let i=1;i<totalscore.length;i++){
                xdata[i-1]=`${totalscore[i].from}~${totalscore[i].to}`
                ydata[i-1]=`${totalscore[i].count}`
            }
            let series={
                    name:"人数",
                    type:'bar',
                    data:ydata,
                    itemStyle: {
                        normal: {
                            color:function(params){ 
                                let colorList = ['#61a0a8', '#d48265', '#91c7ae','#749f83', '#ca8622','#f9f4dc','#fbda41','#867018','#806d9e','#a7535a','#f1939c']; 
                                return colorList[params.dataIndex % colorList.length];
                            }
                        }
                    }
            }
            let xAxis={
                data:xdata
            }
            console.log(xdata)
            console.log(ydata)
            this.drawLine("scoreBar","分数区间人数分布直方图",xAxis,series)
        },


    },
    computed:{
        ranges:function(){
            return this.totalscore
        }
    },
    mounted(){
        if(this.totalscore!=undefined){
            this.drawscore(this.totalscore)
        }
    },
    created(){
        // this.getscore()
    },
}
</script>
<style>
#score_summary{
    width: 100%;
    height: 100%;
}
.score_inner{
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}
#scoreBar{
    width: 80%;
    height: 84%;
}
.score_item{
    display: flex;
    flex-direction: column;
    justify-content: start;
    align-items: center;
}
</style>
<style>
#scoreBar > div:nth-child(1){
    width: 100%!important;
    height: 100%!important;
}
</style>