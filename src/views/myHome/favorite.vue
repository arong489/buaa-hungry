
<template>
  <div class="favorites" style="height: 100%;">
    <MyHeader title="我的收藏" />
    <van-loading v-if="loading" size="30%" style="top: 50%;translate: 0 -50%;text-align:center;"></van-loading>
    <div v-else-if="favoriteDishes.length > 0">
      <van-swipe-cell v-for="dish in favoriteDishes" :key="`dish${dish.dish_id}`">
        <template>
          <van-card :title="dish.name" :thumb="dish.img" :desc="dish.description" :price="dish.price"></van-card>
        </template>
        <template #right><van-button type="warning">删除</van-button></template>
      </van-swipe-cell>
    </div>
    <van-empty v-else description="就决定是你了, 拔叔法国清新柠檬小鹅肝" />
  </div>
</template>

<script>
import { Toast } from 'vant'
import axios from '../../api/api'
import { reactive, toRefs, onMounted } from 'vue'
import MyHeader from '@/components/MyHeader.vue'

export default {
  setup() {
    const data = reactive({
      favoriteDishes: [],
      loading: true
    })

    onMounted(() => {
      axios.get('/getFavorite').then((response) => {
        switch (response.data.status) {
          case 0:
            data.favoriteDishes = response.data.dishes
            break
          case -2:
            break
          default:
            Toast.fail('未知错误')
            break
        }
      }).finally(() => { data.loading = false })
    })

    return ({
      ...toRefs(data)
    })
  },
  components: { MyHeader }
}
</script>
