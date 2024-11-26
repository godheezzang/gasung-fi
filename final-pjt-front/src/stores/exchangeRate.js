import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useRateStore = defineStore("rate", () => {
  const rates = ref(null);
  const formattedRates = ref([]);
  const BASE_URL = import.meta.env.VITE_BASE_URL;

  const getRate = async () => {
    try {
      const response = await axios({
        method: "get",
        url: `${BASE_URL}/exchange_rate/get_exchange_rates/`,
      });

      rates.value = response?.data;

      formattedRates.value = rates.value.map((rate) => {
        const [country, currency] = rate.cur_nm.split(" ");
        const money = currency || rate.cur_nm;
        const countryName = countryMapping[rate.cur_unit] || country;

        return {
          ...rate, // 기존의 모든 데이터를 포함
          country: countryName, // 나라 이름 추가
          money: money, // 통화 이름 추가
        };
      });
    } catch (error) {
      console.error(error);
    }
  };

  const countryMapping = {
    AED: "아랍에미리트",
    AUD: "호주",
    BHD: "바레인",
    BND: "브루나이",
    CAD: "캐나다",
    CHF: "스위스",
    CNH: "중국",
    DKK: "덴마크",
    EUR: "유럽연합",
    GBP: "영국",
    HKD: "홍콩",
    "IDR(100)": "인도네시아",
    "JPY(100)": "일본",
    KRW: "한국",
    KWD: "쿠웨이트",
    MYR: "말레이시아",
    NOK: "노르웨이",
    NZD: "뉴질랜드",
    SAR: "사우디아라비아",
    SEK: "스웨덴",
    SGD: "싱가포르",
    THB: "태국",
    USD: "미국",
  };

  return { rates, getRate, formattedRates };
});
