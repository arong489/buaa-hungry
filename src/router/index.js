import {
  Toast
} from 'vant'
import {
  createRouter,
  createWebHistory
} from 'vue-router'
import HomeView from '../views/myHome/HomeView.vue'
import HomeviewforRider from '@/views/myHome/HomeviewforRider.vue'
import HomeViewCanteen from '@/views/myHome/HomeViewCanteen.vue'

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
{
  path: '/homeCanteen',
  name: 'homeCanteen',
  component: HomeViewCanteen
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
{
  path: '/mineCanteen',
  name: 'mineCanteen',
  component: () =>
    import('../views/mine/MyCanteenMine.vue'),
  meta: {
    isAuth: true
  }
},
{
  path: '/mineRider',
  name: 'mineRider',
  component: () =>
    import('../views/mine/MyRiderMine.vue'),
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
  path: '/store',
  name: 'store',
  component: () =>
    import('../views/mystores/MyStore.vue')
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
  path: '/registerForDish',
  name: 'registerForDish',
  component: () =>
    import('../views/myHome/RigisterForDish.vue')
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
},
{
  path: '/commentmanger',
  name: 'commentmanger',
  component: () =>
    import('../views/myHome/CommentManager.vue')
}

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.isAuth) {
    if (localStorage.getItem('token')) {
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
