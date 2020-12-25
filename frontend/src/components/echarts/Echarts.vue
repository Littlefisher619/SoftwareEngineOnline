<template>
    <div class="echarts">
        <div style="width:400px;height:400px;" :id="id" class="echarts">
    </div>
</template>
<script>
export default {
    data(){
        return{
            chartData: {
                type: Array,
                default: () => []
            }
        }
    },
    props:{
        id:{
            type:String,
            default: () => "echarts"
        },
        title:Promise,
    },
    methods:{
        draw(id,title,){

        }
    }
}
</script>
<style scoped>

</style>