<template>
    <div id="content_head">
        <div class="content__head_line"></div>
        <div class="content_head_route">
            {{this.$route.meta.parentName}}-{{this.$route.meta.name}}
        </div>
    </div>
</template>
<style scoped>
#content_head{
    width: 100%;
    display: flex;
    height: 8%;
    align-items: flex-end;
    position: relative;
    box-sizing: content-box;
    padding-left: 3%;
    max-height: 48px;
}
.content__head_line{
    width: 4px;
    height: 60%;
    background: #01284D;
    position: absolute;
    top: 40%;
    border-radius: 1.5px;
}
.content_head_route{
    margin-left: 10px;
    font-size: 18px;
    color: #01284D;
    font-weight: 600;
}
</style>