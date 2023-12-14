<template>
  <div class="home">
    <div class="content">
      <div class="header">
        <div class="title">食堂管理</div>
        <div class="text">
          <van-icon name="location-o" />
          校园食堂外卖
          <van-icon name="arrow" />

        </div>
        <!--展示菜品-->
      </div>
      <van-tabs class="van-tabs">
        <div v-if="dishes.length > 0">
          <van-card v-for="(dish, index) of dishes" :title="dish.name" :key="`dish${dish.id}`" :price="dish.price"
            :desc="dish.description" :thumb="dish.img" @click="onClick(index, dish)" :tag="dish.available ? '' : '停售'">
          </van-card>
        </div>
        <van-loading v-else-if="loading" size="50%" style="padding-top: 25%; padding-left: 30%;"></van-loading>
        <van-empty v-else description="暂无菜品" />
      </van-tabs>

      <van-popup v-model:show="showDetail" position="bottom" :close-on-click-overlay='false'
        @click-overlay="showDetail = false" :closeable="true" close-icon-position="top-left" close-icon="arrow-left"
        style="height: 100%;">
        <DishDetail :dish="dishDetail" @stopSale="stopSale" @dishModify="dishModify" />
      </van-popup>

    </div><!--添加按钮-->
    <van-button type="primary" size="large" color="#336699" round @click="AddDish">添加新菜品</van-button>
    <FooterCanteen />
  </div>
</template>

<script>
import { reactive, toRefs } from '@vue/reactivity'
import { createApp, onMounted } from 'vue'
import { ContactCard, Toast, SwipeCell } from 'vant'

import router from '@/router'
import axios from 'axios'
import FooterCanteen from '../../components/FooterCanteen.vue'
import DishDetail from '@/components/DishDetail.vue'

const app = createApp()
app.use(ContactCard)
app.use(SwipeCell)

// @ is an alias to /src

export default {
  name: 'HomeViewCanteen',
  components: {
    DishDetail,
    FooterCanteen
  },
  setup() {
    let account
    const data = reactive({
      account,
      dishes: [], // 存储所有的菜
      loading: true,
      dishDetail: {},
      showDetail: false
    })
    const AddDish = () => {
      router.push('/registerForDish')
    }

    onMounted(() => { // 获取餐厅菜品
      axios.post('/getAllDishes').then((response) => {
        switch (response.data.status) {
          case 0:
            data.dishes = response.data.dishes
            break
          default:
            Toast.fail('未知错误')
            break
        }
        data.loading = false
      }).catch((error) => {
        Toast.fail('请求异常')
        console.log(error)
        data.loading = false
      })
    })

    let detailDishIndex = 0
    function onClick(index, dish) {
      data.dishDetail = dish
      detailDishIndex = index
      data.showDetail = true
    }

    function stopSale() {
      data.dishes[detailDishIndex].available = false
    }

    function dishModify(modifiedDish) {
      data.dishes[detailDishIndex] = modifiedDish
    }

    return {
      ...toRefs(data),
      AddDish,
      onClick,
      stopSale,
      dishModify
    }
  }

}
</script>

<style lang="less" scoped>
.home {
  height: 100%;
  display: flex;
  flex-flow: column;

  .content {
    flex: 1;
    overflow-y: auto;
  }

  .main {
    font-size: 12px;

    .classify {
      padding: 10px;

      .small_classify {
        display: flex;
        flex-wrap: wrap;
        /** 超出可以换行*/
        margin-top: 20px;

        div {
          display: flex;
          width: 20%;
          justify-content: center;
          /**可以水平居中显示 */
          align-items: center;
          /*垂直居中*/
          flex-flow: column;
          /**方向是垂直方向 */

          .svg-icon {
            width: 30px;
            height: 30px;
            margin-bottom: 5px;
          }
        }
      }

      .big_classify {
        display: flex;

        div {
          flex: 1;
          /** 均分 */
          display: flex;
          justify-content: center;
          /**可以水平居中显示 */
          align-items: center;
          /*垂直居中*/
          flex-flow: column;
          /**方向是垂直方向 */

          .svg-icon {
            width: 50px;
            height: 50px;
            margin-bottom: 5px;
          }
        }
      }
    }
  }

  .header {
    display: flex;
    justify-content: space-between;
    padding: 20px;
    background-image: linear-gradient(#0099cc, #33cccc);
  }
}
</style>
