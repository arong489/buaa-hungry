<template>
  <van-tree-select :main-active-index="activeIndex" :items="items" @click-nav="navClick" height="calc(100vh - 214px)">

    <template #content>
      <van-field v-if="addCommentEnable" v-model="newComment" rows="1" autosize type="textarea" placeholder="点我输入评论">
        <template #button>
          <van-button type="primary" v-show="newComment.length > 0" @click="inputFocus">发表</van-button>
        </template>
      </van-field>
      <div v-if="comments.length > 0">
        <van-card v-for="comment of comments" :key="`comment${comment.comment_id}`"
          style="border-radius: 15px; margin:10px ;box-shadow: 5px 5px 5px #8e8d8d;" @click="showCommentDetail(comment)">
          <template #thumb>
            <img :src="comment.img" alt="头像缺失" style="aspect-ratio: 1; width: 50px; border-radius: 50%">
          </template>
          <template #title><strong style="font-size: 2.5ch">{{ comment.nick_name }}</strong><br></template>
          <template #desc>
            {{ comment.create_time }}
          </template>
          <template #bottom>
            {{ comment.content }}
          </template>
        </van-card>
      </div>
      <van-empty v-else description="暂无评论" />
      <van-popup v-model:show="showDetail" round position="bottom" :close-on-click-overlay='false'
        @click-overlay="showDetail = false" :closeable="true" style="height: 100%;">
        <commentDetail :fatherComment="commentSelect" />
      </van-popup>
    </template>
  </van-tree-select>
</template>

<script>

import { watch, onMounted, reactive, toRefs } from 'vue'
import axios from '@/api/api'
import { Toast } from 'vant'
import commentDetail from '@/components/commentDetail.vue'

export default {
  components: { commentDetail },
  emits: ['selectCanteen'],
  props: ['canteensInf', 'activeIndex'],
  setup(props, ctx) {
    const data = reactive({
      commentSelect: {},
      items: props.canteensInf.map((canteenInf) => ({ text: canteenInf.location })), // ??????????????????????
      activeIndex: 0,
      comments: [],
      newComment: '',
      showDetail: false,
      addCommentEnable: localStorage.getItem('identity') === '0'
    })

    const navClick = (i) => {
      axios.post('/getCanteenComments', {
        canteen_id: props.canteensInf[i].id
      }).then((response) => {
        switch (response.data.status) {
          case 0:
            data.comments = response.data.comments
            data.activeIndex = i
            ctx.emit('selectCanteen', i)
            break
          default:
            Toast.fail('未知错误')
            break
        }
      }).catch((error) => {
        Toast.fail('请求异常')
        console.log(error)
      })
    }

    onMounted(async () => {
      data.activeIndex = props.activeIndex
      refresh()
      console.log('mount food list')
    })

    watch(() => props.activeIndex, (index, oldIndex) => {
      if (index !== data.activeIndex) {
        axios.post('/getCanteenComments', {
          canteen_id: props.canteensInf[index].id
        }).then((response) => {
          switch (response.data.status) {
            case 0:
              data.comments = response.data.comments
              data.activeIndex = index
              break
            default:
              Toast.fail('未知错误')
              break
          }
        }).catch((error) => {
          Toast.fail('请求异常')
          console.log(error)
        })
      }
    })

    const inputFocus = () => {
      axios.request({
        url: '/commentOnCanteen',
        method: 'post',
        data: {
          canteen_id: props.canteensInf[data.activeIndex].id,
          content: data.newComment
        }
      }).then((response) => {
        switch (response.data.status) {
          case 0:
            Toast.success('评论成功')
            refresh()
            data.newComment = ''
            break
          default:
            Toast.fail('评论错误')
            break
        }
      })
    }

    function refresh() {
      if (props.canteensInf.length !== 0) {
        axios.request({
          url: '/getCanteenComments',
          method: 'post',
          data: {
            canteen_id: props.canteensInf[data.activeIndex].id
          }
        }).then((response) => {
          switch (response.data.status) {
            case 0:
              data.comments = response.data.comments
              break
            default:
              Toast.fail('未知错误')
              break
          }
        })
      }
    }

    function showCommentDetail(comment) {
      data.commentSelect = comment
      data.showDetail = true
    }

    return {
      ...toRefs(data),
      navClick,
      inputFocus,
      showCommentDetail
    }
  }
}

</script>

<style scoped>
.van-card {
  --van-card-thumb-size: 60px
}
</style>
