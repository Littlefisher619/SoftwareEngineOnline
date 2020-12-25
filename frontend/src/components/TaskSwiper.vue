<template>
    <div id="task_swiper">
        <div class="homework_list">
            <swiper :options="swiperOption" ref="mySwiper" class="swiper">
                <swiper-slide v-for="(item,key) in result" :key="key" class="homework_list_swiper">
                    <div class="homework_swiper_title">{{item.title}}</div>
                    <div class="homework_swiper_detail">
                        <div class="homework_lable">作业详情:</div>
                        <div class="homework_url">
                            <a  target="_blank" v-bind:href="item.blogurl">作业链接</a>
                        </div>
                    </div>
                    <div class="homework_swiper_select">
                        <button class="homework_select_button" @click="select(item.id)">选择</button>
                    </div>
                </swiper-slide>
                <div class="swiper-button-prev" slot="button-prev" ref="prev" v-if="result.length>1"></div>
                <div class="swiper-button-next" slot="button-next" ref="next"  v-if="result.length>1"></div>
            </swiper>
        </div>
    </div>
</template>
<script>
export default {
    data(){
        return{
            swiperOption: {
                loop:false,
                effect : 'flip',
                autoplay: {
                delay: 3000000,
                stopOnLastSlide: false,
                centeredSlidesBounds: true,
                disableOnInteraction: false
                },
                // 设置点击箭头
                navigation: {
                    nextEl: ".swiper-button-next",
                    prevEl: ".swiper-button-prev",
                },
            }
        }
    },
    props:{
        result:[]
    },
    methods:{
        select(id){
            this.$emit('childFn',id)
        }
    },
    computed: {
        swiper() {
            return this.$refs.mySwiper.swiper;
        }
    },
    created(){
    }
}
</script>
<style scoped>
button{
    background: #159BD5;
    color: white;
    border: 0;
    width: 100px;
    height: 28px;
}
#task_swiper{
    height: 100%;
    width: 100%;
    padding-top: 4%;
    box-sizing: content-box;
}
.homework_list{
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
}
.swiper{
    height: 100%;
    width: 100%;
}
.homework_list_swiper{
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    padding-top: 8%;
    box-sizing: content-box;
}
.homework_list_swiper>div{
    width: 80%;
    height: auto;
}
.homework_swiper_title{
    width: 100%;
    font-weight: bold;
    font-size: 18px;
}
.homework_swiper_detail{
    width: 90%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 5%;
}
.homework_lable{
    font-size: 16px;
}
.homework_url>a{
    font-size: 16px;
    color: #159BD5;
}
.homework_select_button{
    margin-top: 10%;
}
/* 前进后退按钮 */
.swiper-button-prev{
    width: 12%;
    height: 6%;
    visibility: hidden;
    transition: all 1s linear;
    opacity: 0;
}
.swiper-button-next{
	width: 9%;
    height: 6%;
    visibility: hidden;
    transition: all 0.4s linear;
    opacity: 0;
}
.swiper-container:hover .swiper-button-next{
    visibility: visible;
    opacity: 1;
}
.swiper-container:hover .swiper-button-prev{
    visibility: visible;
    opacity: 1;
}
.swiper-button-disabled{
    opacity: 0.3!important;
}
.swiper-button-disabled{
    opacity: 0.3!important;
}
</style>