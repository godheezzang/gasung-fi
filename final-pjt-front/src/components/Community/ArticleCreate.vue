<template>
  <div class="article-create-wrap">
    <div class="article-create-container">
      <h1 class="article-create-title">
        게시글 {{ isEdit ? "수정" : "작성" }}
      </h1>
      <form
        @submit.prevent="isEdit ? saveArticle('put') : saveArticle('post')"
        class="article-form"
      >
        <div class="article-input">
          <label for="title"></label>
          <Textarea
            type="text"
            id="title"
            placeholder="제목을 작성해 주세요."
            v-model="titleInput"
            maxlength="100"
            class="article-title-input"
          />
          <p class="err-msg" v-if="titleInput.length === 100">
            제목은 100자까지 입력 가능합니다.
          </p>
          <p class="err-msg" v-if="!isValidTitle">제목을 입력해 주세요.</p>
        </div>
        <div class="article-input">
          <label for="content"></label>
          <Textarea
            placeholder="내용을 작성해 주세요."
            id="content"
            v-model="contentInput"
          />
          <p class="err-msg" v-if="!isValidContent">내용을 입력해 주세요.</p>
        </div>
        <div class="article-input">
          <div class="article-upload">
            <input
              type="file"
              id="upload-image"
              hidden
              @change="handleFileUpload($event)"
              accept="image/*"
            />
            <p class="article-imglabel">이미지 첨부하기</p>

            <label for="upload-image">
              <img src="@/assets/icons/icon_upload.svg" class="article-img" />
            </label>
            <div class="filename" v-if="imgFile">
              <p>{{ imgFile.name }}</p>
              <button type="button" @click="removeFile">x</button>
            </div>
          </div>
        </div>

        <div class="article-create-btn">
          <Button content="게시" ariaLabel="글 게시" type="submit" />
        </div>
      </form>
    </div>
  </div>
  <Loading :isLoading="isLoading" />
</template>

<script setup>
import Button from "@/components/Common/Button.vue";
import Loading from "@/components/Common/Loading.vue";
import Textarea from "@/components/Common/Textarea.vue";
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

const isLoading = ref(false);
const imgFile = ref(null);
const isValidTitle = ref(true);
const isValidContent = ref(true);
const imgExtensions = [".jpg", ".png", ".jpeg", ".gif", ".svg"];

onMounted(async () => {
  isLoading.value = true;
  if (articleId) {
    isEdit.value = true;
    try {
      const response = await axios.get(
        `${import.meta.env.VITE_BASE_URL}/articles/${articleId}/`
      );

      titleInput.value = response.data.title;
      contentInput.value = response.data.content;
      isLoading.value = false;
    } catch (error) {
      console.error(error);
    }
  } else {
    isLoading.value = false;
    return;
  }
});

const isValidImageExtension = (fileName) => {
  const extension = fileName
    .slice(((fileName.lastIndexOf(".") - 1) >>> 0) + 2)
    .toLowerCase();
  return imgExtensions.includes(`.${extension}`);
};

const handleFileUpload = async (event) => {
  // console.log(event.target);
  const file = event.target.files[0];
  if (file) {
    if (!isValidImageExtension(file.name)) {
      alert(
        "파일 형식은 '.jpg', '.jpeg', '.png', '.gif', '.svg' 확장자만 첨부 가능합니다."
      );
      imgFile.value = null;
      event.target.value = "";
      return;
    }
    imgFile.value = file;
  }
};

const removeFile = () => {
  imgFile.value = null;
  document.getElementById("upload-image").value = "";
};

const saveArticle = async (method) => {
  isLoading.value = true;

  if (titleInput.value === "") {
    isValidTitle.value = false;
    return;
  }
  if (contentInput.value === "") {
    isValidContent.value = false;
    return;
  }

  const formData = new FormData();
  formData.append("title", titleInput.value);
  formData.append("content", contentInput.value);
  if (imgFile.value) {
    formData.append("image", imgFile.value);
  }

  try {
    const url =
      method === "post"
        ? `${import.meta.env.VITE_BASE_URL}/articles/`
        : `${import.meta.env.VITE_BASE_URL}/articles/${articleId}/`;

    const response = await axios({
      method: method,
      url: url,
      data: formData,
      headers: {
        Authorization: `Token ${store.token}`,
        "Content-Type": "multipart/form-data",
      },
    });

    if (
      (method === "post" && response.status === 201) ||
      (method === "put" && response.status === 200)
    ) {
      isLoading.value = false;
      router.push(
        method === "post"
          ? { name: "community" }
          : { name: "article_detail", params: { article_id: articleId } }
      );
    }
  } catch (error) {
    console.error(error);
    isLoading.value = false;
  }
};

const handleCreate = () => saveArticle("post");
const handleUpdate = () => saveArticle("put");
</script>

<style scoped>
.article-create-wrap {
  /* box-shadow: inset 0 0 20px red; */
  margin-top: 2rem;
}

.err-msg {
  margin-left: 0.4rem;
  margin-bottom: 1rem;
  font-size: var(--font-size-medium);
  text-align: center;
}
.article-create-container {
  /* box-shadow: inset 0 0 20px blue; */
  /* box-shadow: inset 0 0 20px red; */
  width: 50%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  min-height: 80vh;
  border: 1px solid var(--color-gray-02);
  /* border-top: unset; */
  /* border-bottom: unset; */
  border-radius: 5px;
  padding: 2rem;
  gap: 1rem;
  margin-bottom: 1rem;
  justify-content: center;
}

.article-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.article-create-title {
  font-size: var(--font-size-mlarge);
  font-weight: var(--font-weight-bold);
  color: var(--color-gray-05);
  margin-bottom: 1rem;
  text-align: center;
}

.article-create-btn {
  display: flex;
  justify-content: center;
}

.article-input .article-title-input {
  min-height: unset;
}

.article-input textarea {
  min-height: 50rem;
}

.article-upload label {
  /* box-shadow: inset 0 0 20px red; */
  display: block;
  background-color: var(--color-gray-01);
  padding: 1rem;
  border-radius: 5px;
  border: 1px solid var(--color-gray-02);
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.article-imglabel {
  font-weight: var(--font-weight-medium);
  margin-bottom: 1rem;
}

.filename {
  background-color: var(--color-gray-01);
  width: fit-content;
  padding: 0.3rem 0.8rem;
  border-radius: 5px;
  border: 1px solid var(--color-gray-02);
  margin: 0.3rem 0.3rem 0.3rem 0;
  color: var(--color-gray-05);
  font-size: var(--font-size-small);
  display: flex;
  gap: 0.5rem;
}

.filename button {
  width: 1.5rem;
  border-radius: 5px;
}
</style>
