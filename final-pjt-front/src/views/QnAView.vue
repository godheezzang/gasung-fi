<template>
  <div class="main">
    <div class="chatbot-container">
      <div class="chat-window">
        <div class="chat-message" v-for="(msg, index) in messages" :key="index">
          <div v-if="msg.role === 'user'" class="user-message">
            <div class="bubble">{{ msg.content }}</div>
          </div>
          <div v-if="msg.role === 'chatbot'" class="chatbot-message">
            <TypingEffect :text="msg.content" />
          </div>
        </div>
      </div>

      <div class="input-container">
        <input v-model="userInput" @keyup.enter="sendMessage" placeholder="메시지를 입력해주세요." />
        <button @click="sendMessage">Send</button>
      </div>
    </div>
    <Loading :isLoading="isLoading" />
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useUserStore } from "@/stores/user";
import Loading from "@/components/Common/Loading.vue";
import TypingEffect from "@/components/Chatbot/TypingEffect.vue"; // TypingEffect 컴포넌트 임포트

const userInput = ref("");
const messages = ref([]); // 채팅 메시지 저장 배열
const BASE_URL = import.meta.env.VITE_BASE_URL;
const userStore = useUserStore();
const isLoading = ref(false);

// 사용자 입력 메시지 전송
const sendMessage = async () => {
  if (!userInput.value) return;
  isLoading.value = true;

  // 사용자 메시지 추가
  messages.value.push({ role: "user", content: userInput.value });

  const data = userInput.value;
  userInput.value = "";

  try {
    // 백엔드에 POST 요청 보내기
    const response = await axios({
      method: "post",
      url: `${BASE_URL}/chatbot/chat/`,
      data: {
        message: data,
      },
      headers: {
        Authorization: `Token ${userStore.token}`,
      },
    });

    // 챗봇 응답 추가
    if (response.data.response) {
      // 응답을 바로 추가
      messages.value.push({ role: "chatbot", content: response.data.response });
    }
    isLoading.value = false;
  } catch (error) {
    console.error("Error sending message:", error);
    messages.value.push({ role: "chatbot", content: "Sorry, something went wrong." });
    isLoading.value = false;
  }
};
</script>

<style scoped>
.main {
  display: flex;
  flex-direction: column;
  height: 80vh;
  align-items: center;
}

.chatbot-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
  background-color: #f5f5f5;
  width: 80rem;
}

.chat-window {
  flex-grow: 1;
  overflow-y: auto;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  background-color: white;
}

.chat-message {
  margin: 10px 0;
}

.user-message {
  text-align: right;
}

.chatbot-message {
  text-align: left;
}

.bubble {
  display: inline-block;
  padding: 10px;
  border-radius: 20px;
  max-width: 80%;
  word-wrap: break-word;
}

.user-message .bubble {
  background-color: #007bff;
  color: white;
}

.chatbot-message .bubble {
  background-color: #e9e9eb;
  color: black;
}

.input-container {
  display: flex;
  margin-top: 10px;
}

.input-container input {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.input-container button {
  padding: 10px 15px;
  margin-left: 5px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.input-container button:hover {
  background-color: #0056b3;
}
</style>
