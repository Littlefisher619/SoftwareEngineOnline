<template>
  <div id="sails">
    <div class="sails_inner">
      <div id="scoreSails"></div>
      <div class="data_filter"><el-checkbox v-model="isfilter"
      @change="fresh">只看前
        <el-input class="rank_filter"
        @input="rankChange($event)"
        @change="rankChange($event)"
          v-model="rank"></el-input>名
        </el-checkbox></div>
    </div>
  </div>
</template>
<script>
export default {
  data(){
    return{
      name:[],
      scoredetails:[],
      homework:[],
      rank:"",
      isfilter:false,
    }
  },
  methods:{
    fresh(){
      if(this.isfilter)
      {
        let rank=parseInt(this.rank);
        if(rank!=NaN&&rank<this.name.length+1){
          console.log(rank)
          let name=this.name.slice(0,`${rank}`);
          let homework=this.homework;
          let scoredetails=this.scoredetails.slice(0,`${rank}`);
          this.$echarts.init(document.getElementById('scoreSails')).dispose();
          this.drawSails(name,scoredetails,homework)
        }
      }
      else{
        this.drawSails(this.name,this.scoredetails,this.homework);
      }

    },
    getinfo(){
      this.$api.score.rank().then(response=>{
        let res=response.data
        let name=new Array();
        let scoredetails=new Array()
        let homework=new Array()
        for(let item in res[0].scoredetail){
          if(res[0].scoredetail[item].score!=null)
          {
            homework.push(res[0].scoredetail[item].homework)
          }
        }
        for(let i=0;i<res.length;i++){
          name.push(res[i].stuname);
          let arr=res[i].scoredetail
          scoredetails[i]=new Array()
          let score=0;
          for(let j=0;j<arr.length;j++){
            if(arr[j].score!=null){
              score+=arr[j].score;
              scoredetails[i][j]=score
            }
          }
        }
        this.name=name;
        this.scoredetails=scoredetails
        this.homework=homework
        this.drawSails(name,scoredetails,homework)
      })
    },
    rankChange(val){
      this.fresh();
    },
    drawSails(name,scoredetails,homework){
      let serie=new Array()
      for(let item=0;item<name.length;item++){
        let obj={
          name:name[item],
          type:"line",
          data:scoredetails[item]
        }
        serie.push(obj)
      }
      console.log(name)
      let myChart = this.$echarts.init(document.getElementById("scoreSails"));
      let option = {
            title: {
                text: '历次作业成绩曲线'
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
            legend: {
                data: []
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            dataZoom: [{
                type: 'inside',
                // startValue: FFTData[0][0],
            }, {
              start: 0,
                end: 100,
                handleSize: '100%',
                handleStyle: {
                    color: '#fff',
                    shadowBlur: 3,
                    shadowColor: 'rgba(0, 0, 0, 0.6)',
                    shadowOffsetX: 2,
                    shadowOffsetY: 2
                }
            }],
            toolbox: {
                feature: {
                    saveAsImage : {                         //保存为图片。
                        show: true,                         //是否显示该工具。
                        type:"png",                         //保存的图片格式。支持 'png' 和 'jpeg'。
                        name:"pic1",                        //保存的文件名称，默认使用 title.text 作为名称
                        backgroundColor:"#ffffff",        //保存的图片背景色，默认使用 backgroundColor，如果backgroundColor不存在的话会取白色
                        title:"保存为图片",
                        pixelRatio:1                       //保存图片的分辨率比例，默认跟容器相同大小，如果需要保存更高分辨率的，可以设置为大于 1 的值，例如 2
                    },
                    dataZoom: {
            　　　　　　yAxisIndex:"none"
            　　　　　},
                    mark : {                                 // '辅助线开关'
                        show: true
                    },
                    dataView : {show: true, title: '数据视图',readOnly: false,optionToContent:function(opt){
                      var axisData = opt.xAxis[0].data;
                      var series = opt.series;
                      var table = '<table style="width:100%;text-align:center"><tbody><tr>'
                                  + '<td>姓名</td>'
                      for(let i=0;i<homework.length;i++){
                          table+='<td>' + `第${homework[i]}次作业` + '</td>'
                      }
                          table+='</tr>';
                      for (var i = 0, l = series.length; i < l; i++) {
                          table += '<tr>'
                                   +'<td>' + series[i].name + '</td>'
                          for(let j=0;j<axisData.length;j++){
                            table+='<td>' + series[i].data[j] + '</td>'
                          }
                                  // + '<td>' + axisData[i] + '</td>'
                          table+='</tr>';
                      }
                      table += '</tbody></table>';
                      return table;
                    }},   
                },
                orient:"vertical",                        //工具栏 icon 的布局朝向'horizontal' 'vertical'
                itemSize:15,                                 //工具栏 icon 的大小
                itemGap:10,  
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: homework
            },
            yAxis: {
                type: 'value'
            },
            series: serie
        };

        myChart.setOption(option)

    }
  },
  created(){
    this.getinfo()
  }
}
</script>
<style scoped>
#sails{
  width: 100vw;
  height: 100vh;
}
.sails_inner{
  width: 100%;
  height: 100%;
  position: relative;
}
#scoreSails{
  width: 100%;
  height: 100%;
  position: absolute;
}
.data_filter{
  position: absolute;
  top: 2%;
  right: 4%;
  width: 15%;
  height: 6%;
  text-align: left;
}
.rank_filter{
  width: 30%;
  height: 100%;
  margin: 0 4px;
}
</style>
<style>
#sails > div > div.data_filter > label,
#sails > div > div.data_filter > label > span.el-checkbox__label{
  height: 100%!important;
}
#sails > div > div.data_filter > label > span.el-checkbox__label > div,
#sails > div > div.data_filter > label > span.el-checkbox__label > div > input{
  height: 90%!important;
}
</style>