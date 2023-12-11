<template>
  <div class="mystore">
    <Myheader title="餐厅" />
    <div class="content">
      <div class="img"></div>
      <div class="main">
        <div class="name">
          <div class="title">{{ title }}</div>
          <img :src="img">
        </div>
        <div class="classify">
          <van-tabs>
            <van-tab title="点餐">
              <FoodList v-if="canteensInf?.length > 0" :canteensInf="canteensInf" v-model="cart" />
            </van-tab>
            <van-tab title="简介"></van-tab>
          </van-tabs>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, toRefs } from '@vue/reactivity'
import Myheader from '../../components/MyHeader.vue'
import FoodList from './commponents/FoodList.vue'
import Comment from './commponents/Comment.vue'
import { Toast } from 'vant'
import { useStore } from 'vuex'
import axios from '../../api/api'
import { onMounted } from 'vue'
export default {
  components: {
    Myheader,
    // Comment,
    FoodList
  },
  setup() {
    const store = useStore()
    const data = reactive({
      title: 'Canteen',
      // 食堂图片（最右）
      img: 'https://5b0988e595225.cdn.sohucs.com/images/20191206/1d819332644641c7800feef9eaa2eef5.jpeg',
      canteensInf: [],
      cart: {}
    })

    onMounted(async () => {
      data.canteensInf = await axios.get('/getAllCanteens').then(async (response) => {
        switch (response.data.status) {
          case 0:
            return response.data.canteens
          default:
            Toast.fail('未知错误')
            break
        }
      })
      console.log(data.canteensInf)
      console.log('mount my store')
    })

    return {
      ...toRefs(data),
      // AddCart,
      store
      // clickBuy,
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
