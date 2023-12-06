<!--
<button id="add-btn">添加收藏</button>
<ul id="list"></ul>


<script>
const addBtn = document.getElementById('add-btn');
const list = document.getElementById('list');

// 获取本地存储的收藏列表
const getFavorites = () => {
  const favorites = localStorage.getItem('favorites');
  return favorites ? JSON.parse(favorites) : [];
}

// 渲染收藏列表
const renderFavorites = () => {
  const favorites = getFavorites();
  list.innerHTML = '';
  favorites.forEach(favorite => {
    const li = document.createElement('li');
    li.textContent = favorite;
    list.appendChild(li);
  });
}

// 添加收藏
addBtn.addEventListener('click', () => {
  const favorite = prompt('请输入收藏内容：');
  if (favorite) {
    const favorites = getFavorites();
    favorites.push(favorite);
    localStorage.setItem('favorites', JSON.stringify(favorites));
    renderFavorites();
  }
});

// 页面加载时渲染收藏列表
renderFavorites();
</script>
-->
<!--<template>
  <div class="myfavorite">
    <div class="content">
      <MyHeader title="我的收藏" :edit="true" />
      <CartDetails v-if="isShow" :changeShow="changeShow" />

      <MyBack v-else />
    </div>
    <MyFooter />
  </div>
</template>

<script>
import MyHeader from '../../components/MyHeader.vue'
import MyBack from '../../components/MyBack.vue'
import FavoriteDetails from '../../views/myHome/components/FavoriteDetails.vue'
import { onMounted, ref } from 'vue'
import { useStore } from 'vuex'

export default {
  components: {
    MyHeader,
    MyBack,
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
.myfavorite {
  height: 100%;
  display: flex;
  flex-flow: column;

  .content {
    flex: 1;
    overflow-y: auto;
  }
}
</style>-->
<template>
  <div id="app">
    <Favorites />
  </div>
</template>

<script>
import Favorites from "../../components/Favorites.vue";

export default {
  components: {
    Favorites,
  },
};
</script>
