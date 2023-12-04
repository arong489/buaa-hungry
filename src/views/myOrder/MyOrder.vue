<template>
  <div class="order">
    <MyHeader title="订单" />
    <div class="content">
      <van-tabs>
        <van-tab :title="i" v-for="(i, index) in navData" :key="index">
          <div v-for="(item, index) in store.state.orderLists" :key="index"
            v-if="i === '全部' && store.state.orderLists.length">
            <van-card :num="item.num" :price="item.price" :title="item.title" :thumb="item.pic" />
          </div>
          <MyBack v-else />
        </van-tab>
      </van-tabs>
    </div>
    <MyFooter />
  </div>
</template>

<script>
import { reactive, toRefs } from '@vue/reactivity'
import MyFooter from '../../components/MyFooter.vue'
import MyHeader from '../../components/MyHeader.vue'
import { useStore } from 'vuex'
import MyBack from '../../components/MyBack.vue'

export default {
  components: {
    MyFooter,
    MyHeader,
    MyBack
  },

  setup() {
    const store = useStore()
    const data = reactive({
      navData: ['全部', '未接单', '配送中', '交易完成']
    })

    const tabClick = (i) => {
      console.log(i)
    }

    return {
      ...toRefs(data),
      store,
      tabClick
    }
  }
}
</script>

<style lang="less" scoped>
.order {
  height: 100%;
  display: flex;
  flex-flow: column;

  .content {
    flex: 1;
    overflow-y: auto;
    position: relative;
  }
}
</style>
