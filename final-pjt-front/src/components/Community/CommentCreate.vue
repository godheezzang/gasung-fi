<template>
  <div>
    <form
      @submit.prevent="isEdit ? handleUpdate() : handleCreate()"
      class="comment-form"
    >
      <Textarea
        placeholder="250자 이내의 댓글을 달아주세요. 욕설 및 비방은 삭제 조치됩니다."
        id="reply"
        v-model="commentInput"
      />
      <button type="submit">작성</button>
    </form>
    <p class="err-msg" v-if="!isValid">댓글 내용을 작성해 주세요.</p>
    <p class="err-msg" v-if="commentInput.length > 250">
      댓글 작성은 250자까지만 가능합니다.
    </p>
  </div>
  <div>
    <Teleport to="body">
      <Modal :show="showModal" @close="showModal = false">
        <template #header>
          <h3>로그인 필요</h3>
        </template>
        <template #body>
          <p>로그인이 필요한 서비스입니다.</p>
          <p>로그인하시고 이용해보세요!</p>
        </template>
        <template #footer>
          <button
            @click="
              () => {
                console.log('Redirect button clicked');
                redirectToLogin();
              }
            "
          >
            확인
          </button>

          <button @click="showModal = false">취소</button>
        </template>
      </Modal>
    </Teleport>
  </div>
</template>

<script setup>
import Modal from "@/components/Common/Modal.vue";
import Textarea from "@/components/Common/Textarea.vue";
import { useUserStore } from "@/stores/user";
import axios from "axios";
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const props = defineProps({
  isReply: Boolean,
  parentId: Number,
});

const emit = defineEmits(["close", "commentCreated"]);
const commentInput = ref("");
const route = useRoute();
const articleId = route.params.article_id;
const store = useUserStore();
const isEdit = ref(false);
const router = useRouter();
const showModal = ref(false);
const isValid = ref(true);
const userStore = useUserStore();

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

const redirectToLogin = () => {
  console.log("log");
  router.push({ name: "login" }); // 로그인 페이지로 이동
  commentInput.value = "";
  showModal.value = false; // 모달 닫기
};

const handleCreate = async () => {
  if (!store.isLoggedIn) {
    showModal.value = true;
    return;
  }

  if (commentInput.value.length > 250) {
    return;
  }

  if (commentInput.value.trim() === "") {
    isValid.value = false;
    return;
  }
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
    if (response.status === 201) {
      const newComment = {
        ...response.data,
        username: userStore.username,
      };
      commentInput.value = "";
      emit("close");
      emit("commentCreated", newComment);
      router.go(0);
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
  padding-top: 1rem;
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
