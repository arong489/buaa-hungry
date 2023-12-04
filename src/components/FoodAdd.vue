<template>
  <div class="foodadd">
    <div class="content_item">
      <!-- <van-checkbox :name="item.id" v-if="showCheckbox" checked-color="#ffc400"></van-checkbox> -->
      <div class="list">
        <img src="../assets/11.jpg" alt="">
        <div class="text">
          <div class="title">{{ item.title }}</div>
          <van-icon name="add" v-if="showadd && item.add" @click="showsteer(item.id)" />
          <van-stepper v-model="item.num" v-else :name="item.id" :min='1' @change="onChange" />
        </div>
      </div>
      <div class="price">{{ item.price }}</div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['item', 'showadd', 'showsteer', 'onChange', 'showCheckbox']

}
</script>

<style lang="less" scoped>
.foodadd {

  .content_item {
    display: flex;
    justify-content: space-between;
    padding: 5px;

    .list {
      display: flex;

      img {
        width: 70px;
        margin-right: 20px;
      }

      .text {
        .title {}
      }
    }

    .price {
      margin-right: 10px;
    }
  }
}
</style>
