<template>
  <div v-for="comment in comments" :key="comment.id">
    <p>{{ comment.content }}</p>
    <button @click="showReply(comment.id)">回复</button>
    <div v-if="replyTargetId === comment.id">
      <textarea v-model="replyContent"></textarea>
      <button @click="addReply(comment.id)">提交</button>
    </div>
    <div v-for="reply in comment.replies" :key="reply.id">
      <p>{{ reply.content }}</p>
      <button @click="showReply(reply.targetId)">回复</button>
      <div v-if="replyTargetId === reply.id">
        <textarea v-model="replyContent"></textarea>
        <button @click="addReply(comment.id, reply.id)">提交</button>
      </div>
    </div>
  </div>

  <div>
    <textarea v-model="commentContent"></textarea>
    <button @click="addComment">提交评论</button>
  </div>
</template>

<script>
export default {
  props: ['CommentData', 'index'],
  comments: [
    {
      id: 1,
      content: '这道菜做得很好！',
      replies: [
        {
          id: 2,
          content: '阿里嘎多！',
          targetId: 1
        }
      ]
    }
  ],
  data() {
    return {
      commentContent: '',
      replyContent: '',
      replyTargetId: null,
      comments: [
        {
          id: 1,
          content: '这道菜做得很好！|| 这外卖送的很快！',
          replies: [
            {
              id: 2,
              content: '阿里嘎多！',
              targetId: 1
            }
          ]
        }
      ]
    }
  },
  methods: {
    addComment() {
      const comment = {
        id: this.comments.length + 1,
        content: this.commentContent,
        replies: []
      }
      this.comments.push(comment)
      this.commentContent = ''
    },
    addReply(commentId, targetId = null) {
      const reply = {
        id: this.comments.length + 1,
        content: this.replyContent,
        targetId: targetId
      }
      const comment = this.comments.find(comment => comment.id === commentId)
      comment.replies.push(reply)
      this.replyContent = ''
      this.replyTargetId = null
    },
    showReply(commentId) {
      this.replyTargetId = commentId
    }
  }
}
</script>

<style>
button{
  background-color:dodgerblue;
  color:white;
  width: 100px;
  height: 30px;
  border:0;
  font-size: 14px;
  border-radius: 30px;
//text-align: center;
//display:block;
}
button:hover{
  background-color: #00cc66;
}

</style>

