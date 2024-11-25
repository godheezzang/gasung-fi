<template>
  <div>
    <form @submit.prevent="isEdit ? handleUpdate() : handleCreate()" class="comment-form">
      <Textarea placeholder="250자 이내의 댓글을 달아주세요. 욕설 및 비방은 삭제 조치됩니다." id="reply" v-model="commentInput" />
      <button type="submit">작성</button>
    </form>
  </div>
</template>

<script setup>
import Textarea from "@/components/Common/Textarea.vue";
import { useUserStore } from "@/stores/user";
import axios from "axios";
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const props = defineProps({
  isReply: Boolean,
  parentId: Number,
});

const commentInput = ref("");
const route = useRoute();
const articleId = route.params.article_id;
const store = useUserStore();
// const emit = defineEmits(["close"]);
const isEdit = ref(false);
const router = useRouter();

// TODO: 댓글 수정

// onMounted(async () => {
//   if (articleId && commentId) {
//     isEdit.value = true;
//     try {
//       const response = await axios.get(`${import.meta.env.VITE_BASE_URL}/articles/${articleId}/`);

//       (titleInput.value = response.data.title), (contentInput.value = response.data.content);
//     } catch (error) {
//       console.error(error);
//     }
//   }
// });

const handleCreate = async () => {
  try {
    const url = props.isReply ? `${import.meta.env.VITE_BASE_URL}/articles/${articleId}/comments/${props.parentId}/` : `${import.meta.env.VITE_BASE_URL}/articles/${articleId}/comments/`;

    const response = await axios.post(
      url,
      {
        content: commentInput.value,
      },
      {
        headers: { Authorization: `Token ${store.token}` },
      }
    );

    console.log(response);
    if (response.status === 200) {
      commentInput.value = "";
      // emit("close");
    }
  } catch (error) {
    console.error(error);
  }
};

const handleUpdate = () => {};
</script>

<style scoped>
.comment-form {
  display: flex;
  gap: 1rem;
  padding: 1rem;
}

.comment-form button {
  margin: 1rem;
  width: 10rem;
  background-color: var(--color-primary-blue);
  color: var(--color-white);
  font-weight: var(--font-weight-medium);
  border-radius: 5px;
}
</style>
