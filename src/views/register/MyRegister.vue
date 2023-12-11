<template>
  <div class="register">
    <div class="content">
      <MyHeader title='Register' />

      <div>
        <div class="avatar-container">
          <van-uploader class="avatar-container" name="img" @oversize="() => { alert('图片过大') }" v-model="avatar"
            max-count="1" label="avatar" :after-read="saveContent" />
        </div>
        <van-form inset @submit="onSubmit">
          <van-field v-model="identity" label="身份" type="text" is-link readonly @click="showPicker = true" />

          <van-popup :show="showPicker" round position="bottom">
            <van-picker title="身份选择" :columns="identifierOptions" @confirm="changeRegister"
              @cancel="showPicker = false" />
          </van-popup>

          <van-field v-model="account" name="account" label="账号" type="text" placeholder="请输入工学号"
            :rules="[{ required: true, message: '请输入工学号' }]" />
          <van-field v-model="username" :name="nameFieldArray[0]" :label="nameFieldArray[1]" type="text"
            :placeholder="nameFieldArray[2]" :rules="[{ required: true, message: nameFieldArray[2] }]" />
          <van-field v-model="telephone" name="tele" label="电话" type="text" placeholder="请输入电话号码"
            :rules="[{ required: true, message: '请输入电话号码' }]" />
          <van-field v-model="password" name="password" label="密码" type="password" placeholder="请输入密码"
            :rules="[{ required: true, message: '请输入密码' }]" />
          <van-field v-model="passcheck" name="again" label="重复密码" type="password" placeholder="请再次输入密码"
            :rules="[{ required: true, message: '请再次输入密码' }]" />

          <van-field v-if="isCanteen" v-model="description" rows="1" autosize label="描述" type="textarea"
            placeholder="食堂描述" />
          <div style="margin:16px">
            <van-button type="primary" native-type="submit" size="large" round style="margin-bottom:10px">注册</van-button>
            <van-button type="primary" size="large" round @click="toLogin">返回</van-button>
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
    const account = ref()
    const username = ref()
    const telephone = ref()
    const password = ref()
    const passcheck = ref()
    const showPicker = ref(false)
    const identifierOptions = ['用户', '配送员', '食堂']
    const identity = ref('用户')
    const nameFieldArray = ref(['nick', '用户名', '请输入用户名'])
    const isCanteen = ref(false)
    const description = ref('')
    let avatarContent

    // 注册
    const register = () => {
      Toast('注册成功')
      // localStorage.setItem('userInfo', JSON.stringify(value))
      router.push('/login')
    }

    const saveContent = (param) => {
      // console.log(param.content)
      avatarContent = param.content
    }

    const currentInstance = getCurrentInstance()
    const { $axios } = currentInstance.appContext.config.globalProperties

    const changeRegister = (value, index) => {
      identity.value = value
      showPicker.value = false
      switch (index) {
        case 0:
          nameFieldArray.value = ['nick', '用户名', '请输入用户名']
          isCanteen.value = false
          break
        case 1:
          nameFieldArray.value = ['real_name', '配送员名', '请输入姓名']
          isCanteen.value = false
          break
        default:
          nameFieldArray.value = ['location', '地址', '请输入地址']
          isCanteen.value = true
          break
      }
    }

    // 注册
    const onSubmit = (value) => {
      // const that = this
      value.img = avatarContent === undefined ? '' : avatarContent
      $axios.request({
        url: '/buyerRegister',
        method: 'POST',
        data: value
      }).then((response) => {
        switch (response.data.status) {
          case 0:
            register()
            break
          case 1:
            Toast('电话已注册')
            break
          case 2:
            Toast('账号已存在')
            break
          case 3:
            Toast('密码不一致')
            break
          default:
            Toast('为止错误')
            break
        }
      })
    }

    // 登录
    const toLogin = () => {
      router.push('/login')
    }

    return {
      avatar,
      onSubmit,
      toLogin,
      account,
      username,
      telephone,
      passcheck,
      password,
      showPicker,
      identifierOptions,
      identity,
      nameFieldArray,
      isCanteen,
      description,
      saveContent,
      changeRegister
    }
  }
}
</script>

<style lang="less" scoped>
.register {
  .content {
    .avatar-container {
      text-align: center;
    }
  }
}
</style>
