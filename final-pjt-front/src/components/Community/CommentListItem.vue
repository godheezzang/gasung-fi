<template>
  <div class="comment-container">
    <p class="comment-username">{{ comment.username }}</p>
    <p class="comment-content">{{ comment.content }}</p>
    <div class="comment-btns">
      <button @click="handleDelete" v-if="isCurrentUser">삭제</button>
      <button @click="toggleReply" v-if="!isComment">
        {{ isReply ? "답글 취소" : "답글" }}
      </button>
      <button @click="handleUpdate" v-if="isCurrentUser">수정</button>
    </div>

    <div v-if="comment.replies" class="reply-container">
      <CommentListItem
        v-for="reply in comment.replies"
        :key="reply.id"
        :comment="reply"
        :isComment="true"
      />
    </div>
    <CommentCreate
      v-if="isReply"
      :isReply="true"
      :parentId="comment.id"
      @close="isReply = false"
      @commentCreated="handleCommentCreated"
      class="reply-container"
    />
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

const CommentListItem = defineAsyncComponent(() =>
  import("@/components/Community/CommentListItem.vue")
);

const userEmail = computed(() =>
  sessionStorage.getItem("userEmail").replace(/"/g, "")
);
const isCurrentUser = computed(() => {
  return String(userEmail.value) === String(props.comment.email);
});

const toggleReply = () => {
  isReply.value = !isReply.value;
};

const handleDelete = async () => {
  try {
    const response = await axios.delete(
      `${import.meta.env.VITE_BASE_URL}/articles/${articleId}/comments/${
        props.comment.id
      }/`,
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );

    console.log(response);
    if (response.status === 204) {
      emit("commentDeleted", props.comment.id);
    }
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

.comment-container {
  width: 100%;
  /* padding: 0 1rem; */
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
  background-color: var(--color-spinner-blue);
  padding: 1rem;
  border-radius: 10px;
}

.comment-username {
  font-weight: var(--font-weight-medium);
  font-size: var(--font-size-mlarge);
  color: var(--color-deep-blue);
  letter-spacing: -1px;
}

.comment-content {
  overflow: hidden;
  white-space: normal;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 100;
  line-clamp: 100;
  word-break: break-word;
}

.comment-btns {
  margin-top: 0.5rem;
  display: flex;
  gap: 0.5rem;
}

.comment-btns button {
  background-color: var(--color-black);
  border-radius: 5px;
  font-size: var(--font-size-extra-small);
  padding: 0.5rem;
  color: var(--color-white);
}

.comment-btns button:hover {
  background-color: var(--color-gray-03);
}
</style>
