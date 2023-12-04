<template>
  <div class="mycart">
    <div class="content">
      <MyHeader title="购物车" :edit="true" />
      <CartDetails v-if="isShow" :changeShow="changeShow" />
      <MyBack v-else />
    </div>
    <MyFooter />
  </div>
</template>

<script>
import MyFooter from '../../components/MyFooter.vue'
import MyHeader from '../../components/MyHeader.vue'
import MyBack from '../../components/MyBack.vue'
import CartDetails from './component/CartDetails.vue'
import { onMounted, ref } from 'vue'
import { useStore } from 'vuex'

export default {
  components: {
    MyFooter,
    MyHeader,
    MyBack,
    CartDetails
  },
  setup() {
    const store = useStore();
    const isShow = ref(true)

    //初始化页面
    const init = () => {
      if (store.state.cartList.length === 0) {
        isShow.value = false;
      }
    }

    onMounted(() => {
      init()
    })

    const changeShow = () => {
      isShow.value = false
    }


    return {
      init,
      isShow,
      changeShow
    }
  }
}
</script>

<style lang="less" scoped>
.mycart {
  height: 100%;
  display: flex;
  flex-flow: column;

  .content {
    flex: 1;
    overflow-y: auto;
  }
}
</style>
