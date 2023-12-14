<template>
  <div style="height: 2rem;"></div>
  <van-card style="border-radius: 15px; margin:7px ;box-shadow: 5px 5px 5px #8e8d8d;">
    <template #thumb>
      <img :src="fatherComment.img" alt="头像缺失" style="aspect-ratio: 1; width: 50px; border-radius: 50%">
    </template>
    <template #title><strong style="font-size: 2.5ch">{{ fatherComment.nick_name }}</strong><br></template>
    <template #desc>
      {{ fatherComment.create_time }}
    </template>
    <template #bottom>
      {{ fatherComment.content }}
    </template>
  </van-card>

  <van-field v-model="newComment" rows="1" autosize type="textarea" placeholder="点我输入评论">
    <template #button>
      <van-button type="primary" v-show="newComment.length > 0" @click="inputFocus">留言</van-button>
    </template>
  </van-field>
  <div v-if="comments.length > 0">
    <van-card v-for="comment of comments" :key="`comment${comment.comment_id}`"
      style="border-radius: 15px; margin:7px 7px 7px 20px;box-shadow: 5px 5px 5px #8e8d8d;">
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
</template>

<script>

import { onMounted, ref, reactive, toRefs, watch } from 'vue'

import axios from '@/api/api'
import { Toast } from 'vant'

export default {
  props: ['fatherComment'],
  setup(props) {
    const btnShow = true
    const data = reactive({
      activeIndex: 0,
      comments: [],
      newComment: ''
    })
    const activeNames = ref(['1'])

    watch(
      () => props.fatherComment,
      (comment, oldComment) => {
        refresh()
      },
      {
        immediate: true
      }
    )

    const inputFocus = () => {
      axios.request({
        url: '/commentOnComment',
        method: 'post',
        data: {
          comment_id: props.fatherComment.comment_id ? props.fatherComment.comment_id : props.fatherComment.id,
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
      axios.request({
        url: '/getCommentComments',
        method: 'post',
        data: {
          comment_id: props.fatherComment.comment_id ? props.fatherComment.comment_id : props.fatherComment.id
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

    let activeIndex
    return {
      activeIndex,
      btnShow,
      activeNames,
      ...toRefs(data),
      inputFocus
    }
  }
}

</script>

<style scoped>
.van-card {
  --van-card-thumb-size: 60px
}
</style>
