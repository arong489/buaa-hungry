
<template>
  <div class="favorites" style="height: 100%;">
    <MyHeader title="我的收藏" />
    <van-loading v-if="loading" size="30%" style="top: 50%;translate: 0 -50%;text-align:center;"></van-loading>
    <div v-else-if="favoriteDishes.length > 0">
      <van-swipe-cell v-for="(dish, index) in favoriteDishes" :key="`dish${dish.dish_id}`">
        <van-card :title="dish.name" :thumb="dish.img" :desc="dish.description" :price="dish.price"
          style="margin: 5px;background-color: white;border-radius: 15px;"></van-card>
        <template #right><van-button type="danger" style="height: 100%;"
            @click="dislike(index)">取消<br>收藏</van-button></template>
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

    function dislike(index) {
      axios.post('/deleteFavorite', {
        dish_id: data.favoriteDishes[index].dish_id
      }).then((response) => {
        switch (response.data.status) {
          case 0:
            data.favoriteDishes.splice(index, 1)
            Toast.success('已取消收藏')
            break
          case 1:
            Toast.fail('未收藏过该菜品')
            break
          case -2:
            break
          default:
            Toast.fail('未知错误')
            break
        }
      })
    }

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
      ...toRefs(data),
      dislike
    })
  },
  components: { MyHeader }
}
</script>
