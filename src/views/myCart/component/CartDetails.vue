<template>
  <div class="cartDetails" v-if="dishes.length > 0">
    <van-card v-for="(dish, key) in dishes" :title="dish.name" :key="`dish${dish.id}`" :price="dish.price"
      :thumb="dish.img" @click="showDishDetail(dish)">
      <template #num>
        <van-stepper v-model="dish.num" theme="round" min="0" :integer="true" button-size="22"
          @plus="onChange(false, key)" @minus="onChange(true, key)" />
        <!-- <van-button type="danger" icon="delete-o" size="mini" /> -->
      </template>
    </van-card>

    <van-popup v-model:show="ifShowDishDetail" position="bottom" :close-on-click-overlay='false'
      @click-overlay="ifShowDishDetail = false" :closeable="true" style="height: 100%;" close-icon-position="top-left"
      close-icon="arrow-left">
      <DishDetail :dish="detailDish" />
    </van-popup>

    <van-submit-bar :price="totalPrice * 100" button-text="提交订单" class="submitall" :disabled="destination.length == 0"
      @submit="onSubmit">
      <template #tip>
        <div v-if="destination.length == 0">
          未完善期望时间和地址, <span @click="addDetail" style="color:cornflowerblue;">点击完善</span>
        </div>
        <div v-else>
          期望{{ formatDate }} 送达{{ destination }}, <span @click="addDetail" style="color:cornflowerblue;">点击修改</span>
        </div>
      </template>
    </van-submit-bar>
    <van-dialog v-model:show="overShow" style="width: 100%;">
      <van-field label="时间">
        <template #input>
          <van-datetime-picker visible-item-count="1" title="期望送达时间" :show-toolbar="false" v-model="expectDate"
            :formatter="formatter" style="width: 100%;padding: 0;" :min-date="minDate" />
        </template>
      </van-field>
      <van-field label="目的地" v-model="destination"></van-field>
    </van-dialog>
  </div>
  <van-empty v-else description="empty!食食物者为俊杰"></van-empty>
</template>
<script>
import { reactive, toRefs } from '@vue/reactivity'
import { useStore } from 'vuex'
import { computed, onMounted } from '@vue/runtime-core'
import { useRouter } from 'vue-router'
import { Toast } from 'vant'
import axios from '../../../api/api'
import DishDetail from '@/components/DishDetail.vue'

export default {
  components: { DishDetail },
  setup() {
    const router = useRouter()
    const store = useStore()

    const data = reactive({
      dishes: [], // 选中的数据
      totalPrice: 0,
      forbidden: true,
      expectDate: new Date(),
      destination: '',
      overShow: false,
      minDate: new Date(),
      ifShowDishDetail: false,
      detailDish: {}
    })

    function onChange(minus, index) {
      event.stopPropagation()
      let num = Number(data.dishes[index].num)
      const dishId = data.dishes[index].id
      if (minus === true) {
        data.totalPrice -= Number(data.dishes[index].price)
        console.log(data.dishes[index].num)
        if (data.dishes[index].num === 1) {
          data.dishes.splice(index, 1)
        }
        num--
      } else {
        data.totalPrice += Number(data.dishes[index].price)
        num++
      }
      axios.put('/changeDishInCart', { dish_id: dishId, num: num }).then(response => {
        if (response.data.status !== 0) {
          Toast.fail('未知错误')
        }
      })
    }

    function addDetail() {
      data.overShow = true
    }

    const formatDate = computed(() => {
      return data.expectDate.getFullYear().toString() + '-' +
        (data.expectDate.getMonth() + 1) + '-' +
        (data.expectDate.getDate().toString()) + ' ' +
        (data.expectDate.getHours().toString()) + ':' +
        data.expectDate.getMinutes().toString()
    })

    function onSubmit() {
      axios.put('/submitOrder', { time: formatDate.value, destination: data.destination }).then(response => {
        if (response.data.status !== 0) {
          Toast.fail('未知错误')
        } else {
          router.push('/order')
        }
      })
    }

    function formatter(type, value) {
      if (type === 'year') {
        return value + '年'
      } else if (type === 'month') {
        return value + '月'
      } else if (type === 'day') {
        return value + '日'
      } else if (type === 'hour') {
        return value + '时'
      } else if (type === 'minute') {
        return value + '分'
      } else if (type === 'second') {
        return value + '秒'
      }
      return value
    }

    function showDishDetail(dish) {
      data.detailDish = dish
      data.ifShowDishDetail = true
    }

    onMounted(() => {
      axios.get('/getCart').then(response => {
        if (response.data.status === 0) {
          data.totalPrice = Number(response.data.total_price)
          data.dishes = response.data.dishes
        } else if (response.data.status === 1) {
          data.totalPrice = 0
          data.dishes = []
        } else {
          Toast.fail('未知错误')
        }
      })
    })

    return {
      store,
      ...toRefs(data),
      onChange,
      addDetail,
      formatter,
      onSubmit,
      formatDate,
      showDishDetail
    }
  }
}
</script>

<style lang="less" scoped>
.cartDetails {
  display: flex;
  flex-direction: column;

  .submitall {
    position: fixed;
    bottom: 46px;
  }
}
</style>
