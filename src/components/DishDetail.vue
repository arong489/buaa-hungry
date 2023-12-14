<template>
  <van-image :src="dish.img" position="center" :style="imgStyle" fit="cover" />
  <h1>{{ dish.name }}</h1>
  <strong style="color: red;">&yen;</strong>
  <strong style="color: red; font-size: 3ch;">{{ dish.price }}</strong>
  <van-tabs shrink>
    <van-tab title="详情">
      <van-button v-if="modifyDish" @click="removeDish">
        <template #icon>
          <van-icon name="close" size="2rem" />
        </template>
      </van-button>
      <van-button @click="onClick">
        <template #icon>
          <van-icon :name="buttonIcon" :color="buttonIconColor" size="2rem" />
        </template>
      </van-button>

      <van-divider style="clear: both;" />
      <van-field readonly label="商品描述"><template #input>{{ dish.description }}</template></van-field>
    </van-tab>
    <van-tab title="评论">
      <van-field v-if="addCommentEnable" v-model="newComment" rows="1" autosize type="textarea" placeholder="点我输入评论">
        <template #button>
          <van-button type="primary" v-show="newComment.length > 0" @click="createComment">发表</van-button>
        </template>
      </van-field>
      <van-card v-for="comment in dishComments" :key="`comment${comment.comment_id}`"
        style="border-radius: 15px; margin: 10px;box-shadow: 5px 5px 5px #8e8d8d;" @click="showCommentDetail(comment)">
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
    </van-tab>
  </van-tabs>

  <van-popup v-model:show="ifShowCommentDetail" position="bottom" :close-on-click-overlay='false'
    @click-overlay="ifShowCommentDetail = false" :closeable="true" style="height: 100%;">
    <commentDetail :fatherComment="detailComment" />
  </van-popup>
</template>

<script>
import { Toast } from 'vant'
import axios from '../api/api'
import { reactive, toRefs, watch } from 'vue'
import commentDetail from './commentDetail.vue'

export default {
  props: ['dish'],
  components: { commentDetail },
  setup(props) {
    const data = reactive({
      dishComments: [],
      imgStyle: {
        width: '100%'
      },
      newComment: '',
      modifyDish: false,
      buttonIcon: '',
      buttonIconColor: '',
      ifShowCommentDetail: false,
      detailComment: {},
      addCommentEnable: localStorage.getItem('identity') === '0'
    })

    function createComment() {
      axios.post('/commentOnDish', {
        dish_id: props.dish.id ? props.dish.id : props.dish.dish_id,
        content: data.newComment
      }).then((response) => {
        switch (response.data.status) {
          case 0:
            Toast.success('评论成功')
            refreshComments(props.dish)
            data.newComment = ''
            break
          case -2:
            break
          default:
            Toast.fail('未知错误')
            break
        }
      })
    }

    function showCommentDetail(comment) {
      data.detailComment = comment
      data.ifShowCommentDetail = true
    }

    function refreshComments(dish) {
      axios.post('/getDishComments', { dish_id: dish.id ? dish.id : dish.dish_id }).then((response) => {
        switch (response.data.status) {
          case 0:
            data.dishComments = response.data.comments
            break
          case -2:
            break
          default:
            Toast.fail('未知错误')
            break
        }
      })
    }

    async function checkLike(dish) {
      if (localStorage.getItem('identity') !== '0') {
        return false
      }
      let result = false
      await axios.post('/judgeFavorite', {
        dish_id: dish.id ? dish.id : dish.dish_id
      }).then((response) => {
        switch (response.data.status) {
          case 0:
            result = response.data.exist
            break
          case -2:
            break
          default:
            Toast.fail('未知错误')
            break
        }
      })
      return result
    }

    function onClick() {
      switch (localStorage.getItem('identity')) {
        case '0':
          data.buttonIcon === 'like-o' ? like() : dislike()
          break
        case '2':
          modify()
          break
        default:
          Toast.fail('配送员权限错误')
          break
      }
    }

    function like() {
      axios.post('/favoriteDish', {
        dish_id: props.dish.id ? props.dish.id : props.dish.dish_id,
        note: ''
      }).then((response) => {
        switch (response.data.status) {
          case 0:
            data.buttonIcon = 'like'
            data.buttonIconColor = '#ee0a24'
            Toast.success('收藏成功')
            break
          case 1:
            Toast.fail('已收藏')
            break
          case -2:
            break
          default:
            Toast.fail('未知错误')
            break
        }
      })
    }

    function dislike() {
      axios.post('/deleteFavorite', {
        dish_id: props.dish.id ? props.dish.id : props.dish.dish_id
      }).then((response) => {
        switch (response.data.status) {
          case 0:
            data.buttonIcon = 'like-o'
            data.buttonIconColor = ''
            Toast.success('已取消收藏')
            break
          case 1:
            Toast.fail('未收藏过该菜品')
            break
          case -2:
            break
          default:
            Toast.fail('未知错误')
            break
        }
      })
    }

    function modify() {
      Toast('修改请在dishDetail 174行左右实现')
    }

    function removeDish() {
      const tempDish = props.dish
      tempDish.available = false
      axios.post('/delete_favorite', tempDish).then((response) => {
        switch (response.data.status) {
          case 0:
            Toast.success('菜品已删除')
            break
          case -2:
            break
          default:
            Toast.fail('未知错误')
            break
        }
      })
    }

    watch(
      () => props.dish,
      async (dish, preDish) => {
        const img = new Image()
        img.src = dish.img
        if (img.height > img.width) {
          data.imgStyle['aspect-ratio'] = 1
        } else {
          delete data.imgStyle['aspect-ratio']
        }
        refreshComments(dish)
        const identity = localStorage.getItem('identity')
        data.modifyDish = identity === '2'
        const like = await checkLike(dish)
        data.buttonIcon = identity === '0' ? like ? 'like' : 'like-o' : identity === '2' ? 'more-o' : 'close'
        data.buttonIconColor = like ? '#ee0a24' : ''
      },
      {
        immediate: true
      }
    )

    return ({
      ...toRefs(data),
      createComment,
      onClick,
      removeDish,
      showCommentDetail
    })
  }
}
</script>

<style scoped>
.van-card {
  --van-card-thumb-size: 60px
}

.van-button {
  --van-button-border-width: 0;
  margin-right: 1rem;
  float: right;
  --van-button-default-height: 2rem;
  --van-button-normal-padding: 0;
}
</style>
