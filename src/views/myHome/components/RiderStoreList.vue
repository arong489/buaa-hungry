<template>
  <div class="storeItem" @click="toStore">
    <img :src="item.pic" >
    <div class="item_right">
      <div class="title">{{item.title}}</div>
      <div class="sales">{{item.sales}}</div>
      <div class="price">配送费￥{{item.price}}免配送费</div>
      <div class="label">
        <div v-for="(i,index) in item.label" :key="index">
          {{i}}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
export default {
  props: ['item'],
  setup () {
    const router = useRouter()
    const toStore = () => {
      router.push('./store-rider')
    }

    return {
      toStore
    }
  }
}
</script>

<style lang="less" scoped>
.storeItem{
  display: flex;
  padding: 20px;
  background: white;
  border-radius: 20px;
  margin-top: 20px;
  .item_right{
    display: flex;
    flex-flow: column;
    justify-content: space-around;
    .title{
      font-weight: bold;
      font-size: 16px;
    }
    .label{
      display: flex;
      div{
        margin-right: 10px;
        background-color: #ffc400;
        border-radius: 5px;
      }
    }

  }
  img{
    width: 150px;
    height: 150px;
    margin-right: 20px;
    border-radius: 10px;
  }

}
</style>
