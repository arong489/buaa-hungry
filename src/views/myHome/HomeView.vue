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
      <div class="search">
        <input type="text">
        <div class="search_text">搜索</div>
      </div>
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
          <MyStore :store_list='i.data'/>
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
// @ is an alias to /src

export default {
  name: 'HomeView',
  components: {
    MyStore,
    MyFooter
  },
  setup () {
    const data = reactive({
      centent_nav_list: [
        {
          tab: '人气',
          data: [
            {
              pic: 'https://img1.baidu.com/it/u=1599947592,1695977044&fm=253&fmt=auto&app=138&f=JPEG?w=640&h=440',
              title: '鱼拿酸菜鱼',
              sales: '2888',
              price: '20',
              label: ['门店上新', '很下饭']
            },
            {
              pic: 'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fwww.cfcy168.com%2FUploadFiles%2F2020%2F2%2F15904074889874037.jpg&refer=http%3A%2F%2Fwww.cfcy168.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1645421933&t=66b58fbba9dce6f6b397e38820de24dc',
              title: '隆江猪脚饭',
              sales: '2888',
              price: '20',
              label: ['门店上新', '很下饭']
            },
            {
              pic: 'https://img1.baidu.com/it/u=1599947592,1695977044&fm=253&fmt=auto&app=138&f=JPEG?w=640&h=440',
              title: '鱼拿酸菜鱼',
              sales: '2888',
              price: '20',
              label: ['门店上新', '很下饭']
            },
            {
              pic: 'https://img1.baidu.com/it/u=1599947592,1695977044&fm=253&fmt=auto&app=138&f=JPEG?w=640&h=440',
              title: '鱼拿酸菜鱼',
              sales: '2888',
              price: '20',
              label: ['门店上新', '很下饭']
            }
          ]
        },
        {
          tab: '实惠',
          data: [
            {
              pic: 'https://img1.baidu.com/it/u=1599947592,1695977044&fm=253&fmt=auto&app=138&f=JPEG?w=640&h=440',
              title: '鱼拿酸菜鱼',
              sales: '2888',
              price: '20',
              label: ['门店上新', '很下饭']
            }
          ]
        },
        {
          tab: '高分',
          data: [
            {
              pic: 'https://img1.baidu.com/it/u=1599947592,1695977044&fm=253&fmt=auto&app=138&f=JPEG?w=640&h=440',
              title: '鱼拿酸菜鱼',
              sales: '2888',
              price: '20',
              label: ['门店上新', '很下饭']
            },
            {
              pic: 'https://img1.baidu.com/it/u=1599947592,1695977044&fm=253&fmt=auto&app=138&f=JPEG?w=640&h=440',
              title: '鱼拿酸菜鱼',
              sales: '2888',
              price: '20',
              label: ['门店上新', '很下饭']
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
  .main{
    font-size: 12px;
    .classify{
      padding: 10px;
      .small_classify{
        display: flex;
        flex-wrap: wrap;  /** 超出可以换行*/
        margin-top: 20px;
        div{
          display: flex;
          width: 20%;
          justify-content: center;   /**可以水平居中显示 */
          align-items: center;      /*垂直居中*/
          flex-flow: column;       /**方向是垂直方向 */
          .svg-icon{
            width: 30px;
            height: 30px;
            margin-bottom: 5px;
          }
        }
      }

      .big_classify{
        display: flex;
        div{
          flex: 1;/** 均分 */
          display: flex;
          justify-content: center;   /**可以水平居中显示 */
          align-items: center;      /*垂直居中*/
          flex-flow: column;       /**方向是垂直方向 */
          .svg-icon{
            width: 50px;
            height: 50px;
            margin-bottom: 5px;
          }
        }
      }
    }

    .search{
      padding: 10px;
      display: flex;
      position: relative;
      .search_text{
        position:absolute;
        right: 10px;
        top: 11px;
        background: #666699;
        height: 32px;
        width: 50px;
        line-height: 32px;
        text-align: center;
        border-radius: 16px;
      }
      input{
        width: 100%;
        border-radius: 20px;
        height: 30px;
        border: 1px solid #0066cc;
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
