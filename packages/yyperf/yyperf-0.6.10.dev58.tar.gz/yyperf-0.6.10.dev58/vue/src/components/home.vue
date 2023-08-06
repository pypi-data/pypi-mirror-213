<template>
    <div id="main" style="height: 100vh">
        <div class="container">
            <el-card>
                <img @click="debug" src="../assets/debug.png"
                     class="image">
                <div style="padding: 14px;text-align: center">
                    <span>手机调试</span>
                </div>
            </el-card>
            <el-card>
                <img @click="perf" src="../assets/performance.png"
                     class="image">
                <div style="padding: 14px;text-align: center">
                    <span>性能采集</span>
                </div>
            </el-card>
        </div>
    </div>
</template>

<script>

export default {
    name: 'App',
    computed: {},
    data() {
        return {}
    }, methods: {
        perf() {
            window.open("#/perf", "_blank")
        },
        debug() {
            window.open("#/wda", "_blank")
        }
    }
}
</script>

<style scoped>
.container {
    display: flex;
    justify-content: center; /* 水平居中 */
    align-items: center; /* 垂直居中 */
    width: 100%;
    height: 100vh
}

.container > div {
    margin: 10px; /* 为了增加div之间的间距，可根据需求自行调整 */
}


.image {
    width: 300px;
    height: 200px;
    object-fit: contain;
    display: block;
}


#main {
    background: linear-gradient(to bottom right, rgba(255, 173, 66, 0.8), rgba(255, 111, 0, 0.8));
}

.el-card.is-always-shadow:hover {
    transform: scale(1.05);
}
</style>
