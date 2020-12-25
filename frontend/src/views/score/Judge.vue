<template>
    <div id="group">
        <div class="group_box">
            <c-head></c-head>
            <div class="group_homework_list">
                <div class="group_homework_item" v-for="(item,i) in result" :key="i">
                    <div class="group_item_header">
                        {{item.title}}
                    </div>
                    <div class="group_item_conent">
                        <a target="view_window" :href="item.blogurl" class="group_item_more">{{item.blogurl}}</a>
                        <div class="tasklist_button">
                        <div v-if="role==2||role==3" @click="gettask(item.id,item.title)" class="homework_type">待评分列表>>></div>
                        <div v-if="role==2||role==3" @click="getjudge(item.id,item.title)" class="homework_type">查看评分>>></div>
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
            result:[],
            homeworktype:2
        }
    },
    methods:{
        getlist(){
            this.$api.homework.getlist(this.homeworktype).then(response=>{
                let res=response.data;
                if(res!=undefined){
                    this.result=res.results.filter(item=>item.homeworktype==2);
                }
                else{
                    this.result=[];
                }
            })
        },
        gettask(id,title){
            this.$store.dispatch('setHomeworkName',title)
            this.$router.push({
                path:'/score/list',
                query:{
                    "homeworkid":id,
                    "homeworktype":2
                }
            }
            )
        },
        getjudge(id,title){
            this.$store.dispatch('setHomeworkName',title)
            this.$router.push({
                path:'/score/all',
                query:{
                    "homeworkid":id,
                    "homeworktype":2
                }
            })
        }
    },
    created(){
        this.getlist();
    },
    computed:{
        role(){
            return this.$store.getters.role;
        }
    }
}
</script>
<style scoped>
#group{
    min-height: 100%;
    width: 100%;
    height: auto;
    background: #ffffff;
}
.group_box{
    width: 100%;
    height: 100%;
    box-sizing: content-box;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 1.5%;
}
.group_homework_list{
    position: relative;
    margin-top: 10px;
    width: 92%;
}
.group_homework_item{
    max-height: 200px;
    width: 100%;
    margin-top: 20px;
    border-bottom: 1px dashed #e8e7d0;
    box-sizing: content-box;
    padding-bottom: 20px;
}
.group_item_header{
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
.group_item_conent{
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
.group_item_more{
    cursor: pointer;
    color: #1491a8;
}
.group_item_more:hover{
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
.group_item_more{
    cursor: pointer;
    color: #1491a8;
}
.group_item_more:hover{
    text-decoration: underline;
}
.tasklist_button{
    width: 100%;
    display: flex;
}
.homework_type{
    border: 1px solid #314659;
    border-radius: 3px;
    padding: 2px 9px;
    font-size: 13px;
    height: 25px;
    display: flex;
    line-height: 25px;
    align-items: center;
    justify-content: center;
    margin-top: 10px;
    display: table;
    color: #314659;
    text-decoration: none;
    transition: all .3s ease;
    cursor: pointer;
    margin-right: 10px;
}
</style>