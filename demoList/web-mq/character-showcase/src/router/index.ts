import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

// 懒加载视图组件
const WorldView = () => import('../views/WorldView.vue')
const CharactersView = () => import('../views/CharactersView.vue')

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'world',
    component: WorldView,
    meta: {
      title: '昆墟 - 世界观',
    },
  },
  {
    path: '/characters',
    name: 'characters',
    component: CharactersView,
    meta: {
      title: '角色展示',
    },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫 - 设置页面标题
router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = `${to.meta.title} - 没钱修什么仙`
  }
  next()
})

export default router
