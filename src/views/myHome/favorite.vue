
<template>
  <div id="app">
    <!--<Favorites />-->
    <!--从后端拉取个人收藏菜品进行展示-->
    <van-card
      title="name of dish"
      desc="description"
      price="price"
      thumb="https://fastly.jsdelivr.net/npm/@vant/assets/ipad.jpeg"
    >
      <!--thumb放入传来的img-->
    </van-card>

  </div>
</template>



<script>
//import Favorites from "../../components/Favorites.vue";
import { createApp } from 'vue';
import { Card } from 'vant';

const app = createApp();
app.use(Card);

export default {
  /*components: {
    Favorites,
  },*/
};
</script>
