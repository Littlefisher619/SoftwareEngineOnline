<template>
    <div id="score">
        <div v-show="roles!=2" class="err_tips" key="1">此页面测试组专用</div>
        <div v-show="roles==2" key="2" class="normal">
        <router-view name="scoresingle" :single="single"></router-view>
        <router-view name="scorecouple" :couple="couple"></router-view>
        <router-view :group="group"></router-view>
        </div>
    </div>
</template>
<script>
export default {
    data(){
        return{
            single:1,
            couple:1,
            role:0,
            group:[{
                "stuid":"031802143"
            }],
        }
    },
    methods:{
        getlist(){
            this.$api.homework.getlist().then(response=>{
                let res=response.data;
                if(res.results[0]){
                    let results=res;
                    for(let item in results){
                        if(results[item].homeworktype==0){
                            this.single.push(results[item])
                        }
                        if(results[item].homeworktype==1){
                            this.couple.push(results[item])
                        }
                        else{
                            this.group.push(results[item]);
                        }
                    }
                }
            })
        }
    },
    computed: {
        roles(){
            return this.$store.getters.role
        }
    },
}
</script>
<style scoped>
.err_tips{
    margin-top: 100px;
    font-size: 24px;
}
.normal{
    width: 100%;
    height: 100%;
}
</style>