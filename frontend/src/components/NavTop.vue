<template>
    <div id="navTop">
        <div class="navTop_box">
            <div class="navTop_router">
                <span class="parent_route_name">{{this.$route.meta.parentName}}</span> /
                <span class="homework_name" v-if="this.homeworkname!=''">{{this.homeworkname}}&nbsp;/</span>
                <span class="route_name">{{this.$route.meta.name}}</span>
            </div>
            <div class="navTop_avater">
                <div class="user_name">
                    {{this.stuname}}
                </div>
                <div class="user_avater" @click="toSetting()">
                    <img :src="avater">
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    data(){
        return{
            avater:require("../assets/images/avater.jpg"),
        }
    },
    methods:{
        toSetting(){
            this.$router.push({
                path:'/setting'
            })
        },
    },
    computed: {
        stuname(){
            return this.$store.getters.stuname
        },
        homeworkname(){
            return this.$store.getters.homeworkName
        }
    },

}
</script>
<style scoped>
#navTop{
    position: relative;
    box-sizing: content-box;
    border: 1px solid #dddbdb;
    border-left: 0;
}
.navTop_box{
    width: 100%;
    padding-left: 4%;
    height: 100%;
    box-sizing: content-box;
    display: flex;
    align-items: center;
    justify-content: flex-start;
}
.navTop_avater{
    position: absolute;
    right: 4%;
    height: 100%;
    width: 20%;
    display: flex;
    align-items: center;
    justify-content: flex-end;
}
.parent_route_name{
    font-size: 12px;
    color: #8b8a8a;
}
.homework_name{
    font-size: 14px;
    margin-right: 4px;
}
.route_name{
    font-size: 13px;
    color: #697970;
    font-weight: 600;
}
.user_name{
    color: #697970;
    font-size: 16px;
}
.user_avater{
    width: 44px;
    height: 36px;
    border-radius: 50%;
    margin-left: 10px;
    transition: all .4s ease-in-out;
	-webkit-transition: all .4s ease-in-out;
	object-fit: cover;
    cursor: pointer;
}
.user_avater>img{
    width: 100%;
    height: 100%;
    border-radius: 50%;
}
.user_avater:hover{
    transform: rotate(360deg);
	-webkit-transform: rotate(360deg);
}
</style>