<template>
  <div class="store_list">
    <div v-for="(i,index) in store_list" :key="index">
      <RiderStoreList :item='i' />
    </div>
  </div>
</template>

<script>
import RiderStoreList from './RiderStoreList.vue'
export default {
  components: {
    RiderStoreList
  },
  props: ['store_list']

}
</script>

<style lang="less" scoped>
.store_list{
  background: whitesmoke;
  padding: 10px;
}
</style>
