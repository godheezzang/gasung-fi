<template>
  <div class="article-wrap">
    <div class="article-container">
      <div class="article-detail">
        <div class="article-header">
          <p class="article-title">{{ article.title }}</p>
        </div>
        <div class="article-desc">
          <p class="article-user">
            작성자<span>{{ article.username }}</span>
          </p>
          <p class="article-time">
            작성일<span>{{ formattedCreatedAt }}</span>
          </p>
        </div>
        <div class="article-body">
          <img
            v-if="article.image"
            :src="imageUrl"
            alt="Image"
            class="article-image"
          />
          <p>{{ article.content }}</p>
        </div>
      </div>
      <div class="comment-wrap">
        <p class="comment-count">
          <span>{{ article.comment_count }}</span
          >개의 댓글
        </p>
        <div class="comment-container">
          <CommentListItem
            v-if="article.comment_count"
            v-for="comment in article.comments"
            :key="comment.id"
            :comment="comment"
            @commentDeleted=""
          />
          <div v-if="!article.comment_count">
            <p>댓글이 없습니다.</p>
          </div>
        </div>
        <CommentCreate @commentCreated="addComment" />
      </div>
      <!-- TODO: 사용자 동일 여부에 따라 삭제, 수정버튼 렌더링 -->
      <div class="article-btn-container">
        <Button content="목록" :onClick="moveToList" ariaLabel="게시글 목록" />
        <Button
          v-if="article.email === store.userEmail"
          content="삭제"
          :onClick="handleDelete"
          ariaLabel="게시글 삭제"
        />
        <Button
          v-if="article.email === store.userEmail"
          content="수정"
          :onClick="moveToUpdate"
          ariaLabel="게시글 수정"
        />
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
const imageUrl = ref("");

const formatDate = (dateString) => {
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hours = date.getHours();
  const minutes = String(date.getMinutes()).padStart(2, "0");

  const formattedTime = (hours === 0 ? 24 : hours) + ":" + minutes;

  return `${year}.${month}.${day} ${formattedTime}`;
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
      const response = await axios.delete(
        `${import.meta.env.VITE_BASE_URL}/articles/${articleId}/`,
        {
          headers: {
            Authorization: `Token ${store.token}`,
          },
        }
      );

      // console.log(response);
      if (response.status === 204) {
        router.push({ name: "community" });
      }
    } catch (error) {
      console.error(error);
    }
  }
};

const addComment = (newComment) => {
  article.value.comments.push(newComment);
  article.value.comment_count += 1;
};

const moveToUpdate = () => {
  router.push({ name: "create_article", query: { article_id: articleId } });
};

const getDetailArticle = async () => {
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_BASE_URL}/articles/${articleId}/`
    );

    if (response.status === 200) {
      // console.log(response);
      article.value = response.data;
      imageUrl.value = `${import.meta.env.VITE_BASE_URL}${response.data.image}`;
      // console.log(imageUrl.value);
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
  /* box-shadow: inset 0 0 20px blue; */
}

.article-container {
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
  padding: 1rem;
  gap: 1rem;
  margin-bottom: 1rem;
}

.article-detail {
  /* box-shadow: inset 0 0 20px yellow; */
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0 1rem;
  gap: 1rem;
  flex-shrink: 0;
  min-height: 30rem;
  border-bottom: 1px solid var(--color-gray-02);
  flex-wrap: wrap;
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

.article-desc span {
  border-left: 1px solid var(--color-gray-02);
  padding-left: 1rem;
  margin-left: 1rem;
}

.article-body {
  /* box-shadow: inset 0 0 20px gray; */
  flex-grow: 2;
  flex-shrink: 0;
  margin-top: 2rem;
  padding: 0 0 3rem 0;
}

.article-body p {
  width: 100%;
}

.comment-wrap {
  /* box-shadow: inset 0 0 20px lime; */
  padding: 1rem 1rem;
}

.comment-wrap span {
  font-weight: var(--font-weight-medium);
  color: var(--color-primary-blue);
}

.comment-count {
  margin-bottom: 1rem;
  font-size: var(--font-size-mlarge);
  border-bottom: 1px solid var(--color-gray-02);
  padding-bottom: 2rem;
}

/* .comment-container {
  box-shadow: inset 0 0 20px paleturquoise;
} */

.article-btn-container {
  /* box-shadow: inset 0 0 20px orange; */
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.article-image {
  max-width: 50rem;
  margin: 2rem 0;
}

.article-image:hover {
  border: 1px solid var(--color-gray-02);
}
</style>
