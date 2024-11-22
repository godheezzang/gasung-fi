<template>
  <div>
    <form @submit.prevent="handleCreate">
      <textarea
        id="reply"
        placeholder="250자 이내의 댓글을 달아주세요. 욕설 및 비방은 삭제 조치됩니다."
        v-model="commentInput"
      ></textarea>
      <button type="submit">작성</button>
    </form>
  </div>
</template>

<script setup>
import { useUserStore } from "@/stores/user";
import axios from "axios";
import { ref } from "vue";
import { useRoute } from "vue-router";

const props = defineProps({
  isReply: Boolean,
  parentId: Number,
});

const commentInput = ref("");
const route = useRoute();
const articleId = route.params.article_id;
const store = useUserStore();
const emit = defineEmits(["close"]);

const handleCreate = async () => {
  try {
    const url = props.isReply
      ? `${import.meta.env.VITE_BASE_URL}/articles/${articleId}/comments/${
          props.parentId
        }/`
      : `${import.meta.env.VITE_BASE_URL}/articles/${articleId}/comments/`;

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
      emit("close");
    }
  } catch (error) {
    console.error(error);
  }
};
</script>

<style scoped></style>
