<template>
  <div class="favorites">
    <h1>我的收藏</h1>
    <ul>
      <li v-for="(item, index) in favorites" :key="index">{{ item }}</li>
    </ul>
    <input type="text" v-model="newItem" @keyup.enter="addFavorite" placeholder="输入收藏内容" />
    <button @click="addFavorite">添加</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      favorites: [],
      newItem: "",
    };
  },
  methods: {
    addFavorite() {
      if (this.newItem.trim() !== "") {
        this.favorites.push(this.newItem);
        this.newItem = "";
      }
    },
  },
};
</script>

<style scoped>
.favorites {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  margin-bottom: 30px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  padding: 10px;
  border-bottom: 1px solid #eee;
}

li:last-child {
  border-bottom: none;
}

button{
  background-color:dodgerblue;
  color:white;
  width: 100px;
  height: 35px;
  border:0;
  font-size: 20px;
  border-radius: 30px;
}
button:hover{
  background-color: #00cc66;
}

</style>
