<template>
    <div>
         <MyHeader :title="address"/>
        <van-address-edit
            :area-list="areaList"
            :address-info="addressInfo"
            show-delete
            show-set-default
            :area-columns-placeholder="['请选择', '请选择']"
            @save="onSave"
            @delete="onDelete"
        />

    </div>
</template>

<script>
import MyHeader from '../..//components/MyHeader.vue';
import { computed, onMounted, reactive, ref, toRefs } from 'vue';
import { Toast } from 'vant';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';
export default {
    components:{
        MyHeader
    },
  setup() {
      const store=useStore();
      const route=useRoute();
      const router=useRouter();
      const data=reactive({
        areaList:{
                province_list: {
                110000: "沙河校区",
                120000: "学院路校区",
                },
                city_list: {
                110100: "沙河公寓群",
                120100: "大运村学生公寓群",
                120200: "校内公寓群",
                120300: "新北公寓群"
                },
                county_list: {
                110101: "一号楼",
                110102: "二号楼",
                110103: "三号楼",
                110104: "四号楼",
                110105: "五号楼",

                120101: "一号楼",
                120102: "二号楼",
                120103: "三号楼",
                120104: "四号楼",
                120105: "五号楼",

                120201: "一公寓",
                120202: "二公寓",
                120203: "三公寓",
                120204: "四公寓",
                120205: "五公寓",

                120301: "11公寓",
                120302: "12公寓",
                120303: "13公寓",
                120304: "14公寓",
                120305: "15公寓",
                },
            },
            addressInfo:{},
      })

      const address=computed(()=>{
          return route.query.type==='change'?'地址编辑':'添加地址'
      })

      //数据初始化
      const init=()=>{
          store.state.userAddress.forEach((item)=>{
              if(item.id===Number(route.query.id)){
                  data.addressInfo=item
              }
          })
      }

      onMounted(()=>{
          init()
      })


        //保存按钮
        const onSave=(content)=>{
            if(route.query.type==='add'){
                store.commit('ADDADDRESS',content)
            }else{
                store.commit('CHANGEADDRESS',content)
            }
            Toast.fail('保存成功')

            router.back();
        }

        //删除按钮
        const onDelete=(content)=>{
            store.commit('DELECTADDRESS',content)
            Toast.fail('删除成功')
            router.back();
        }



    return {
        ...toRefs(data),
      address,
      onSave,
      onDelete
    };
  },
};
</script>

<style lang="scss" scoped>

</style>
