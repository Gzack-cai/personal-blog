import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './styles/global.css'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/profile' },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('./views/Profile.vue'),
    },
    {
      path: '/projects',
      name: 'Projects',
      component: () => import('./views/Projects.vue'),
    },
    {
      path: '/articles',
      name: 'Articles',
      component: () => import('./views/Articles.vue'),
    },
    {
      path: '/life',
      name: 'Life',
      component: () => import('./views/Life.vue'),
    },
    {
      path: '/friends',
      name: 'Friends',
      component: () => import('./views/Friends.vue'),
    },
    {
      path: '/contact',
      name: 'Contact',
      component: () => import('./views/Contact.vue'),
    },
    {
      path: '/music',
      name: 'Music',
      component: () => import('./views/Music.vue'),
    },
    {
      path: '/admin',
      name: 'Admin',
      component: () => import('./views/Admin.vue'),
    },
  ],
})

const app = createApp(App)
app.use(router)
app.mount('#app')
