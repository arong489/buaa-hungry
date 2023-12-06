import {
  Toast
} from 'vant'
import {
  createRouter,
  createWebHistory
} from 'vue-router'
import HomeView from '../views/myHome/HomeView.vue'
import HomeviewforRider from '@/views/myHome/HomeviewforRider.vue'

const routes = [{
  path: '/',
  redirect: '/home' /** 默认路由 */

},
{
  path: '/home',
  name: 'home',
  component: HomeView
},
/// //////////////////
{
  path: '/homeRider',
  name: 'homeRider',
  component: HomeviewforRider
},
/// //////////////////
{
  path: '/cart',
  name: 'cart',
  component: () =>
    import('../views/myCart/MyCart.vue'),
  meta: {
    isAuth: true
  }
},
{
  path: '/mine',
  name: 'mine',
  component: () =>
    import('../views/mine/MyMine.vue'),
  meta: {
    isAuth: true
  }
},
/// ////////////////////////////////////////////
{
  path: '/mine-rider',
  name: 'mine-rider',
  component: () =>
    import('../views/mine/MymineRider.vue'),
  meta: {
    isAuth: true
  }
},
/// ///////////////////////////////////////////
{
  path: '/cart',
  name: 'cart',
  component: () =>
    import('../views/myCart/MyCart.vue'),
  meta: {
    isAuth: true
  }
},
{
  path: '/order',
  name: 'order',
  component: () =>
    import('../views/myOrder/MyOrder.vue'),
  meta: {
    isAuth: true
  }
},
/// ////////////////////////////////////////////////
{
  path: '/rider-order',
  name: 'rider-order',
  component: () =>
    import('../views/myOrder/RiderOrder.vue'),
  meta: {
    isAuth: true
  }
},
/// ////////////////////////////////////////////////
{
  path: '/store',
  name: 'store',
  component: () =>
    import('../views/mystores/MyStore.vue')
},

/// ////////////////////////////////////////
{
  path: '/store-rider',
  name: 'store-rider',
  component: () =>
    import('../views/mystores/RiderStore.vue')
},
/// ////////////////////////////////////////

{
  path: '/ordercreate',
  name: 'ordercreate',
  component: () =>
    import('../views/myOrder/component/OrderCreate.vue'),
  meta: {
    isAuth: true
  }
},
{
  path: '/address',
  name: 'address',
  component: () =>
    import('../views/AddRess/AddRess.vue'),
  meta: {
    isAuth: true
  }
},
{
  path: '/addressedit',
  name: 'addressedit',
  component: () =>
    import('../views/AddRessedit/AddRessedit.vue'),
  meta: {
    isAuth: true
  }
},
{
  path: '/login',
  name: 'login',
  component: () =>
    import('../views/login/MyLogin.vue')
},
{
  path: '/register',
  name: 'register',
  component: () =>
    import('../views/register/MyRegister.vue')
},
{
  path: '/userinfoedit',
  name: 'userinfoedit',
  component: () =>
    import('../views/userinfoedit/UserInfoedit.vue')
},
{
  path: '/favorite',
  name: 'favorite',
  component: () =>
    import('../views/myHome/favorite.vue')
}
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.isAuth) {
    if (localStorage.isLogin === '1') {
      next()
    } else {
      Toast('请登录')
      router.push('/login')
    }
  } else {
    next()
  }
})

export default router
