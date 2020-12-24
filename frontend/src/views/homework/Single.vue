<template>
    <div id="single">
        <div class="single_box">
            <c-head></c-head>
            <div class="single_homework_list">
                <div class="single_homework_item" v-for="(item,i) in result" :key="i">
                    <div class="single_item_header">
                        {{item.title}}
                    </div>
                    <div class="single_item_conent">
                        <a target="view_window" :href="item.blogurl" class="single_item_more">{{item.blogurl}}</a>
                        <!-- <span class="single_item_more" @click="getdetail(item.id)">查看更多</span> -->
                        <div class="homework_button_list">
                            <div @click="getdetail(item.id)" class="homework_type">查看更多>>></div>
                            <div @click="analyse()" class="homework_type analyse" v-if="item.id==1">作业分析>>></div>
                            <div @click="summary()" class="homework_type analyse" v-if="item.id!=1">作业分析>>></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    data(){
        return{
            result:[]
        }
    },
    methods:{
        getlist(){
            this.$api.homework.getlist().then(response=>{
                let res=response.data;
                console.log(res);
                if(res!=undefined){
                    this.result=res.results.filter(item=>item.homeworktype==0);
                }
                else{
                    this.result=[];
                }
            })
        },
        getdetail(id){
            this.$router.push({
                path:'/homework/detail',
                query:{
                    "homeworkid":id,
                    "homeworktype":0,
                }
            }
            )
        },
        analyse(){
            this.$router.push(
                {
                    path:'/homework/analyse',
                    query:{
                        "homeworkid":1,
                        "homeworktype":0,
                    }
                }
            )
        },
        summary(){
            const { href } = this.$router.resolve({
                path: `/homework/summary`,
                query:{
                    "homeworkid":2,
                    "homeworktype":0,
                }
            });
            window.open(href, "_blank");
        }
    },
    created(){
        this.getlist();
    }
}
</script>
<style scoped>
#single{
    height: 100%;
    width: 100%;
}
.single_box{
    width: 100%;
    height: 100%;
    box-sizing: content-box;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.single_homework_list{
    position: relative;
    margin-top: 10px;
    width: 92%;
}
.single_homework_item{
    max-height: 200px;
    width: 100%;
    margin-top: 20px;
    border-bottom: 1px dashed #e8e7d0;
    box-sizing: content-box;
    padding-bottom: 20px;
}
.single_item_header{
    height: 20%;
    width: 100%;
    text-align: left;
    box-sizing: border-box;
    border-left: 4px solid #108DE9;
    display: flex;
    align-items: center;
    box-sizing: content-box;
    padding-left: 10px;
    color: #314659;
    text-decoration: none;
    transition: all .3s ease;
    cursor: pointer;
    font-size: 20px;
}
.single_item_conent{
    width: 100%;
    text-align: left;
    margin-top: 10px;
    word-break: break-all;
    overflow: hidden;
    line-height: 1.5;
    height: 100%;
    color: #314659;
    font-family: Lato,"PingFang SC","Microsoft YaHei",sans-serif;
    font-size: 14px;
    font-weight: 300;
}
.single_item_more{
    cursor: pointer;
    color: #1491a8;
}
.single_item_more:hover{
    text-decoration: underline;
}
.homework_type{
    border: 1px solid #314659;
    border-radius: 3px;
    padding: 2px 9px;
    font-size: 13px;
    margin-top: 10px;
    display: table;
    color: #314659;
    text-decoration: none;
    transition: all .3s ease;
    cursor: pointer;
}
.homework_button_list{
    display: flex;
}
.analyse{
    margin-left: 10px;
}
</style>