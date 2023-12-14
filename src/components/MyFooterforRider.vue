<template>
  <div class="footer">
    <router-link to="/homeRider" class="item" active-class="nav_color">
      <van-icon name="label-o" size="30" />
      订单
    </router-link>
    <router-link to="/mineRider" class="item" active-class="nav_color">
      <van-icon name="user-o" size="30" />
      我的
    </router-link>
  </div>
</template>

<script>
export default {

}
</script>

<style lang="less" scoped>
.footer {
  display: flex;
  font-size: 12px;
  background: #fff;
  border-top: 0.5px solid #eee;

  .nav_color {
    color: #ffc400;
  }

  .item {
    display: flex;
    flex-flow: column;
    //flex-flow: row;
    flex: 1;
    align-items: center;
    justify-content: center;

  }
}
</style>
