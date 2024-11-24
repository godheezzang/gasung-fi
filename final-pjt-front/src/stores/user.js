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
  const isStaff = ref(false);
  const userProducts = ref([]);
  const password = ref(null);
  const gender = ref(null);
  const income = ref(null);
  const assets = ref(null);

  onMounted(() => {
    const storedIsLoggedIn = JSON.parse(sessionStorage.getItem("isLoggedIn"));
    const storedToken = JSON.parse(sessionStorage.getItem("userToken"));
    const storedEmail = JSON.parse(sessionStorage.getItem("userEmail"));
    const storedUsername = JSON.parse(sessionStorage.getItem("username"));
    const storedIsStaff = JSON.parse(sessionStorage.getItem("isStaff"));
    const storedUserProducts = JSON.parse(sessionStorage.getItem("userProducts"));
    const storedUserGender = JSON.parse(sessionStorage.getItem("userGender"));
    const storedUserIncome = JSON.parse(sessionStorage.getItem("userIncome"));
    const storedUserAssets = JSON.parse(sessionStorage.getItem("userAssets"));

    // console.log(storedIsStaff);

    // console.log(storedEmail);
    if (storedIsLoggedIn && storedToken) {
      isLoggedIn.value = true;
      token.value = storedToken;
      userEmail.value = storedEmail;
      username.value = storedUsername;
      isStaff.value = storedIsStaff;
      userProducts.value = storedUserProducts;
      gender.value = storedUserGender;
      income.value = storedUserIncome;
      assets.value = storedUserAssets;
      // console.log(isStaff.value);
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

      if (response.status === 201) {
        const userData = data;
        userData.userToken = response.data.key;

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

      // console.log(response.data);

      userEmail.value = data.email;
      token.value = response.data.key;
      username.value = response.data.username;
      isLoggedIn.value = true;
      isStaff.value = response.data.is_staff;
      userProducts.value = response.data.user_products;
      password.value = data.password ? data.password : data.password1;

      sessionStorage.setItem("userToken", JSON.stringify(token.value));
      sessionStorage.setItem("isLoggedIn", JSON.stringify(isLoggedIn.value));
      sessionStorage.setItem("userEmail", JSON.stringify(userEmail.value));
      sessionStorage.setItem("username", JSON.stringify(username.value));
      sessionStorage.setItem("isStaff", JSON.stringify(isStaff.value));
      sessionStorage.setItem("userProducts", JSON.stringify(userProducts.value));

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
    isStaff.value = null;
    isLoggedIn.value = false;

    sessionStorage.removeItem("userToken");
    sessionStorage.removeItem("isLoggedIn");
    sessionStorage.removeItem("userEmail");
    sessionStorage.removeItem("username");
    sessionStorage.removeItem("isStaff");

    router.push({ name: "home" });
  };

  const getUserProducts = async () => {
    try {
      const response = await axios({
        method: "get",
        url: `${import.meta.env.VITE_BASE_URL}/accounts/detail/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });

      // console.log(response.data.user_products);
      userProducts.value = response.data.user_products;
      sessionStorage.setItem("userProducts", JSON.stringify(userProducts.value));
    } catch (error) {
      console.error(error);
    }
  };

  const getUserInfo = async () => {
    try {
      const response = await axios({
        method: "get",
        url: `${import.meta.env.VITE_BASE_URL}/accounts/detail/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });

      console.log(response.data);
      gender.value = response.data.gender;
      income.value = response.data.income;
      assets.value = response.data.assets;

      sessionStorage.setItem("userGender", JSON.stringify(gender.value));
      sessionStorage.setItem("userIncome", JSON.stringify(income.value));
      sessionStorage.setItem("userAssets", JSON.stringify(assets.value));
    } catch (error) {
      console.error(error);
    }
  };

  return { isLoggedIn, token, login, logout, signup, username, userEmail, isStaff, userProducts, getUserProducts, password, getUserInfo, gender, income, assets };
});
