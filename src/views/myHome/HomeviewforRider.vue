<template>
  <div class="order">
    <MyHeader title="订单" />
    <div class="content">
      <van-tabs>
        <van-tab title="全部" :key="navData.length">
          <div v-if="allOrders > 0" style="margin-top: var(--van-padding-xs);">
            <van-card v-for="(order, index) in orderData[0]" :key="order.id" @click="showOrderDetail(0, index)">
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
            <van-card v-for="(order, index) in orderData[1]" :key="order.id" @click="showOrderDetail(1, index)">
              <template #title>
                <p><strong>目的地: </strong>{{ order.destination }}</p>
              </template>
              <template #desc>
                <p>
                  <strong>期望送达时间: </strong>{{ order.expected_finish_time }}<br>
                </p>
              </template>
              <template #tags>
                <van-tag type="warning">配送中</van-tag>
              </template>
            </van-card>
            <van-card v-for="(order, index) in orderData[2]" :key="order.id" @click="showOrderDetail(2, index)">
              <template #title>
                <p><strong>目的地: </strong>{{ order.destination }}</p>
              </template>
              <template #desc>
                <p>
                  <strong>期望送达时间: </strong>{{ order.expected_finish_time }}<br>
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
          <div v-if="orderData[index].length > 0" style="margin-top: var(--van-padding-xs);">
            <van-card v-for="(order, orderIndex) in orderData[index]" :key="order.id"
              @click="showOrderDetail(index, orderIndex)">
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
      <van-popup v-model:show="showDetail" round position="bottom" :close-on-click-overlay='false'
        @click-overlay="showDetail = false" :closeable="true" style="height: 100%">
        <OrderDetail :order="orderDetail" :type="orderType" @changeOrder="changeOrder" />
      </van-popup>
    </div>
    <MyFooterforRider />
  </div>
</template>

<script>
import { reactive, toRefs } from '@vue/reactivity'
import MyFooterforRider from '../../components/MyFooterforRider.vue'
import MyHeader from '../../components/MyHeader.vue'
import { useStore } from 'vuex'
import { onMounted, computed } from 'vue'
import axios from '../../api/api'
import { Toast } from 'vant'
import OrderDetail from '../../components/OrderDetail.vue'

export default {
  components: {
    MyFooterforRider,
    MyHeader,
    OrderDetail
  },

  setup() {
    const store = useStore()
    const data = reactive({
      navData: ['未接单', '配送中', '交易完成'],
      orderData: [[], [], []],
      showDetail: false,
      orderDetail: {},
      orderType: 0
    })

    let OrderIndex = 0
    const tabClick = (i) => {
      console.log(i)
    }

    function showOrderDetail(type, index) {
      data.orderDetail = data.orderData[type][index]
      data.orderType = type
      OrderIndex = index
      data.showDetail = true
    }

    function changeOrder(type) {
      if (type === 0) {
        axios.put('/takeOrder', {
          order_id: data.orderDetail.order_id
        }).then((response) => {
          switch (response.data.status) {
            case -2:
              break
            case 0:
              Toast.success('订单已接收')
              const tempOrder = data.orderData[0][OrderIndex]
              data.orderData[0].splice(OrderIndex, 1)
              data.orderData[1].push(tempOrder)
              data.showDetail = false
              break
            case 1:
              Toast.success('订单状态错误')
              break
            default:
              Toast.fail('未知错误')
              break
          }
        })
      }
    }

    onMounted(() => {
      axios.get('/getOrders').then((response) => {
        if (response.data.status !== -2) {
          if (response.data.status !== 0) {
            Toast.fail('未知错误')
          } else {
            data.orderData[0] = response.data.orders
          }
        }
      })
      axios.get('/getDeliveryOrder').then((response) => {
        if (response.data.status !== -2) {
          if (response.data.status !== 0) {
            Toast.fail('未知错误')
          } else {
            data.orderData[1] = response.data.orders
          }
        }
      })
      axios.get('/getStaffHistoryOrder').then((response) => {
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
      showOrderDetail,
      allOrders,
      changeOrder
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
