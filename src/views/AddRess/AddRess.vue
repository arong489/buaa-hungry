<template>
    <div class="address">
        <div class="content">
            <MyHeader title="地址编辑"/>
            <van-address-list
                v-model="chosenAddressId"
                :list="list"
                default-tag-text="默认"
                @add="onAdd"
                @edit="onEdit"
            />

        </div>
    </div>
</template>

<script>
import { Toast } from 'vant';
import {onMounted, reactive, ref, toRefs} from 'vue'
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import MyHeader from '@/components/MyHeader.vue';
export default {
  components: { MyHeader },
    setup() {
    const store=useStore();
    const router=useRouter();
    const chosenAddressId = ref('1');
    const data=reactive({
        list:[]
    })

    //用户初始化
    const init=()=>{
        data.list=store.state.userAddress.map((item)=>{
            return{
                id: item.id,
                name: item.name,
                tel: item.tel,
                address: `${item.school}${item.dorm}${item.addressDetail}`,
                isDefault:!!item.isDefault,
            }
        })
    }

    onMounted(()=>{
        init()
    })

    const onAdd = () => {
        router.push({
            path:'/addressedit',
            query:{
                type:'add'
            }
        })
    };

    //编辑按钮
    const onEdit = (item) => {
        router.push({
            path:'/addressedit',
            query:{
                id:item.id,
                type:'change'
            }
        })
    };

    return {
      ...toRefs(data),
      onAdd,
      onEdit,
      chosenAddressId,
    };
  },
}
</script>

<style lang="scss" scoped>

</style>
