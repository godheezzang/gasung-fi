import { defineStore } from "pinia";
import { onMounted, ref } from "vue";

export const useUserStore = defineStore("user", () => {
  const user = ref(null);
  const isLoggedIn = ref(false);
  const token = ref(null);

  onMounted(() => {
    const storedIsLoggedIn = JSON.parse(sessionStorage.getItem("isLoggedIn"));
    const storedToken = JSON.parse(sessionStorage.getItem("userToken"));
    if (storedIsLoggedIn && storedToken) {
      isLoggedIn.value = true;
      token.value = storedToken;
    }
  });

  const login = (userData, userToken) => {
    user.value = userData;
    token.value = userToken;
    isLoggedIn.value = true;

    sessionStorage.setItem("userToken", JSON.stringify(token.value));
    sessionStorage.setItem("isLoggedIn", JSON.stringify(isLoggedIn.value));
  };

  const logout = () => {
    user.value = null;
    token.value = null;
    isLoggedIn.value = false;

    sessionStorage.removeItem("userToken");
    sessionStorage.removeItem("isLoggedIn");
  };

  return { user, isLoggedIn, token, login, logout };
});
