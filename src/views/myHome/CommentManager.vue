<template>
  <div class="favorites" style="height: 100%;">
    <MyHeader title="评论管理"/>
    <div v-if="comments.length > 0">
      <van-card v-for="comment of comments" :key="`comment${comment.comment_id}`"
                style="border-radius: 15px; margin:7px ;box-shadow: 5px 5px 5px #8e8d8d;">
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
        <template #footer>
          <van-button type="danger" style="height: 100%;"
                      @click="deleteComment(comment.comment_id)">删除
          </van-button>
        </template>

      </van-card>
    </div>
    <van-empty v-else description="暂无评论"/>
  </div>
</template>

<script>
import {Toast} from 'vant'
import axios from '../../api/api'
import {reactive, toRefs, onMounted} from 'vue'
import MyHeader from '@/components/MyHeader.vue'

export default {
  setup() {
    const data = reactive({
      comments: [],
    })

    function deleteComment(index) {
      axios.post('/deleteComment', {
        comment_id: index
      }).then((response) => {
        switch (response.data.status) {
          case 0:
            Toast.success('已删除评论')
            refresh()
            break
          default:
            Toast.fail('未知错误')
            break
        }
      })
    }

    onMounted(() => {
      refresh()
    })
    function refresh() {
      axios.post('/getAllComments').then((response) => {
        switch (response.data.status) {
          case 0:
            data.comments = response.data.comments
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

    return ({
      ...toRefs(data),
      deleteComment
    })
  },
  components: {MyHeader}
}
</script>

<style scoped>
.van-card {
  --van-card-thumb-size: 60px
}
</style>
