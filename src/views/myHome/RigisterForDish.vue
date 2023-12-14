<template>
  <div class="registerForDish">
    <div class="content">
      <MyHeader title='添加菜品' />

      <div>
        <div class="avatar-container">
          <van-uploader class="avatar-container" name="img" @oversize="() => { alert('图片过大') }" v-model="avatar"
                        max-count="1" label="avatar" :after-read="saveContent" />
        </div>


        <!--后端添加菜品增加id，而展示菜品删除id-->


        <van-form inset @submit="onSubmit">
          <van-field v-model="DishName" :name="nameFieldArray[0]" :label="nameFieldArray[1]" type="text"
                     :placeholder="nameFieldArray[2]" :rules="[{ required: true, message: nameFieldArray[2] }]" />
          <van-field v-model="price" name="price" label="价格" type="text" placeholder="请输入售价"
                     :rules="[{ required: true, message: '请输入售价' }]" />
          <van-field v-model="description" name="description" rows="1" autosize label="菜品描述" type="textarea"
                     placeholder="请输入菜品介绍" />
          <div style="margin:16px">
            <van-button type="primary" native-type="submit" size="large" round style="margin-bottom:10px">添加</van-button>
            <van-button type="primary" size="large" round @click="backtoCanteen">返回</van-button>
          </div>
        </van-form>
      </div>

    </div>
  </div>
</template>

<script>
import { ref, getCurrentInstance } from 'vue'
import { useRouter } from 'vue-router'
import MyHeader from '../../components/MyHeader.vue'
import { Toast } from 'vant'
export default {
  components: { MyHeader },

  setup() {
    const router = useRouter()
    const avatar = ref()
    const DishName = ref()
    const price = ref()
    const password = ref()
    const nameFieldArray = ref(['name', '新菜品名字', '请输入新菜品名字'])
    const description = ref('')
    const tags = ref('')
    let avatarContent


    // 注册
    const register = () => {
      Toast('添加成功')
      // localStorage.setItem('userInfo', JSON.stringify(value))
      router.push('/homeCanteen')
    }

    const saveContent = (param) => {
      // console.log(param.content)
      avatarContent = param.content
    }

    const currentInstance = getCurrentInstance()
    const { $axios } = currentInstance.appContext.config.globalProperties

    // 注册
    const onSubmit = (value) => {
      // const that = this
      value.img = avatarContent === undefined ? '' : avatarContent
      value.tags=['好','辣']
      $axios.request({
        url: '/addDish',
        method: 'POST',
        data: value
      }).then((response) => {
        switch (response.data.status) {
          case 0:
            register()
            break
          default:
            Toast('未知错误')
            break
        }
      })
    }

    // 登录
    const backtoCanteen = () => {
      router.push('/homeCanteen')
    }

    return {
      avatar,
      onSubmit,
      backtoCanteen,
      DishName,
      price,
      password,
      nameFieldArray,
      description,
      tags,
      saveContent,
    }
  }
}
</script>

<style lang="less" scoped>
.registerForDish {
  .content {
    .avatar-container {
      text-align: center;
    }
  }
}
</style>
