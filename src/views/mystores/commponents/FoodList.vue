<template>
  <div class="foot_list" v-if="index === 0">
    <van-tree-select :main-active-index="activeIndex" height="55vw" :items="items" @click-nav="navClick">
      <template #content>
        <div v-for="(i, index) in subItem" :key="index">
          <FoodAdd :item="i" showadd=true :showsteer=showsteer :onChange=onChange />
        </div>
      </template>
    </van-tree-select>
  </div>
  <div v-else>{{ foodData.content }}</div>
</template>

<script>
import { reactive, toRefs } from '@vue/reactivity'
import FoodAdd from '../../../components/FoodAdd.vue'
export default {
  components: {
    FoodAdd
  },
  props: ['foodData', 'index'],
  setup(props) {
    const data = reactive({
      items: [],
      activeIndex: 0,
      subItem: []
    })

    const init = () => {
      const newList = []
      console.log(props.foodData.items)
      props.foodData?.items?.map((i, index) => {
        newList.push({ text: i.text }) // 左侧标题
        data.items = newList
        if (data.activeIndex === index) {
          data.subItem = i.children
        }
      })
    }
    init()

    // 点击左侧导航
    const navClick = (i) => {
      // console.log(i)
      data.activeIndex = i
      init()
    }

    // 切换步进器
    const showsteer = (i) => {
      data.subItem.forEach(item => {
        if (item.id === i) {
          item.add = false
          item.num += 1
        }
      })
    }

    // 步进器增加触发事件
    const onChange = (value, detail) => { // detail是取得步进器中name中的数据
      data.subItem.forEach(item => {
        if (item.id === detail.name) {
          item.num = value // value是真实的数据
        }
        console.log(data.subItem)
      })
    }

    return {
      ...toRefs(data),
      navClick,
      showsteer,
      onChange
    }
  }
}
</script>

<style></style>
