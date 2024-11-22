import App from "@/App.vue";
import ArticleCreate from "@/components/Community/ArticleCreate.vue";
import ArticleDetail from "@/components/Community/ArticleDetail.vue";
import ExchangeCalculate from "@/components/ExchangeRate/ExchangeCalculate.vue";
import ProductDetail from "@/components/Product/ProductDetail.vue";
import RecommendProduct from "@/components/Profile/RecommendProduct.vue";
import { useUserStore } from "@/stores/user";
import ExchangeRateView from "@/views/ExchangeRateView.vue";
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
      children: [
        {
          path: "/profile/my_products",
          name: "my_products",
          component: () => import("@/views/MyProductView.vue"),
        },
        {
          path: "/profile/recommend",
          name: "recommend_products",
          component: () => import("@/components/Profile/RecommendProduct.vue"),
        },
      ],
    },
    {
      path: "/exchange-rate",
      name: "exchange_rate",
      component: () => import("@/views/ExchangeRateView.vue"),
      children: [
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
      component: () => import("@/views/SearchBankView.vue"),
    },
    {
      path: "/community",
      name: "community",
      component: () => import("@/views/CommunityView.vue"),
    },
    {
      path: "/cummunity/create",
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
          path: "/products/:product_id",
          name: "product_detail",
          component: ProductDetail,
        },
      ],
    },
  ],
});

router.beforeEach((to, from, next) => {
  const userStore = useUserStore();

  if (!userStore.isLoggedIn && to.meta.requiresAuth) {
    return next({ name: "login" });
  }

  if ((userStore.isLoggedIn && to.path === "/login") || to.path === "signup") {
    return next({ path: "/" });
  }

  next();
});

export default router;
