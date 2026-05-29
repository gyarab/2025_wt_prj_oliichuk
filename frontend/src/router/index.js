import { createRouter, createWebHistory } from 'vue-router' 
import MatchList from '../components/MatchList.vue'
import MatchDetail from '../components/MatchDetail.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', name: 'home', component: MatchList },
        { path: '/matches/:id', name: 'match-detail', component: MatchDetail },    
    ],
    history: createWebHistory(),
})

export default router