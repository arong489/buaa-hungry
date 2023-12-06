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
          <div>
            <van-tabs>
              <van-tab :title="i.name" v-for="(i, index) in  storeData" :key="index">
                <FoodList :foodData=i.data :index=index />
              </van-tab>
              <van-tab :title="i.name" v-for="(i, index) in  commentsData" :key="index">
                <Comment :CommentData=i.data :index=index />
              </van-tab>
            </van-tabs>
          </div>
        </div>
      </div>
    </div>
    <van-action-bar>
      <van-action-bar-icon icon="cart-o" text="购物车" :badge="store.state.cartList.length" @click="toCart" />
      <van-action-bar-button type="warning" text="加入购物车" @click="AddCart" />
      <van-action-bar-button type="danger" text="立即购买" @click="clickBuy" />
    </van-action-bar>
  </div>
</template>

<script>
import { reactive, toRefs } from '@vue/reactivity'
import Myheader from '../../components/MyHeader.vue'
import FoodList from './commponents/FoodList.vue'
import Comment from './commponents/Comment.vue'
import { Toast } from 'vant'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
export default {
  components: {
    Myheader,
    Comment,
    FoodList
  },
  setup() {
    const router = useRouter()
    const store = useStore()
    const data = reactive({
      title: 'Canteen',
      // 食堂图片（最右）
      img: 'https://5b0988e595225.cdn.sohucs.com/images/20191206/1d819332644641c7800feef9eaa2eef5.jpeg',
      storeData: [
        {
          name: '菜品',
          data: {
            content: '点菜',
            items: [ // 后端
              {
                text: '热销套餐', // 从后端拉取餐厅信息摆放
                children: [ // 从后端拉取每个餐厅对应的菜品展示
                  {
                    pic: 'https://img1.baidu.com/it/u=1599947592,1695977044&fm=253&fmt=auto&app=138&f=JPEG?w=640&h=440',
                    title: '招牌酸菜鱼',
                    num: 0,
                    price: 25.0,
                    id: 0,
                    add: true
                  },
                  {
                    pic: 'https://img1.baidu.com/it/u=1599947592,1695977044&fm=253&fmt=auto&app=138&f=JPEG?w=640&h=440',
                    title: '藤椒酸菜鱼',
                    num: 0,
                    price: 25.0,
                    id: 1,
                    add: true
                  }
                ]
              },
              {
                text: '澳洲肥牛',
                children: [// 从后端拉取
                  {
                    pic: 'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fbkimg.cdn.bcebos.com%2Fpic%2F8694a4c27d1ed21b0ef4f3137f24cac451da80cb91b8&refer=http%3A%2F%2Fbkimg.cdn.bcebos.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1645407747&t=ea2c9f772ba0df3a2d1b00b962875460',
                    title: '酸汤肥牛',
                    num: 0,
                    price: 25.0,
                    id: 3,
                    add: true
                  },
                  {
                    pic: 'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fbkimg.cdn.bcebos.com%2Fpic%2F8694a4c27d1ed21b0ef4f3137f24cac451da80cb91b8&refer=http%3A%2F%2Fbkimg.cdn.bcebos.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1645407747&t=ea2c9f772ba0df3a2d1b00b962875460',
                    title: '香辣肥牛',
                    num: 0,
                    price: 25.0,
                    id: 4,
                    add: true
                  }
                ]
              },
              {
                text: '超级折扣',
                children: [// 从后端拉取
                  {
                    pic: 'https://img1.baidu.com/it/u=1599947592,1695977044&fm=253&fmt=auto&app=138&f=JPEG?w=640&h=440',
                    title: '无骨酸菜鱼+肥牛双拼',
                    num: 0,
                    price: 25.0,
                    id: 5,
                    add: true
                  },
                  {
                    pic: 'https://img1.baidu.com/it/u=1599947592,1695977044&fm=253&fmt=auto&app=138&f=JPEG?w=640&h=440',
                    title: '香辣水煮鱼+肥牛双拼',
                    num: 0,
                    price: 25.0,
                    id: 6,
                    add: true
                  }
                ]
              },
              {
                text: '玛卡巴卡',
                children: [// 从后端拉取
                  {
                    pic: 'https://img1.baidu.com/it/u=1599947592,1695977044&fm=253&fmt=auto&app=138&f=JPEG?w=640&h=440',
                    title: '无骨酸菜鱼+肥牛双拼',
                    num: 0,
                    price: 25.0,
                    id: 5,
                    add: true
                  },
                  {
                    pic: 'https://img1.baidu.com/it/u=1599947592,1695977044&fm=253&fmt=auto&app=138&f=JPEG?w=640&h=440',
                    title: '香辣水煮鱼+肥牛双拼',
                    num: 0,
                    price: 25.0,
                    id: 6,
                    add: true
                  }
                ]
              }
            ]
          }
        }],
      //                          餐厅的评价
      commentsData: [
        {
          name: '评价',
          data: {
            content: '评价' // 后端拉取过来进行展示
            /* items: [
              {
                id: 1,
                content: '这道菜做得很好！',
                replies: [
                  {
                    id: 2,
                    content: '阿里嘎多！',
                    targetId: 1
                  }
                ],
              },
              {
                id: 1,
                content: '这道菜做得很好！',
                replies: [
                  {
                    id: 2,
                    content: '阿里嘎多！',
                    targetId: 1
                  }
                ],
              },
              {
                id: 1,
                content: '这道菜做得很好！',
                replies: [
                  {
                    id: 2,
                    content: '阿里嘎多！',
                    targetId: 1
                  }
                ],
              },
              {
                id: 1,
                content: '这道菜做得很好！',
                replies: [
                  {
                    id: 2,
                    content: '阿里嘎多！',
                    targetId: 1
                  }
                ],
              }
            ] */
          }
        }
      ]
    })

    // 跳转到购物车
    const toCart = () => {
      router.push('./cart')
    }
    // 加入购物车
    const AddCart = (type) => {
      const newList = []
      data.storeData.forEach((item) => {
        item.data.items?.forEach((value) => { // 因为评价和商家没有开发，?作为兼容
          value.children.forEach((number) => {
            if (number.num > 0) {
              newList.push(number)
            }
          })
        })
      })
      if (newList.length === 0) {
        Toast('请添加商品')
        return
      }
      store.commit('ADDCART', newList)
      type === 'buy' ? toCart() : ''
    }

    // 点击立即购买
    const clickBuy = () => {
      AddCart('buy')
    }

    return {
      ...toRefs(data),
      AddCart,
      store,
      clickBuy,
      toCart
    }

  }
}
</script>

<style lang="less" scoped>
.mystore {
  .content {
    .main {
      height: 500px;
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
      background-color: lightsteelblue;
      width: 100%;
      height: 150px;
    }
  }
}
</style>
