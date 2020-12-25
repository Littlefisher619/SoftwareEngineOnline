<template>
    <div id="duigou">
        <div class="icon_canvas">
            <input type="checkbox" v-model="check" class="checkbox_con">
            <svg>
                <circle class="circle" fill="none" stroke="#3585F7" stroke-width="4" cx="30" cy="30" r="28.5"
                    stroke-linecap="round" transform="rotate(-13.5,30,30)" />
                <polyline class="tick" fill="none" stroke="#3585F7" stroke-width="4" points="13.2,32.1 25.95,42.6 45.6,20.7"
                    stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            <h2>{{this.tips}}</h2>
        </div>
    </div>
</template>
<script>
export default {
    data(){
        return{
            // check:this.ischeck
            check:true
        }
    },
    props:["ischeck","tips"]
}
</script>
<style scoped>
.icon_canvas{
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    width: 100%;
    height: 100%;
    flex-direction: column;
}

svg {
    width: 60px;
	height: 60px;
}

h2 {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    font-size: 20px;
    margin-top: 10px;
    color: #333;
    opacity: 0;
}
.checkbox_con{
    width: 0;
    height: 0;
    padding: 0;
}
input[type="checkbox"]:checked~h2 {
    animation: .6s title ease-in-out;
    animation-delay: 1.2s;
    animation-fill-mode: forwards;
}

.circle {
    stroke-dasharray:179.1;
    stroke-dashoffset: 179.1;
}

@keyframes circle {
    from {
        stroke-dashoffset: 179.1;
    }
    to {
        stroke-dashoffset: 358.2;
    }
}

input[type="checkbox"]:checked+svg .circle {
    animation: circle 1s ease-in-out;
    animation-fill-mode: forwards;
}

.tick {
    stroke-dasharray: 52.5;
    stroke-dashoffset: 52.5;
}

@keyframes tick {
    from {
        stroke-dashoffset: 52.5;
    }
    to {
        stroke-dashoffset: 0;
    }
}

input[type="checkbox"]:checked+svg .tick {
    animation: tick 0.8s ease-in-out;
    animation-fill-mode: forwards;
    animation-delay: .95s;
}

@keyframes title {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}


</style>