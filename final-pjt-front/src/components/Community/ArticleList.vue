<template>
  <div>
    <h2>게시글 목록</h2>
    <ArticleListItem
      v-for="article in articles"
      :key="article.article_id"
      :article="article"
    />
  </div>
  <Button :onClick="moveToCreate" content="글쓰기" ariaLabel="글쓰기" />
</template>

<script setup>
import Button from "@/components/Common/Button.vue";
import ArticleListItem from "@/components/Community/ArticleListItem.vue";
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const articles = ref([]);

const moveToCreate = () => {
  router.push({ name: "create_article" });
};

const getArticles = async () => {
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_BASE_URL}/articles/`
    );
    // console.log(response);
    articles.value = response?.data;
    // console.log(articles.value);
  } catch (error) {
    console.error(error);
  }
};
onMounted(() => {
  getArticles();
});
</script>

<style scoped></style>
