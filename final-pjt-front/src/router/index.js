import App from "@/App.vue";
import ArticleCreate from "@/components/Community/ArticleCreate.vue";
import ArticleDetail from "@/components/Community/ArticleDetail.vue";
import ExchangeCalculate from "@/components/ExchangeRate/ExchangeCalculate.vue";
import ExchangeRateList from "@/components/ExchangeRate/ExchangeRateList.vue";
import ProductDetail from "@/components/Product/ProductDetail.vue";
import ProductUpdate from "@/components/Product/ProductUpdate.vue";
import Recommend from "@/components/Product/RecommendList.vue";
import ChangePassword from "@/components/Profile/ChangePassword.vue";
import MyProductList from "@/components/Profile/MyProductList.vue";
import MyProfile from "@/components/Profile/MyProfile.vue";
import PasswordVerification from "@/components/Profile/PasswordVerification.vue";
import { useUserStore } from "@/stores/user";
import LoginView from "@/views/LoginView.vue";
import MainView from "@/views/MainView.vue";
import ProfileView from "@/views/ProfileView.vue";
import SignupView from "@/views/SignupView.vue";
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: MainView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/signup",
      name: "signup",
      component: SignupView,
    },
    {
      path: "/profile",
      name: "profile",
      component: ProfileView,
      meta: { requiresAuth: true },
      children: [
        {
          path: "profile/my_info",
          name: "my_profile",
          component: MyProfile,
        },
        {
          path: "/profile/my_products",
          name: "my_products",
          component: MyProductList,
        },
        {
          path: "/profile/password-verification",
          name: "password_verification",
          component: PasswordVerification,
        },
        {
          path: "/profile/change_password",
          name: "change_password",
          component: ChangePassword,
        },
      ],
    },
    {
      path: "/exchange-rate",
      name: "exchange_rate",
      component: () => import("@/views/ExchangeRateView.vue"),
      children: [
        {
          path: "/exchange-rate",
          name: "exchange_rate_home",
          component: ExchangeRateList,
        },
        {
          path: "/exchange-rate/calculate",
          name: "exchange-rate_calcuate",
          component: ExchangeCalculate,
        },
      ],
    },
    {
      path: "/search-bank",
      name: "search_bank",
      component: () => import("@/views/MapView.vue"),
    },
    {
      path: "/community",
      name: "community",
      component: () => import("@/views/CommunityView.vue"),
    },
    {
      path: "/community/create",
      name: "create_article",
      component: ArticleCreate,
    },
    {
      path: "/community/:article_id",
      name: "article_detail",
      component: ArticleDetail,
    },
    {
      path: "/products",
      name: "products",
      component: () => import("@/views/ProductView.vue"),
      children: [
        {
          path: "/products/deposits",
          name: "product_deposits",
          component: () => import("@/components/Product/DepositList.vue"),
        },
        {
          path: "/products/savings",
          name: "product_savings",
          component: () => import("@/components/Product/SavingList.vue"),
        },
        {
          path: "/products/:product_id",
          name: "product_detail",
          component: ProductDetail,
        },
        {
          path: "/products/recommend",
          name: "product_recommend",
          component: Recommend,
          meta: { requiresAuth: true }, // 인증 필요 페이지
        },
        {
          path: "/products/:product_id/:option_id/edit",
          name: "product_edit",
          component: ProductUpdate,
        },
      ],
    },
    {
      path: "/qna",
      name: "qna",
      component: () => import("@/views/QnAView.vue"),
    },
  ],
});

// router.beforeEach((to, from, next) => {
//   const userStore = useUserStore();

//   if (!userStore.isLoggedIn && to.meta.requiresAuth) {
//     const confirmed = window.confirm(
//       "로그인이 필요한 페이지입니다. 로그인하시겠습니까?"
//     );
//     if (confirmed) {
//       return next({ name: "login" });
//     }
//     return;
//   }

//   if ((userStore.isLoggedIn && to.path === "/login") || to.path === "signup") {
//     return next({ path: "/" });
//   }

//   next();
// });

export default router;
