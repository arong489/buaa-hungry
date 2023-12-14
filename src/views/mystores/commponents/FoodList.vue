<template>
  <div class="foot_list">
    <van-tree-select :main-active-index="activeIndex" :items="items" @click-nav="navClick" height="calc(100vh - 264px)">
      <template #content>
        <div v-if="dishes.length > 0">
          <van-card v-for="(dish, index) of dishes" :title="dish.name" :key="`dish${dish.id}`" :price="dish.price"
            :desc="dish.description" :thumb="dish.img" @click="onClick(index)">
            <template #num>
              <van-stepper v-model="dishCounts[dish.id]" theme="round" min="0" default-value="0" :integer="true"
                button-size="22" @change="onChange(dish.id)" @plus="cartNum++" @minus="cartNum--" />
            </template>
          </van-card>
        </div>
        <van-empty v-else description="暂无菜品" />
      </template>
    </van-tree-select>

    <van-popup v-model:show="showDetail" position="bottom" :close-on-click-overlay='false'
      @click-overlay="showDetail = false" :closeable="true" close-icon-position="top-left" close-icon="arrow-left"
      style="height: 100%;">
      <DishDetail :dish="dishDetail" />
    </van-popup>

    <van-action-bar>
      <van-action-bar-icon icon="cart-o" text="购物车" :badge="cartNum" @click="toCart" />
      <van-action-bar-button type="warning" text="加入购物车" @click="AddCart()" />
      <van-action-bar-button type="danger" text="立即购买" @click="AddCart(true)" />
    </van-action-bar>
  </div>
</template>

<script>
import { reactive, toRefs } from '@vue/reactivity'
import { onMounted, watch } from 'vue'
import axios from '../../../api/api.js'
import { Toast } from 'vant'
import { useRouter } from 'vue-router'
import DishDetail from '@/components/DishDetail.vue'

export default {
  props: ['canteensInf', 'modelValue', 'activeIndex'],
  emits: ['update:modelValue', 'selectCanteen'],
  setup(props, ctx) {
    const data = reactive({
      items: props.canteensInf.map((canteenInf) => ({ text: canteenInf.location })),
      activeIndex: 0,
      dishes: [],
      dishCounts: {},
      cartNum: 0,
      dishDetail: {},
      showDetail: false
    })

    const router = useRouter()
    // 点击左侧导航
    const navClick = (i) => {
      axios.post('/getAvDishes', { id: props.canteensInf[i].id }).then((response) => {
        switch (response.data.status) {
          case 0:
            data.dishes = response.data.dishes
            data.activeIndex = i
            response.data.dishes.forEach((dish) => {
              data.dishCounts[dish.id] += 0
            })
            ctx.emit('selectCanteen', i)
            break
          default:
            Toast.fail('未知错误')
            break
        }
      }).catch((error) => {
        Toast.fail('请求异常')
        console.log(error)
      })
    }

    function onClick(index) {
      data.dishDetail = data.dishes[index]
      data.showDetail = true
    }

    function toCart() {
      router.push('./cart')
    }

    function AddCart(jump) {
      const dishes = []
      Object.keys(props.modelValue).forEach(key => {
        dishes.push({ dish_id: key, num: props.modelValue[key] })
        data.dishCounts[key] = 0
      })
      axios.post('/addDishesToCart', {
        dishes: dishes
      }).then((response) => {
        switch (response.data.status) {
          case 0:
            Toast.success('已加入购物车')
            break
          case -1:
            break
          case -2:
            break
          default:
            Toast.fail('未知错误')
            break
        }
      })
      // 清空
      data.cartNum = 0
      ctx.emit('update:modelValue', {})
      // 是否直接去购买
      if (jump === true) {
        router.push('./cart')
      }
    }

    function onChange(dishId) {
      event.stopPropagation()
      const emitValue = props.modelValue
      if (data.dishCounts[dishId] === 0) {
        delete emitValue[dishId]
      } else {
        emitValue[dishId] = data.dishCounts[dishId]
      }
      ctx.emit('update:modelValue', emitValue)
    }

    watch(() => props.activeIndex, (index, oldIndex) => {
      if (index !== data.activeIndex) {
        axios.post('/getAvDishes', { id: props.canteensInf[index].id }).then((response) => {
          switch (response.data.status) {
            case 0:
              data.dishes = response.data.dishes
              data.activeIndex = index
              response.data.dishes.forEach((dish) => {
                data.dishCounts[dish.id] += 0
              })
              break
            default:
              Toast.fail('未知错误')
              break
          }
        }).catch((error) => {
          Toast.fail('请求异常')
          console.log(error)
        })
      }
    })

    onMounted(async () => {
      data.activeIndex = props.activeIndex
      if (props.canteensInf.length !== 0) {
        axios.request({
          url: '/getAvDishes',
          method: 'post',
          data: {
            id: props.canteensInf[data.activeIndex].id
          }
        }).then((response) => {
          switch (response.data.status) {
            case 0:
              data.dishes = response.data.dishes
              response.data.dishes.forEach((dish) => {
                if (!(dish.id in data.dishCounts)) {
                  data.dishCounts[dish.id] = 0
                }
              })
              break
            default:
              Toast.fail('未知错误')
              break
          }
        })
      }
      console.log('mount food list')
    })
    return {
      ...toRefs(data),
      navClick,
      onChange,
      AddCart,
      toCart,
      onClick
    }
  },
  components: { DishDetail }
}
</script>

<style></style>
