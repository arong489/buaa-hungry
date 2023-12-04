<template>
  <div class="header">
      <van-icon name="arrow-left" class="icon" @click="back" />
      <div> {{title}} </div>
      <div class="edit" v-if="edit" @click="editClick">{{store.state.edit?"编辑":"完成"}}</div>
  </div>
</template>

<script>
import { Toast } from 'vant';
import {useRouter} from 'vue-router'
import emitter from  '../common/js/eventbus'
import {useStore} from 'vuex'
export default {
    props:['title','edit'],
    setup(){
        const router=useRouter();
        const store=useStore();
        const back=()=>{
            router.back();
        }


        //编辑按钮
        const editClick=()=>{
            if(store.state.cartList.length){
                store.commit('EDIT')
                emitter.emit('edit')
            }else{
                Toast.fail('还没买东西呢！')
            }
        }

        return{
            back,
            editClick,
            store
        }
    }

}
</script>

<style lang="less" scoped>
.header{
     display: flex;
     justify-content: center;
    align-items: center;
    height: 40px;
    line-height: 40px;
    font-size: 20px;
    font-weight: bold;
    .icon{
        position: absolute;
        left:5px;
    }
    .edit{
        position:fixed;
        right: 8px;
    }
}
</style>
