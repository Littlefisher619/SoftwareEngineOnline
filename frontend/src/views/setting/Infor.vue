<template>
    <div id="setInfo">
        <button @click="me()">点我</button>
    </div>
</template>
<script>
export default {
    data(){
        return {

        }
    },
    methods:{
        me(){
            this.$api.user.information().then(response=>{
                console.log(response.data);
            }).catch(err=>{
                console.log(err.response)
            })
        }
    }
}
</script>
<style scoped>

</style>