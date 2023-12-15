<template>
  <p>
    <van-field v-model="order.destination" readonly>
      <template #label>
        <strong style="font-size: large;">目的地: </strong>
      </template>
    </van-field>
    <van-field v-model="order.expected_finish_time" readonly>
      <template #label>
        <strong style="font-size: large;">期望送达时间: </strong>
      </template>
    </van-field>
    <van-field v-model="totalPrice" readonly>
      <template #label>
        <strong style="font-size: large;">总计: </strong>
      </template>
    </van-field>
    <span v-if="order.staff_id">
      <van-field v-model="order.staff_name" readonly>
        <template #label>
          <strong style="font-size: large;">配送员: </strong>
        </template>
      </van-field>
      <van-field v-model="order.staff_tele" readonly>
        <template #label>
          <strong style="font-size: large;">电话: </strong>
        </template>
      </van-field>
    </span>
  </p>

  <van-button style="float: right;margin-right: 3%;" v-if="buttonText.length > 0" type="primary" @click="onClick">{{
    buttonText }}</van-button>

  <van-field readonly>
    <template #label>
      <strong style="font-size: large;">菜品:</strong>
    </template>
  </van-field>
  <van-card v-for="(dish, index) of dishes" :title="dish.name" :key="`dish${index}`" :price="dish.price"
    :desc="dish.description" :thumb="dish.img" :num="dish.num" @click="showDishDetail(dish)">
  </van-card>

  <van-popup v-model:show="ifShowDishDetail" position="bottom" :close-on-click-overlay='false'
    @click-overlay="ifShowDishDetail = false" :closeable="true" style="height: 100%;" close-icon-position="top-left"
    close-icon="arrow-left">
    <DishDetail :dish="detailDish" />
  </van-popup>
</template>

<script lang="js">
import { Toast } from 'vant'
import axios from '../api/api'
import { reactive, toRefs, watch } from 'vue'
import DishDetail from './DishDetail.vue'

export default {
  props: ['order', 'type'],
  emits: ['changeOrder'],
  components: { DishDetail },
  setup(props, ctx) {
    const data = reactive({
      dishes: [],
      totalPrice: 0,
      buttonText: '',
      ifShowDishDetail: false,
      detailDish: {}
    })

    watch(
      () => props.order,
      (order, preOrder) => {
        const people = localStorage.getItem('identity')
        switch (props.type) {
          case 0:
            data.buttonText = people === '0' ? '取消' : people === '1' ? '接单' : ''
            break
          case 1:
            data.buttonText = people === '0' ? '完成' : ''
            break
          default:
            data.buttonText = ''
            break
        }
        const orderId = order.id ? order.id : order.order_id
        axios.post('/getOrderInfo', {
          order_id: orderId
        }).then((response) => {
          switch (response.data.status) {
            case 0:
              data.totalPrice = response.data.total_price
              data.dishes = response.data.dishes
              break
            case 1:
              Toast.fail('订单不存在')
              break
            case -2:
              break
            default:
              Toast.fail('未知错误')
              break
          }
        })
      },
      { immediate: true }
    )

    function onClick() {
      ctx.emit('changeOrder', props.type)
    }

    function showDishDetail(dish) {
      data.detailDish = dish
      data.ifShowDishDetail = true
    }

    return { ...toRefs(data), onClick, showDishDetail }
  }
}
</script>
