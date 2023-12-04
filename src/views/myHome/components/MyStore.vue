<template>
  <div class="store_list">
      <div v-for="(i,index) in store_list" :key="index">
          <StoreList :item='i' />
      </div>
  </div>
</template>

<script>
import StoreList from './StoreList.vue'
export default {
  components: {
    StoreList
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
