import axios from "axios";
import { useUserStore } from "@/stores/user";

const axiosInstance = axios.create({
  baseURL: import.meta.VITE_BASE_URL,
});

// 요청 인터셉터
axiosInstance.interceptors.request.use(
  (config) => {
    const userStore = useUserStore();
    if (userStore.isLoggedIn && userStore.token) {
      config.headers["Authorization"] = `Bearer ${userStore.token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 응답 인터셉터
axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    const userStore = useUserStore();
    if (error.response && error.response.status === 401) {
      // 로그아웃 처리 또는 리다이렉트
      userStore.logout();
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
