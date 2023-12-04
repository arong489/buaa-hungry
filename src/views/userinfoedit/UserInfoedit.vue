<template>
  <div class="useredit">
    <div class="content">
      <MyHeader title="个人信息管理" />
      <van-field v-model="nickname" type="text" label="昵称" />
      <van-field v-model="pwd" type="password" label="修改密码" />
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
export default {
  components: { MyHeader },
  setup() {
    const router = useRouter();
    let data = reactive({
      nickname: '',
      pwd: ''
    })

    //保存
    const submit = () => {
      if (data.nickname && data.pwd) {
        let userInfo = JSON.parse(localStorage.userInfo);
        let newInfo = {
          用户名: data.nickname || userInfo['用户名'],
          密码: data.pwd || userInfo['密码']
        }
        localStorage.setItem('userInfo', JSON.stringify(newInfo))
        Toast('修改成功')
        router.push('/mine')
      } else {
        Toast('请输入你修改的值')
      }
    }

    //退出登录
    const loginout = () => {
      localStorage.removeItem('isLogin')
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
