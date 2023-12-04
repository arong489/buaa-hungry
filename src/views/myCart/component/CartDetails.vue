<template>
  <div class="cartDetails">
    <div class="content">
      <van-checkbox-group v-model="result" class="foodlist" @change="groupChange">
        <div v-for="(i, index) in store.state.cartList" :key="index">
          <van-checkbox :name="i.id" checked-color="#ffc400">
            <FoodAdd :item="i" :onChange="onChange" :showCheckbox="true" />
          </van-checkbox>
        </div>
      </van-checkbox-group>
    </div>
    <van-submit-bar :price="allPrice * 100" button-text="提交订单" @submit="onSubmit" class="submitall" v-if="isDelete">
      <van-checkbox v-model="checked" @click="choseall">全选</van-checkbox>
    </van-submit-bar>

    <div class="buy" v-else>
      <div class="left">
        <van-checkbox v-model="checked" @click="choseall">全选</van-checkbox>
      </div>
      <div class="delect" @click="deleteClick">删除</div>
    </div>


  </div>
</template>

<script>
import { reactive, toRefs } from '@vue/reactivity';
import { useStore } from 'vuex'
import FoodAdd from '../../../components/FoodAdd.vue'
import { computed, onMounted } from '@vue/runtime-core';
import { useRouter } from 'vue-router';
import { Toast } from 'vant';
import emitter from '../../../common/js/eventbus'
export default {
  components: { FoodAdd },
  props: ['changeShow'],
  setup(props) {
    const router = useRouter();
    const store = useStore();

    let data = reactive({
      result: [], //选中的数据
      checked: true, //全选
      isDelete: true
    })

    //初始化默认值
    const init = () => {
      data.result = store.state.cartList.map((i) => { return i.id })
    }

    onMounted(() => {
      init()
    })


    //改变步进器的数量      判断商品的id是否于数据中的id一致，是则将步进器中的真实数据存入num中
    const onChange = (value, detail) => {
      store.state.cartList.map((item) => {
        if (item.id === detail.name) {
          item.num = value;
        }
      })
    }

    //更新数据      将包含的数据返回出来，传到下一个页面
    const updata = (type) => {
      return store.state.cartList.filter((item) => {
        return type === 2 ? data.result.includes(item.id) : !data.result.includes(item.id)
      })
    }

    //结算功能
    const onSubmit = () => {
      if (data.result.length !== 0) {
        store.commit('PAY', updata(2))
        router.push({
          path: './ordercreate',
          query: {
            list: data.result
          }
        })
      } else {
        Toast.fail('请选择下单的商品')
      }

    }

    //选择全部或者取消全部
    const choseall = () => {
      if (data.result.length !== store.state.cartList.length) {
        init()
      } else {
        data.result = [];
      }
    }

    //复选框触发事件
    const groupChange = (i) => {        //返回的是一个proxy的对象，左面是下标，右面是菜名的id
      console.log(i)
      if (i.length === store.state.cartList.length) {
        data.checked = true
      } else {
        data.checked = false
      }
      data.result = i;
    }

    //计算订单总的金额
    const allPrice = computed(() => {
      let contList = updata(2)
      // let contList=store.state.cartList.filter((item)=>{
      //    return data.result.includes(item.id)
      // })
      let sum = 0;
      contList.forEach((value) => {
        sum += value.price * value.num
      })
      return sum
    })

    //监听事件
    emitter.on('edit', () => {
      data.isDelete = !data.isDelete
    })

    //删除按钮
    const deleteClick = () => {
      if (data.result.length) {
        //更新删除后的购物车数据
        store.commit('DELETE', updata(1))

        //删除后的选中 删除选中的     设置为空的原因是因为复选框选择不到name值，使数据保留下来
        data.result = []

        //购物车无数据时
        if (store.state.cartList.length === 0) {
          store.commit('EDIT', 'delete')
          props.changeShow();                 //cart传过来的无数据的页面方法
        }
      } else {
        Toast.fail('请选择需要删除的商品');
      }
    }

    return {
      store,
      ...toRefs(data),
      onChange,
      choseall,
      groupChange,
      allPrice,
      onSubmit,
      deleteClick
    }
  }
}
</script>

<style lang="less" scoped>
.cartDetails {
  display: flex;

  .submitall {
    position: fixed;
    bottom: 46px;
  }

  .buy {
    width: 100%;
    height: 50px;
    position: fixed;
    bottom: 46px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: white;

    .left {
      margin-left: 20px;
    }

    .delect {
      width: 110px;
      height: 40px;
      line-height: 40px;
      text-align: center;
      margin-right: 20px;
      background: red;
      border-radius: 20px;
      color: white;
    }
  }

}</style>
