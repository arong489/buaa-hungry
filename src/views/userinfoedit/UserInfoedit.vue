<template>
  <div class="useredit">
    <div class="content">
      <MyHeader title="账号管理" />
      <div style="height: 10vh;"></div>
      <van-field v-model="pwdOld" type="password" label="旧密码" />
      <van-field v-model="pwdNew" type="password" label="新密码" />
      <van-field v-model="pwdAgain" type="password" label="重复新密码" />
      <div style="margin-top:16px">
        <van-button type="primary" size="large" round @click="submit" style="margin-bottom:10px">保存</van-button>
        <van-button type="primary" size="large" round @click="loginout">退出登录</van-button>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, toRefs } from '@vue/reactivity'
import MyHeader from '../../components/MyHeader.vue'
import { useRouter } from 'vue-router'
import { Toast } from 'vant'
import axios from '../../api/api'
export default {
  components: { MyHeader },
  setup() {
    const router = useRouter()
    const data = reactive({
      pwdOld: '',
      pwdNew: '',
      pwdAgain: ''
    })

    // 保存
    const submit = () => {
      if (data.pwdOld && data.pwdAgain && data.pwdNew) {
        axios.put('/resetPassword', {
          old: data.pwdOld,
          new: data.pwdNew,
          again: data.pwdAgain
        }).then((response) => {
          switch (response.data.status) {
            case 0:
              Toast.success('密码修改成功')
              break
            case 1:
              Toast.fail('原密码错误')
              break
            case 2:
              Toast.fail('两次输入新密码不一致')
              break
            default:
              break
          }
        })
      } else {
        Toast('请输入你修改的值')
      }
    }

    // 退出登录
    const loginout = () => {
      localStorage.removeItem('isLogin')
      localStorage.removeItem('token')
      Toast('退出登录')
      router.push('/login')
    }

    return {
      ...toRefs(data),
      loginout,
      submit
    }
  }
}
</script>

<style lang="scss" scoped></style>
