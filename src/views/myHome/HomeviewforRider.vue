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
        <div class="classify">
          <div class="big_classify">
            <div v-for="i in big_classify" :key="i.name">
              <svg class="icon svg-icon" aria-hidden="true">
                <use :xlink:href="`${i.icon}`"></use>
              </svg>
              {{i.name}}
            </div>
          </div>
          <div class="small_classify">
            <div v-for="(i,index) in small_classify" :key="index">
              <svg class="icon svg-icon" aria-hidden="true">
                <use :xlink:href="`${i.icon}`"></use>
              </svg>
              {{i.name}}
            </div>
          </div>
        </div>

        <van-tabs class="van-tabs">
          <van-tab :title="i.tab" v-for="(i,index) in centent_nav_list" :key="index">
            <RiderStore :store_list='i.data'/>
          </van-tab>

        </van-tabs>
      </div>
    </div>

    <MyFooterforRider />

  </div>
</template>

<script>
import RiderStore from './components/RiderStore.vue'
import MyFooterforRider from '../../components/MyFooterforRider.vue'
import { reactive, toRefs } from '@vue/reactivity'
// @ is an alias to /src

export default {
  name: 'HomeViewforRider',
  components: {
    RiderStore,
    MyFooterforRider
  },
  setup () {
    const data = reactive({
      centent_nav_list: [                       //此处为提供外卖服务的几个地点的展示
        {
          tab: '订单',
          data: [
            {
              pic: 'https://5b0988e595225.cdn.sohucs.com/images/20180904/c46bb31bd1b240b792ef2a40816c7b9a.jpeg',
              title: '沙河订单',
              price: '20',
            },
            {
              pic: 'https://img1.baidu.com/it/u=3211807031,2781908075&fm=253&fmt=auto&app=138&f=JPEG?w=667&h=500',
              title: '学院路学二订单',
              price: '20',
            },
            {
              pic: 'https://pic2.zhimg.com/80/v2-265affebcd2c3c966e49afd8a0c3b501_720w.webp',
              title: '学院路合一订单',
              price: '20',
            },
            {
              pic: 'https://img1.baidu.com/it/u=1313264085,1652997716&fm=253&fmt=auto&app=138&f=JPEG?w=845&h=500',
              title: '学院路新北订单',
              price: '20',
            }
          ]
        },
      ]
    })

    return {
      ...toRefs(data)
    }
  }

}
</script>

<style lang="less" scoped>
.home{
  height: 100%;
  display: flex;
  flex-flow: column;
  .content{
    flex: 1;
    overflow-y: auto;
  }
  .main {
    font-size: 12px;

    .classify {
      padding: 10px;

      .small_classify {
        display: flex;
        flex-wrap: wrap; /** 超出可以换行*/
        margin-top: 20px;

        div {
          display: flex;
          width: 20%;
          justify-content: center; /**可以水平居中显示 */
          align-items: center; /*垂直居中*/
          flex-flow: column; /**方向是垂直方向 */

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
          flex: 1; /** 均分 */
          display: flex;
          justify-content: center; /**可以水平居中显示 */
          align-items: center; /*垂直居中*/
          flex-flow: column; /**方向是垂直方向 */

          .svg-icon {
            width: 50px;
            height: 50px;
            margin-bottom: 5px;
          }
        }
      }
    }
  }
  .header{
    display: flex;
    justify-content: space-between;
    padding: 10px;
    background-image:linear-gradient(#0099cc,#33cccc);
  }
}
</style>
