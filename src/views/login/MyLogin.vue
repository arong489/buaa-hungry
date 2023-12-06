<template>
  <div class="login">
    <div class="content">
      <MyHeader title="Login In" />
      <div>
        <van-form @submit="onSubmit">
          <van-cell-group inset>
            <van-field v-model="account" name="account" label="账号" placeholder="账号"
              :rules="[{ required: true, message: '请填写账号' }]" />
            <van-field name="identity" v-model="identityStr" label="身份" placeholder="身份" is-link readonly
              @click="showPicker = true" />

            <van-popup round position="bottom" :show="showPicker">
              <van-picker title="选择身份" :columns="identifierOptions"
                @confirm="(value, index) => { identity = index; identityStr = value; showPicker = false }"
                @cancel="showPicker = false" />
            </van-popup>

            <van-field v-model="password" type="password" name="password" label="密码" placeholder="密码"
              :rules="[{ required: true, message: '请填写密码' }]" />
          </van-cell-group>
          <div style="margin: 66px;">
            <van-button block type="primary" native-type="submit">
              登录
            </van-button>
            <van-button block type="primary" @click="toRegister" style="margin-top:20px">
              注册
            </van-button>
          </div>
        </van-form>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, toRefs, getCurrentInstance } from 'vue'
import MyHeader from '../../components/MyHeader.vue'
import { useRouter } from 'vue-router'
import { Toast } from 'vant'
export default {
  components: { MyHeader },
  setup() {
    const router = useRouter()
    const data = reactive({
      account: '',
      identity: 0,
      identityStr: '用户',
      password: '',
      showPicker: false,
      identifierOptions: ['用户', '配送员', '食堂']
    })

    const currentInstance = getCurrentInstance()
    const { $axios } = currentInstance.appContext.config.globalProperties
    const identities = ['buyer', 'staff', 'canteen']

    const onSubmit = (value) => {
      $axios.request({
        url: '/login',
        method: 'post',
        data: {
          account: value.account,
          identity: identities[data.identity],
          password: value.password
        }
      }).then((response) => {
        switch (response.data.status) {
          case 0:
            Toast('登录成功')
            localStorage.setItem('isLogin', 1)
            localStorage.setItem('identity', data.identity)
            localStorage.setItem('token', response.data.token)
            data.identity === 0
              ? router.push('/home')
              : data.identity === 2
                ? router.push('/homeCanteen')
                : router.push('/homeRider')
            break
          case 1:
            Toast('未注册')
            break
          case 2:
            Toast('密码错误')
            break
          case 3:
            Toast('身份错误')
            break
          default:
            Toast('未知错误')
            break
        }
      })
    }

    // 注册
    const toRegister = () => {
      router.push('/register')
    }

    return {
      ...toRefs(data),
      onSubmit,
      toRegister
    }
  }
}
</script>

<style lang="less" scoped>
.login {
  .content {
    .img {
      width: 400px;
      height: 200px;
      background-color: #3399ff;
      font-size: 100px;
      line-height: 200px;
      text-align: center;
      border-radius: 40px;
      margin: 20px auto;
    }
  }
}
</style>
