<template>
  <div style="text-align:center;margin-top: 5vh;"><van-image height="200" width="200" fit="contain"
      :src="modifiedDish.img" @click="changeDishImg" /></div>
  <van-uploader ref="dishImgUploader" max-count="1" v-show="false" v-model="avatarFile" :preview-image="false"
    :after-read="saveImg" @oversize="() => { alert('图片过大') }" />

  <van-form inset @submit="onSubmit">
    <van-field v-model="modifiedDish.name" type="text" placeholder="请输入菜品名"
      :rules="[{ required: true, message: '请输入菜品名' }]" label="菜品名" />
    <van-field v-model="modifiedDish.price" type="number" placeholder="请输入价格"
      :rules="[{ required: true, message: '请输入价格' }]" label="价格" />
    <van-field v-model="modifiedDish.description" rows="1" autosize type="textarea" placeholder="请输入菜品介绍" label="介绍" />
    <div style="margin:16px">
      <van-button type="primary" native-type="submit" size="large" round style="margin-bottom:10px">修改</van-button>
      <van-button type="primary" size="large" round @click="back">返回</van-button>
    </div>
  </van-form>
</template>

<script>
import axios from '../../../api/api'
import { Toast } from 'vant'
import { reactive, ref, toRefs } from 'vue'

export default {
  props: ['dish'],
  emits: ['dishModify', 'back'],
  setup(props, ctx) {
    const data = reactive({
      avatarFile: [],
      modifiedDish: props.dish
    })

    const dishImgUploader = ref(null)

    function changeDishImg() {
      dishImgUploader.value.chooseFile()
    }

    function saveImg() {
      data.modifiedDish.img = data.avatarFile[0].content
      data.avatarFile = []
    }

    function onSubmit() {
      axios.put('/changeDish', data.modifiedDish).then((response) => {
        switch (response.data.status) {
          case 0:
            Toast.success('修改成功')
            ctx.emit('dishModify', data.modifiedDish)
            break
          case -2:
            break
          case -1:
            break
          case -3:
            break
          default:
            Toast.fail('未知错误')
            break
        }
      })
    }

    function back() {
      ctx.emit('back')
    }

    return ({
      ...toRefs(data),
      changeDishImg,
      saveImg,
      onSubmit,
      back,
      dishImgUploader
    })
  }
}
</script>
