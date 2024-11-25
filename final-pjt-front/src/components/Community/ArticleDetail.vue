<template>
  <div class="article-wrap">
    <div class="article-container">
      <div class="article-detail">
        <div class="article-header">
          <p class="article-title">{{ article.title }}</p>
        </div>
        <div class="article-desc">
          <p class="article-user">작성자: {{ article.username }}</p>
          <p class="article-time">작성일: {{ formattedCreatedAt }}</p>
        </div>
        <div class="article-body">
          <p>{{ article.content }}</p>
        </div>
      </div>
      <hr />
      <div class="comment-wrap">
        <p>
          <span>{{ article.comment_count }}개의 댓글</span>
        </p>
        <div class="comment-container">
          <CommentListItem v-if="article.comment_count" v-for="comment in article.comments" :key="comment.id" :comment="comment" />
          <div v-if="!article.comment_count">댓글이 없습니다.</div>
        </div>
      </div>
      <CommentCreate />
      <!-- TODO: 사용자 동일 여부에 따라 삭제, 수정버튼 렌더링 -->
      <div class="article-btn-container">
        <Button content="목록" :onClick="moveToList" ariaLabel="게시글 목록" />
        <Button v-if="article.email === store.userEmail" content="삭제" :onClick="handleDelete" ariaLabel="게시글 삭제" />
        <Button v-if="article.email === store.userEmail" content="수정" :onClick="moveToUpdate" ariaLabel="게시글 수정" />
      </div>
    </div>
  </div>
</template>

<script setup>
import Button from "@/components/Common/Button.vue";
import CommentCreate from "@/components/Community/CommentCreate.vue";
import CommentListItem from "@/components/Community/CommentListItem.vue";
import { useUserStore } from "@/stores/user";
import axios from "axios";
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const articleId = route.params.article_id;
const article = ref("");
const store = useUserStore();

const formatDate = (dateString) => {
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hours = date.getHours();
  const minutes = String(date.getMinutes()).padStart(2, "0");

  const formattedTime = (hours === 0 ? 24 : hours) + "시 " + minutes + "분";

  return `${year}년  ${month}월 ${day}일 ${formattedTime}`;
};

const formattedCreatedAt = computed(() => formatDate(article.value.created_at));
const formattedUpdatedAt = computed(() => formatDate(article.value.updated_at));

const moveToList = () => {
  router.push({ name: "community" });
};

const handleDelete = async () => {
  window.confirm("게시글을 삭제하시겠습니까?");
  if (confirm) {
    try {
      const response = await axios.delete(`${import.meta.env.VITE_BASE_URL}/articles/${articleId}/`, {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      });

      // console.log(response);
      if (response.status === 204) {
        router.push({ name: "community" });
      }
    } catch (error) {
      console.error(error);
    }
  }
};

const moveToUpdate = () => {
  router.push({ name: "create_article", query: { article_id: articleId } });
};

const getDetailArticle = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_BASE_URL}/articles/${articleId}/`);

    if (response.status === 200) {
      console.log(response);
      article.value = response.data;
    }
  } catch (error) {
    console.error(error);
  }
};
onMounted(() => {
  getDetailArticle();
});
</script>

<style scoped>
.article-wrap {
  margin-top: 2rem;
  box-shadow: inset 0 0 20px blue;
}

.article-container {
  /* box-shadow: inset 0 0 20px red; */
  width: 70%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  min-height: 80vh;
  border: 1px solid var(--color-gray-02);
  border-top: unset;
  border-bottom: unset;
  gap: 1rem;
}

.article-detail {
  box-shadow: inset 0 0 20px yellow;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0 2rem;
  gap: 1rem;
}

.article-header {
  /* box-shadow: inset 0 0 20px skyblue; */
  flex-grow: 0.2;
  display: flex;
  align-items: center;
}

.article-title {
  font-weight: var(--font-weight-medium);
  font-size: var(--font-size-large);
}

.article-desc {
  /* box-shadow: inset 0 0 20px hotpink; */
  flex-grow: 0;
}

.article-body {
  /* box-shadow: inset 0 0 20px gray; */
  flex-grow: 2;
}

.comment-wrap {
  box-shadow: inset 0 0 20px lime;
}

.comment-container {
  box-shadow: inset 0 0 20px paleturquoise;
}

.article-btn-container {
  box-shadow: inset 0 0 20px orange;
  display: flex;
  justify-content: center;
  gap: 1rem;
}
</style>
