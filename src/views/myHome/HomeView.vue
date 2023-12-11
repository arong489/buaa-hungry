<template>
  <div class="home">
    <div class="content">
      <div class="header">
        <div class="title">外卖</div>
        <div class="text">
          <van-icon name="location-o" />
          校园食堂外卖
          <van-icon name="arrow" />
        </div>
      </div>
      <div class="main">

        <van-tabs class="van-tabs">
          <van-tab :title="i.tab" v-for="(i, index) in canteenNavList" :key="index">
            <MyStore :store_list='i.data' />
          </van-tab>

        </van-tabs>
      </div>
    </div>

    <MyFooter />

  </div>
</template>

<script>
import MyStore from './components/MyStore.vue'
import MyFooter from '../../components/MyFooter.vue'
import { reactive, toRefs } from '@vue/reactivity'
import { onMounted } from 'vue'
import axios from '../../api/api'
import { Toast } from 'vant'
// @ is an alias to /src

export default {
  name: 'HomeView',
  components: {
    MyStore,
    MyFooter
  },
  setup() {
    const data = reactive({
      canteenNavList: [
        {
          tab: '餐厅',
          data: []
        }
      ]
    })

    onMounted(() => {
      axios.get('/getAllCanteens').then((response) => {
        switch (response.data.status) {
          case 0:
            data.canteenNavList[0].data = response.data.canteens
            break
          default:
            Toast.fail('未知错误')
            break
        }
      })
    })

    return {
      ...toRefs(data)
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
    padding: 10px;
    background-image: linear-gradient(#0099cc, #33cccc);
  }
}
</style>
