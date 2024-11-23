import axios from "axios";
import { defineStore } from "pinia";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

export const useUserStore = defineStore("user", () => {
  const isLoggedIn = ref(false);
  const token = ref(null);
  const userEmail = ref(null);
  const username = ref(null);
  const router = useRouter();

  onMounted(() => {
    const storedIsLoggedIn = JSON.parse(sessionStorage.getItem("isLoggedIn"));
    const storedToken = JSON.parse(sessionStorage.getItem("userToken"));
    const storedEmail = JSON.parse(sessionStorage.getItem("userEmail"));
    const storedUsername = JSON.parse(sessionStorage.getItem("username"));

    console.log(storedEmail);
    if (storedIsLoggedIn && storedToken) {
      isLoggedIn.value = true;
      token.value = storedToken;
      userEmail.value = storedEmail;
      username.value = storedUsername;
    }
  });

  const signup = async (data) => {
    const username = data.username;
    const email = data.email;
    const password1 = data.password1;
    const password2 = data.password2;

    try {
      const response = await axios({
        method: "post",
        url: `${import.meta.env.VITE_BASE_URL}/accounts/signup/`,
        data: {
          username,
          email,
          password1,
          password2,
        },
      });

      // console.log(response);
      if (response.status === 201) {
        const userData = data;
        userData.userToken = response.data.key;

        // console.log(userData);
        login(userData);
      }
    } catch (error) {
      console.error(error);
      return error.response ? error.response.data : "알 수 없는 오류가 발생했습니다.";
    }
  };

  const login = async (data) => {
    try {
      const response = await axios({
        method: "post",
        url: `${import.meta.env.VITE_BASE_URL}/accounts/login/`,
        data: {
          email: data.email,
          password: data.password ? data.password : data.password1,
        },
      });

      // console.log(response);

      userEmail.value = data.email;
      token.value = response.data.key;
      username.value = response.data.username;
      isLoggedIn.value = true;

      sessionStorage.setItem("userToken", JSON.stringify(token.value));
      sessionStorage.setItem("isLoggedIn", JSON.stringify(isLoggedIn.value));
      sessionStorage.setItem("userEmail", JSON.stringify(userEmail.value));
      sessionStorage.setItem("username", JSON.stringify(username.value));

      router.push({ name: "home" });
    } catch (error) {
      console.error(error);
      return error.response;
    }
  };

  const logout = () => {
    token.value = null;
    userEmail.value = null;
    username.value = null;
    isLoggedIn.value = false;

    sessionStorage.removeItem("userToken");
    sessionStorage.removeItem("isLoggedIn");
    sessionStorage.removeItem("userEmail");
    sessionStorage.removeItem("username");
  };

  return { isLoggedIn, token, login, logout, signup, username, userEmail };
});
