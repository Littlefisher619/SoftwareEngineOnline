<template>
    <div id="summary">
        <div class="summary" v-if="homeworktype==0">
            <div class="summary_head">
                <div class="head_left_dec">
                    <div v-for="(item,key) in 6" :key="key" class="parallelogram">
                    </div>
                </div>
                <div class="summary_title">软工评测总结</div>
                <div class="head_right_dec">
                    <div v-for="(item,key) in 6" :key="key" class="parallelogram">
                    </div>
                </div>
            </div>
            <div class="summary_body">
                <component :is='componentName'></component>
            </div>
        </div>
        <div class="summary_analyse" v-if="homeworktype!=0">
            <component :is='componentName'></component>
        </div>
    </div>
</template>
<script>
import Analyse2 from './analyse/Analyse2'
import Analyse3 from './analyse/Analyse3.vue'
export default {
    components:{
        Analyse2,
        Analyse3,
    },
    data(){
        return{
            componentName:"Analyse2",
            homeworkid:0,
            homeworktype:1,
            avater:require("../../assets/images/avater2.jpg")
        }
    },
    methods:{
        getid(){
            this.homeworkid=this.$route.query.homeworkid;
            this.homeworktype=this.$route.query.homeworktype; 
            this.componentName=`Analyse${this.homeworkid}`
        }
    },
    computed:{
        stuname(){
            return this.$store.getters.stuname
        }
    },
    created(){
        this.getid();
    }
}
</script>
<style scoped>
#summary,
.summary{
    width: 100vw;
    height: 100vh;
    position: relative;
    overflow-x: hidden;
    overflow-y: auto;
    scrollbar-width: none; /* firefox */
    -ms-overflow-style: none; /* IE 10+ */
}
#summary{
    background: #ffffff;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.summary{
    background: url('http://www.kyube.top/images/cover/2.jpg');
    background-size: cover;
}
#summary::-webkit-scrollbar,
.summary::-webkit-scrollbar{
    display: none; /* Chrome Safari */
}
.summary_head{
    height: 8%;
    border-bottom: 1px solid #427a99;
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 999;
}
.summary_title{
    transform: skewX(-25deg);
    width: auto;
    height: 26px;
    border: 1px solid#5d7394;
    padding: 0 20px;
    color: #ffffff;
    font-size: 16px;
}
.head_left_dec,
.head_right_dec{
    transform: skewX(-25deg);
    display: flex;
    justify-content: center;
    align-items: center;
    margin-left: 10px;
}
.parallelogram{
    width: 10px;
    height: 20px;
    background: #5d7394;
    margin-right: 10px;
}
.summary_body{
    width: 100%;
    height: auto;
    position: absolute;
    top: 8%;
    bottom: 0;
    overflow-y: scroll;
}
.summary_body::-webkit-scrollbar{
    display: none; /* Chrome Safari */
}

.summary_analyse{
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: center;
}

</style>