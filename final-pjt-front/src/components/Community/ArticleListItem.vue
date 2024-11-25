<template>
  <RouterLink
    :to="{
      name: 'article_detail',
      params: { article_id: article.id },
    }"
  >
    <div class="article-item">
      <div class="article-desc">
        <p class="article-id">{{ article.id }}</p>
        <p class="article-title">
          {{ article.title }}
          <span class="article-comment"></span>
        </p>
        <p class="article-username">{{ article.username }}</p>
      </div>
    </div>
  </RouterLink>
</template>

<script setup>
import { ref } from "vue";
import { RouterLink } from "vue-router";

const props = defineProps({
  article: Object,
});

// console.log(props.article);
</script>

<style scoped>
.article-item {
  /* box-shadow: inset 0 0 20px green; */
  padding: 2rem;
  border-bottom: 1px solid var(--color-gray-01);
}

.article-desc {
  display: flex;
  gap: 2rem;
  height: 1rem;
  align-items: center;
}

.article-id {
  flex-grow: 1;
  flex-basis: 6rem;
  text-align: center;
  border-right: 1px solid var(--color-gray-01);
}

.article-title {
  flex-grow: 2;
}

.article-username {
  flex-grow: 1;
  text-align: center;
}
</style>
