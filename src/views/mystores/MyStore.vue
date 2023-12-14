<template>
  <div class="mystore">
    <Myheader title="餐厅" />
    <div class="content">
      <div class="img"></div>
      <div class="main">
        <div class="name">
          <div class="title">{{ description }}</div>
          <img :src="img">
        </div>
        <div class="classify">
          <van-tabs>
            <van-tab title="点餐">
              <FoodList v-if="canteensInf?.length > 0" :canteensInf="canteensInf" :activeIndex="canteenIndex"
                v-model="cart" @selectCanteen="selectCanteen" />
              <van-empty v-else description="暂无餐厅" />
            </van-tab>
            <van-tab title="评论">
              <Comment v-if="canteensInf?.length > 0" :canteensInf="canteensInf" :activeIndex="canteenIndex"
                @selectCanteen="selectCanteen" />
              <van-empty v-else description="暂无餐厅" />
            </van-tab>
          </van-tabs>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, toRefs, onMounted } from 'vue'
import Myheader from '../../components/MyHeader.vue'
import FoodList from './commponents/FoodList.vue'
import Comment from './commponents/Comment.vue'
import { Toast } from 'vant'
import { useStore } from 'vuex'
import axios from '../../api/api'
export default {
  components: {
    Myheader,
    Comment,
    FoodList
  },
  setup() {
    const store = useStore()
    const data = reactive({
      description: '',
      // 食堂图片（最右）
      img: '',
      canteensInf: [],
      cart: {},
      canteenIndex: 0
    })

    onMounted(async () => {
      data.canteensInf = await axios.get('/getAllCanteens').then(async (response) => {
        switch (response.data.status) {
          case 0:
            data.img = response.data.canteens[0].img
            data.description = response.data.canteens[0].description
            return response.data.canteens
          default:
            Toast.fail('未知错误')
            break
        }
      })
      console.log(data.canteensInf)
      console.log('mount my store')
    })

    function selectCanteen(index) {
      data.canteenIndex = index
      data.img = data.canteensInf[index].img
      data.description = data.canteensInf[index].description
    }

    return {
      ...toRefs(data),
      selectCanteen,
      store
    }
  }
}
</script>

<style lang="less" scoped>
.mystore {
  .content {
    .main {
      background-color: white;
      border-radius: 30px 30px 0 0;
      margin-top: -30px;
      border-radius: 30px 30px 0 0;

      .name {
        height: 90px;
        line-height: 90px;
        display: flex;
        justify-content: space-between;
        padding: 10px;
        position: relative;

        img {
          position: absolute;
          width: 80px;
          height: 80px;
          right: 30px;
          border-radius: 10px;
        }
      }
    }

    .img {
      background-color: transparent;
      width: 100%;
      height: 50px;
    }
  }
}
</style>
