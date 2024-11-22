<template>
  <div>
    <h1>게시글 {{ isEdit ? "수정" : "작성" }}</h1>
    <form @submit.prevent="isEdit ? handleUpdate() : handleCreate()">
      <div>
        <label for="title">제목: </label>
        <input
          type="text"
          id="title"
          placeholder="제목을 작성해 주세요."
          v-model="titleInput"
        />
      </div>
      <div>
        <label for="content">내용</label>
        <textarea
          id="content"
          placeholder="내용을 작성해 주세요."
          v-model="contentInput"
        ></textarea>
      </div>
      <Button content="게시" ariaLabel="글 게시" type="submit" />
    </form>
  </div>
</template>

<script setup>
import Button from "@/components/Common/Button.vue";
import { useUserStore } from "@/stores/user";
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const titleInput = ref("");
const contentInput = ref("");

const store = useUserStore();
const router = useRouter();
const route = useRoute();

const isEdit = ref(false);
const articleId = route.query.article_id;

onMounted(async () => {
  if (articleId) {
    isEdit.value = true;
    try {
      const response = await axios.get(
        `${import.meta.env.VITE_BASE_URL}/articles/${articleId}/`
      );

      (titleInput.value = response.data.title),
        (contentInput.value = response.data.content);
    } catch (error) {
      console.error(error);
    }
  }
});

const handleCreate = async () => {
  try {
    const data = {
      title: titleInput.value,
      content: contentInput.value,
    };
    const response = await axios.post(
      `${import.meta.env.VITE_BASE_URL}/articles/`,
      data,
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );

    if (response.status === 201) {
      router.push({ name: "community" });
    }
  } catch (error) {
    console.error(error);
  }
};

const handleUpdate = async () => {
  try {
    const data = {
      title: titleInput.value,
      content: contentInput.value,
    };
    const response = await axios.put(
      `${import.meta.env.VITE_BASE_URL}/articles/${articleId}/`,
      data,
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );

    if (response.status === 200) {
      router.push({ name: "community" });
    }
  } catch (error) {
    console.error(error);
  }
};
</script>

<style scoped></style>
