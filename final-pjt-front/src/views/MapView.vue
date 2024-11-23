<template>
  <div class="map-size">
    <div>
      <!-- 도/시 선택 -->
      <label for="province">도/시:</label>
      <select id="province" v-model="province" @change="updateCities">
        <option value="" disabled>선택하세요</option>
        <option v-for="prov in provinces" :key="prov" :value="prov">{{ prov }}</option>
      </select>
    </div>
    <div>
      <!-- 시/군/구 선택 -->
      <label for="city">시/군/구:</label>
      <select id="city" v-model="city">
        <option value="" disabled>선택하세요</option>
        <option v-for="ct in cities" :key="ct" :value="ct">{{ ct }}</option>
      </select>
    </div>
    <div>
      <!-- 은행 선택 -->
      <label for="bank">은행:</label>
      <select id="bank" v-model="bank">
        <option value="" disabled>선택하세요</option>
        <option v-for="bnk in banks" :key="bnk" :value="bnk">{{ bnk }}</option>
      </select>
    </div>
    <!-- 지도 출력 Component 연결, 선택된 데이터 전달 -->
    <MapSearch :province="province" :city="city" :bank="bank" />
  </div>
</template>

<script setup>
import { ref, watch, computed } from "vue";
import { useMapStore } from "@/stores/map";
import MapSearch from "@/components/SearchBank/MapSearch.vue";

const store = useMapStore();

const infos = store.infos;
const banks = store.banks;
const cities = ref([]);
const selectLocation = ref("");

// 도/시 목록
const provinces = computed(() => infos.map((info) => info.prov));

// 도/시
const province = ref("선택해주세요");
// 시/군/구
const city = ref("선택해주세요");
// 은행
const bank = ref("선택해주세요");

// 조건에 맞는 데이터 호출 -> cities에 할당
const updateCities = () => {
  const selectedInfo = infos.find((info) => info.prov === province.value);
  cities.value = selectedInfo ? selectedInfo.city : [];
};

watch(province, () => {
  updateCities();
});
</script>
