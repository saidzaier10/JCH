import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import('../views/HomeView.vue')
        },
        {
            path: '/inscription',
            name: 'registration',
            component: () => import('../views/RegistrationView.vue')
        },
        {
            path: '/dashboard',
            name: 'dashboard',
            component: () => import('../views/AdminDashboard.vue'),
            meta: { requiresAuth: true, requiresAdmin: true }
        },
        {
            path: '/events',
            name: 'events',
            component: () => import('../views/EventsView.vue')
        },
        {
            path: '/gallery',
            name: 'gallery',
            component: () => import('../views/GalleryView.vue')
        },
        {
            path: '/contact',
            name: 'contact',
            component: () => import('../views/ContactView.vue')
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('../views/LoginView.vue')
        },
        {
            path: '/admin/login',
            name: 'admin-login',
            component: () => import('../views/LoginView.vue')
        },
        {
            path: '/signup',
            name: 'signup',
            component: () => import('../views/SignupView.vue')
        },
        {
            path: '/my-space',
            name: 'parent-dashboard',
            component: () => import('../views/ParentDashboard.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/payment/success',
            name: 'payment-success',
            component: () => import('../views/PaymentSuccess.vue')
        },
        {
            path: '/payment/cancel',
            name: 'payment-cancel',
            component: () => import('../views/PaymentCancel.vue')
        },
    ]
})

router.beforeEach((to, from, next) => {
    const isAuthenticated = !!localStorage.getItem('access_token')
    const isStaff = localStorage.getItem('is_staff') === 'true'

    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/login')
    } else if (to.meta.requiresAdmin && !isStaff) {
        next('/my-space') // Redirect non-admins to parent dashboard
    } else {
        next()
    }
})

export default router
