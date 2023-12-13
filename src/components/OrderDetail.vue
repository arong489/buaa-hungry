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
  <van-divider />
  <van-field readonly>
    <template #label>
      <strong style="font-size: large;">菜品:</strong>
    </template>
  </van-field>
  <van-card v-for="(dish, index) of dishes" :title="dish.name" :key="`dish${index}`" :price="dish.price"
    :desc="dish.description" :thumb="dish.img" :num="dish.num">
  </van-card>
</template>

<script lang="js">
import { Toast } from 'vant'
import axios from '../api/api'
import { reactive, toRefs, watch } from 'vue'

export default {
  props: ['order'],
  setup(props) {
    const data = reactive({
      dishes: [],
      totalPrice: 0
    })

    watch(
      () => props.order,
      (order, preOrder) => {
        console.log(order)
        axios.post('getOrderInfo', {
          order_id: order.id
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

    return { ...toRefs(data) }
  }
}
</script>
