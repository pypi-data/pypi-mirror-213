import Vue from 'vue';
import VueRouter from 'vue-router';
Vue.use(VueRouter);
const routes = [{
    path: '/',
    component: () => import(/* webpackChunkName: "home" */ '../components/home.vue'),
    meta: {title: 'yyPerf'},
}, {
    path: '/perf',
    component: () => import(/* webpackChunkName: "home" */ '../components/yyPerf.vue'),
    meta: {title: '性能采集'},
}, {
    path: '/wda',
    component: () => import(/* webpackChunkName: "home" */ '../components/uiDebug.vue'),
    meta: {title: 'wda调试'},
},]

const router = new VueRouter({
    routes
})

export default router
router.beforeEach((to, from, next) => {
  document.title = to.meta.title  // 设置页面标题为目标路由的标题
  next()
})