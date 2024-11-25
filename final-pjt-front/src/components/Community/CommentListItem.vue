<template>
  <div class="comment-container">
    <!-- {{ comment }} -->
    <p>{{ comment.username }}</p>
    <p>{{ comment.content }}</p>
    <button @click="handleDelete" v-if="isCurrentUser">삭제</button>
    <button @click="toggleReply" v-if="!isComment">
      {{ isReply ? "답글 취소" : "답글" }}
    </button>
    <button @click="handleUpdate" v-if="isCurrentUser">수정</button>

    <div v-if="comment.replies" class="reply-container">
      <CommentListItem v-for="reply in comment.replies" :key="reply.id" :comment="reply" :isComment="true" />
    </div>
    <CommentCreate v-if="isReply" :isReply="true" :parentId="comment.id" @close="isReply = false" class="reply-container" />
  </div>
</template>

<script setup>
import CommentCreate from "@/components/Community/CommentCreate.vue";
import { useUserStore } from "@/stores/user";
import axios from "axios";
import { computed, defineAsyncComponent, ref } from "vue";
import { useRoute } from "vue-router";

const props = defineProps({
  comment: Object,
  reply: Object,
  isComment: {
    type: Boolean,
    default: false,
  },
});

const route = useRoute();
const store = useUserStore();

const articleId = route.params.article_id;
const isReply = ref(false);

const CommentListItem = defineAsyncComponent(() => import("@/components/Community/CommentListItem.vue"));

// console.log(props.comment);

const userEmail = computed(() => sessionStorage.getItem("userEmail").replace(/"/g, ""));
const isCurrentUser = computed(() => {
  // console.log("userEmail:", userEmail.value);
  // console.log("commentUser:", String(props.comment.email));

  // console.log(typeof userEmail.value);
  // console.log(typeof props.comment.email);

  return String(userEmail.value) === String(props.comment.email);
});

console.log("isCurrentUser:", isCurrentUser.value);

const toggleReply = () => {
  isReply.value = !isReply.value;
};

const handleDelete = async () => {
  try {
    const response = await axios.delete(`${import.meta.env.VITE_BASE_URL}/articles/${articleId}/comments/${props.comment.id}`, {
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });

    console.log(response);
  } catch (error) {}
};

// TODO: 댓글 수정 구현
const handleUpdate = async () => {
  try {
  } catch (error) {}
};
</script>

<style scoped>
.reply-container {
  margin-left: 2rem;
}
</style>
