<template>
  <div class="map-size main">
    <div class="select-container">
      <div>
        <div class="select-box">
          <!-- 도/시 선택 -->
          <label for="province">도/시 선택</label>
          <select
            class="custom-select"
            id="province"
            v-model="province"
            @change="updateCities"
          >
            <option value="" disabled>선택하세요</option>
            <option v-for="prov in provinces" :key="prov" :value="prov">
              {{ prov }}
            </option>
          </select>
        </div>
        <div class="select-box">
          <!-- 시/군/구 선택 -->
          <label for="city">시/군/구 선택</label>
          <select class="custom-select" id="city" v-model="city">
            <option value="" disabled>선택하세요</option>
            <option v-for="ct in cities" :key="ct" :value="ct">{{ ct }}</option>
          </select>
        </div>
        <div class="select-box">
          <!-- 은행 선택 -->
          <label for="bank">은행 선택</label>
          <select class="custom-select" id="bank" v-model="bank">
            <option value="" disabled>선택하세요</option>
            <option v-for="bnk in banks" :key="bnk" :value="bnk">
              {{ bnk }}
            </option>
          </select>
        </div>
      </div>
      <div class="map-button-container">
        <button @click="searchOnMap">검색하기</button>
        <button @click="getCurrentLocation">내 주변 은행</button>
      </div>
    </div>

    <!-- 지도 출력 Component 연결, 선택된 데이터 전달 -->
    <MapSearch ref="mapSearch" :province="province" :city="city" :bank="bank" />
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
const mapSearch = ref(null);

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

const searchOnMap = () => {
  if (mapSearch.value) {
    mapSearch.value.searchOnMap();
  }
};

const getCurrentLocation = () => {
  if (mapSearch.value) {
    mapSearch.value.getCurrentLocation();
  }
};

watch(province, () => {
  updateCities();
});
</script>

<style scoped>
.map-size {
  display: flex;
  align-items: center;
}
.select-container {
  margin-top: 1rem;
  flex-grow: 0;
  text-align: left;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.select-container label {
  font-weight: var(--font-weight-medium);
}

.select-box {
  display: flex;
  flex-direction: column;
  margin-bottom: 2rem;
  gap: 0.3rem;
}

.map-button-container {
  margin: 1rem 0.5rem;
  display: flex;
}

.map-button-container button {
  display: block;
  margin: 1rem 0 1rem 1rem;
  background-color: var(--color-black);
  color: var(--color-white);
  padding: 0.5rem 1rem;
  border-radius: 5px;
  width: 10rem;
}
</style>
