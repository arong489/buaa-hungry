<template>
  <div class="mine rider">
    <MyHeader title="我的" />
    <div class="content">
      <div class="user-info">
        <div class="info">
          <img :src="avatar.length > 0 ? avatar : '../../assets/user.svg'" @click="changeAvatar" />
          <van-uploader ref="uploader" max-count="1" v-show="false" v-model="avatarFile" :preview-image="false"
            :after-read="saveContent" @oversize="() => { alert('图片过大') }" />
          <div class="user-desc">
            <span>
              <h2>{{ name }}</h2>
            </span>
          </div>
        </div>
      </div>
      <ul class="user-list">
        <li class="van-hairline--bottom" @click="togo('./homeRider')">
          <span>订单管理</span>
          <van-icon name="arrow" />
        </li>
        <li class="van-hairline--bottom" @click="togo('./userinfoedit')">
          <span>账号管理</span>
          <van-icon name="arrow" />
        </li>
      </ul>
    </div>
    <MyFooterforRider />
  </div>
</template>

<script>
import { reactive, toRefs } from '@vue/reactivity'
import MyFooterforRider from '../../components/MyFooterforRider.vue'
import MyHeader from '../../components/MyHeader.vue'
import { useRouter } from 'vue-router'
import axios from '../../api/api'
import { onMounted, ref } from 'vue'
import { Toast } from 'vant'
export default {
  components: {
    MyFooterforRider,
    MyHeader
  },
  setup() {
    const router = useRouter()
    const data = reactive({
      name: '',
      avatar: '',
      avatarFile: []
    })

    const uploader = ref(null)

    const togo = (path) => {
      router.push(path)
    }

    function changeAvatar() {
      uploader.value.chooseFile()
    }

    function saveContent() {
      axios.put('/resetPic', {
        img: data.avatarFile[0].content
      }).then((response) => {
        if (response.data.status !== 0) {
          Toast.fail('头像修改失败')
          data.avatarFile = []
        } else {
          data.avatar = data.avatarFile[0].content
          data.avatarFile = []
        }
      })
    }

    onMounted(() => {
      axios.get('/getStaffInfo').then((response) => {
        data.name = response.data.real_name
        data.avatar = response.data.img
      })
    })

    return {
      ...toRefs(data),
      togo,
      changeAvatar,
      uploader,
      saveContent
    }
  }
}
</script>

<style lang='less' scoped>
.mine {
  height: 100%;
  display: flex;
  flex-flow: column;

  .content {
    flex: 1;
    overflow-y: auto;

    .user-info {
      width: 94%;
      margin: 10px;
      height: 115px;
      background: linear-gradient(90deg, #3399ff, #33cc33);
      box-shadow: 0 2px 5px #003300;
      border-radius: 6px;

      .info {
        position: relative;
        display: flex;
        width: 100%;
        height: 100%;
        padding: 25px 20px;
        box-sizing: border-box;

        img {
          border-radius: 50%;
          // margin-top: 4px;
          aspect-ratio: 1;
        }

        .user-desc {
          display: flex;
          flex-direction: column;
          margin-left: 10px;
          line-height: 20px;
          font-size: 14px;
          color: #fff;
          justify-content: space-between;

          span {
            color: #fff;
            font-size: 14px;
            padding: 2px 0;
          }
        }

        .account-setting {
          position: absolute;
          top: 10px;
          right: 20px;
          font-size: 13px;
          color: #fff;

          .van-icon-setting-o {
            font-size: 16px;
            vertical-align: -3px;
            margin-right: 4px;
          }
        }
      }
    }

    .user-list {
      padding: 0 20px;
      margin-top: 20px;
      background-color: #fff;

      li {
        height: 80px;
        line-height: 40px;
        display: flex;
        justify-content: space-between;
        font-size: 14px;

        .van-icon-arrow {
          margin-top: 13px;
        }
      }
    }
  }
}
</style>
