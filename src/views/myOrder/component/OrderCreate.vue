<template>
  <div class="order-details">
    <div class="content">
      <MyHeader title="订单" />
      <div>
        <van-contact-card type="edit" :tel="createuser.tel" :name="createuser.name" @click="onEdit" />
        <div v-for="(i, index) in store.state.orderList" :key="index">
          <van-card :num="i.num" :price="i.price" :title="i.title" :thumb="i.pic" />
        </div>
      </div>
      <div class="footer">
        <div class="price">
          <div>商品金额</div>
          <div>￥{{ allPrice }}</div>
        </div>
        <div class="button" @click="buy">生成订单</div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, toRefs } from '@vue/reactivity'
import { useStore } from 'vuex'
import MyHeader from '../../../components/MyHeader.vue'
import { computed, onMounted } from '@vue/runtime-core'
import { useRoute, useRouter } from 'vue-router'
import { Dialog } from 'vant'
export default {
  components: {
    MyHeader
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    const route = useRoute()

    const data = reactive({
      createuser: {
        name: '',
        tel: ''
      },
      allPrice: 0
    })

    // 初始化用户
    const initUser = () => {
      store.state.userAddress.forEach((item) => {
        if (item.isDefault) {
          data.createuser.name = item.name
          data.createuser.tel = item.tel
        }
      })
    }

    // 初始化用户价格
    const initPrice = () => {
      let sum = 0
      if (store.state.orderList) {
        store.state.orderList.forEach(item => {
          sum += item.num * item.price
        })
        data.allPrice = sum
      }
    }

    onMounted(() => {
      initUser()
      initPrice()
    })

    // 生成订单按钮
    const buy = () => {
      Dialog.alert({
        title: '订单',
        message: '订单已完成。'
      }).then(() => {
        const newList = store.state.cartList.forEach((item) => {
          return !route.query.list.includes(item.id + '')
        })
        store.commit('DELETE', newList)
        store.commit('UPORDERLIST')
        router.push('/order')
      })
    }

    // 点击编辑
    const onEdit = () => {
      router.push('/address')
    }

    return {
      store,
      ...toRefs(data),
      onEdit,
      buy
    }
  }
}
</script>

<style lang="less" scoped>
.order-details {
  .content {
    .footer {
      width: 100%;
      height: 100px;
      position: fixed;
      bottom: 0px;
      background: white;
      border: 1px solid white;
      padding: 10px 0;

      .price {
        display: flex;
        justify-content: space-between;
        padding: 10px;
        margin-bottom: 10px;
      }

      .button {
        display: flex;
        justify-content: center;
        align-items: center;
        flex: 1;
        background: yellow;
        padding: 10px;
      }
    }
  }
}
</style>
