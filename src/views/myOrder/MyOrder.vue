<template>
  <div class="order">
    <MyHeader title="订单" />
    <div class="content">
      <van-tabs>
        <van-tab title="全部" :key="navData.length">
          <div v-if="allOrders > 0" style="margin-top: var(--van-padding-xs);">
            <van-card v-for="order in orderData[0]" :key="order.id">
              <template #title>
                <p><strong>目的地: </strong>{{ order.destination }}</p>
              </template>
              <template #desc>
                <p><strong>期望送达时间: </strong>{{ order.expected_finish_time }}</p>
              </template>
              <template #tags>
                <van-tag type="primary">未接单</van-tag>
              </template>
            </van-card>
            <van-card v-for="order in orderData[1]" :key="order.id">
              <template #title>
                <p><strong>目的地: </strong>{{ order.destination }}</p>
              </template>
              <template #desc>
                <p>
                  <strong>期望送达时间: </strong>{{ order.expected_finish_time }}<br>
                  <strong>配送员: </strong>{{ order.staff_name }}<br>
                  <strong>电话: </strong>{{ order.staff_tele }}
                </p>
              </template>
              <template #tags>
                <van-tag type="waring">配送中</van-tag>
              </template>
            </van-card>
            <van-card v-for="order in orderData[2]" :key="order.id">
              <template #title>
                <p><strong>目的地: </strong>{{ order.destination }}</p>
              </template>
              <template #desc>
                <p>
                  <strong>期望送达时间: </strong>{{ order.expected_finish_time }}<br>
                  <strong>配送员: </strong>{{ order.staff_name }}<br>
                  <strong>电话: </strong>{{ order.staff_tele }}
                </p>
              </template>
              <template #tags>
                <van-tag type="success">已完成</van-tag>
              </template>
            </van-card>
          </div>
          <van-empty description="没有订单" v-else />
        </van-tab>
        <van-tab :title="value" v-for="(value, index) in navData" :key="index">
          <div v-if="orderData[index].length > 0">
            <van-card v-for="order in orderData[index]" :key="order.id">
              <template #title>
                <p><strong>目的地: </strong>{{ order.destination }}</p>
              </template>
              <template #desc>
                <p>
                  <strong>期望送达时间: </strong>{{ order.expected_finish_time }}<br>
                  <span v-if="order.staff_id">
                    <strong>配送员: </strong>{{ order.staff_name }}<br>
                    <strong>电话: </strong>{{ order.staff_tele }}
                  </span>
                </p>
              </template>
            </van-card>
          </div>
          <van-empty description="没有订单" v-else />
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
import { onMounted, computed } from 'vue'
import axios from 'axios'
import { Toast } from 'vant'

export default {
  components: {
    MyFooter,
    MyHeader
  },

  setup() {
    const store = useStore()
    const data = reactive({
      navData: ['未接单', '配送中', '交易完成'],
      orderData: [[], [], []]
    })

    const tabClick = (i) => {
      console.log(i)
    }

    onMounted(() => {
      axios.get('/getNotTakenOrders').then((response) => {
        if (response.data.status !== -2) {
          if (response.data.status !== 0) {
            Toast.fail('未知错误')
          } else {
            data.orderData[0] = response.data.orders
          }
        }
      })
      axios.get('/getBuyerDeliveryOrders').then((response) => {
        if (response.data.status !== -2) {
          if (response.data.status !== 0) {
            Toast.fail('未知错误')
          } else {
            data.orderData[1] = response.data.orders
          }
        }
      })
      axios.get('/getBuyerHistoryOrders').then((response) => {
        if (response.data.status !== -2) {
          if (response.data.status !== 0) {
            Toast.fail('未知错误')
          } else {
            data.orderData[2] = response.data.orders
          }
        }
      })
    })

    const allOrders = computed(() => {
      let temp = 0
      data.orderData.forEach(element => {
        temp += element.length
      })
      return temp
    })

    return {
      ...toRefs(data),
      store,
      tabClick,
      allOrders
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

div {
  .van-card {
    background-color: white;
    border-radius: 10px;
  }
}
</style>
