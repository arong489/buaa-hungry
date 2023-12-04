<template>
  <div class="login">
    <div class="content">
      <MyHeader title="Login In" />
      <div class="img">Takeout</div>
      <div>
        <van-form @submit="onSubmit">
          <van-cell-group inset>
            <van-field v-model="username" name="用户名" label="用户名" placeholder="用户名"
              :rules="[{ required: true, message: '请填写用户名' }]" />
            <van-field v-model="identity" name="身份" label="身份" placeholder="学生-1\外卖员-2\食堂-3"
              :rules="[{ required: true, message: '请填写身份（学生、外卖员、食堂）' }]" />
            <van-field v-model="password" type="password" name="密码" label="密码" placeholder="密码"
              :rules="[{ required: true, message: '请填写密码' }]" />
          </van-cell-group>
          <div style="margin: 66px;">
            <van-button block type="primary" native-type="submit">
              登录
            </van-button>
            <van-button block type="primary" native-type="submit" @click="toRegister" style="margin-top:20px">
              注册
            </van-button>
          </div>
        </van-form>

      </div>
    </div>
  </div>
</template>

<script>
import { reactive, toRefs } from 'vue'
import MyHeader from '../../components/MyHeader.vue'
import { useRouter } from 'vue-router'
import { Toast } from 'vant'
export default {
  components: { MyHeader },
  setup () {
    const router = useRouter()
    const data = reactive({
      username: 'abaaba',
      identity: '1',
      password: '123456'
    })

    // //登录，此处为无条件登录进入主页
    // const onSubmit = (value) => {
    //   Toast('登录成功')
    //   localStorage.setItem('isLogin', 1);
    //   router.push('/home');
    // }
    const onSubmit = (value) => {
      if (!localStorage.userInfo) {
        Toast('账号没有注册')
      } else {
        const userInfo = JSON.parse(localStorage.userInfo)
        if (userInfo['用户名'] === value['用户名']) {
          if (userInfo['密码'] === value['密码']) {
            Toast('登录成功')
            localStorage.setItem('isLogin', 1)
            router.push('/home')
          } else {
            Toast('密码错误')
          }
        } else {
          Toast('账号错误')
        }
      }
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
