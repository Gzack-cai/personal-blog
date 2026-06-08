import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/profile' },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
  },
  {
    path: '/projects',
    name: 'Projects',
    component: () => import('@/views/Projects.vue'),
  },
  {
    path: '/articles',
    name: 'Articles',
    component: () => import('@/views/Articles.vue'),
  },
  {
    path: '/life',
    name: 'Life',
    component: () => import('@/views/Life.vue'),
  },
  {
    path: '/friends',
    name: 'Friends',
    component: () => import('@/views/Friends.vue'),
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('@/views/Contact.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
