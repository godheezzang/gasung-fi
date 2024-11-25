<script setup>
import { onMounted, ref } from "vue";
import { KakaoMap, KakaoMapMarker } from "vue3-kakao-maps";

const props = defineProps({
  province: String,
  city: String,
  bank: String,
});

const coordinate = ref({
  lat: 33.450701,
  lng: 126.570667,
});

const map = ref(null);
const markerList = ref([]);
const searchKeyword = ref("");

const loadKakaoMap = function () {
  // Kakao 지도 API 스크립트 동적으로 추가
  const script = document.createElement("script");
  const KAKAO_KEY = import.meta.env.VITE_KAKAO_MAP_KEY; // APP KEY
  script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_KEY}&autoload=false&libraries=services`;
  script.async = true;
  script.onload = () => {
    // Kakao 지도 API 로드 완료 후 실행할 콜백 함수
    window.kakao.maps.load(function () {
      getCurrentLocation();
    });
  };

  document.head.appendChild(script);
};

const getCurrentLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        coordinate.value.lat = position.coords.latitude; // 사용자 위도
        coordinate.value.lng = position.coords.longitude; // 사용자 경도

        onLoadKakaoMap(map.value);
      },
      (error) => {
        console.error("Geolocation error:", error);
      }
    );
  }
};

const onLoadKakaoMap = (mapRef) => {
  map.value = mapRef;

  const ps = new kakao.maps.services.Places();
  const level = map.value.getLevel();

  // 범위조정
  const radius = 650;

  ps.categorySearch("BK9", placesSearchCB, {
    location: new kakao.maps.LatLng(coordinate.value.lat, coordinate.value.lng),
    radius: radius,
  });
  // console.log(coordinate.value.lat);
  // console.log(coordinate.value.lng);
  map.value.setLevel(level - 2);
};

const searchOnMap = () => {
  searchKeyword.value = `${props.province} ${props.city} ${props.bank}`;
  searchPlaces(searchKeyword.value);
  // 상품 검색 함수 실행
};

const searchPlaces = (keyword) => {
  const ps = new kakao.maps.services.Places();
  ps.keywordSearch(keyword, placesSearchCB);
};

const removeAllMarkers = () => {
  for (let i = 0; i < markerList.value.length; i++) {
    // markerList.value[i].setMap(null);
    // console.log(markerList.value[i]);
  }

  markerList.value = [];
};

const placesSearchCB = (data, status) => {
  if (status === kakao.maps.services.Status.OK) {
    removeAllMarkers();

    const bounds = new kakao.maps.LatLngBounds();

    for (let marker of data) {
      const markerItem = {
        lat: marker.y,
        lng: marker.x,
        infoWindow: {
          content: marker.place_name,
          visible: false,
        },
      };
      markerList.value.push(markerItem);
      bounds.extend(new kakao.maps.LatLng(Number(marker.y), Number(marker.x)));
    }

    map.value?.setBounds(bounds);
  }
};

const onClickMapMarker = (markerItem) => {
  if (
    markerItem.infoWindow?.visible !== null &&
    markerItem.infoWindow?.visible !== undefined
  ) {
    markerItem.infoWindow.visible = !markerItem.infoWindow.visible;
  } else {
    markerItem.infoWindow.visible = true;
  }
};

defineExpose({
  searchOnMap,
  getCurrentLocation,
});

onMounted(() => {
  loadKakaoMap();
});
</script>

<template>
  <div class="map-wrap">
    <div class="map-container">
      <KakaoMap
        :lat="coordinate.lat"
        :lng="coordinate.lng"
        @onLoadKakaoMap="onLoadKakaoMap"
      >
        <KakaoMapMarker
          v-for="(marker, index) in markerList"
          :key="marker.key === undefined ? index : marker.key"
          :lat="marker.lat"
          :lng="marker.lng"
          :infoWindow="marker.infoWindow"
          :clickable="true"
          @onClickKakaoMapMarker="onClickMapMarker(marker)"
        />
        <KakaoMapMarker
          :lat="coordinate.lat"
          :lng="coordinate.lng"
          title="my_place"
          :image="{
            imageSrc: 'https://cdn-icons-png.flaticon.com/512/6934/6934535.png',
            imageWidth: 50,
            imageHeight: 50,
          }"
        />
      </KakaoMap>
    </div>
  </div>
</template>

<style scoped>
.map-wrap {
  flex-grow: 1;
}
.map-container {
  margin: 0 auto;
  padding: 1rem;
}

.map-container div {
  width: 100% !important;
  border-radius: 10px;
  border: 1px solid var(--color-gray-03);
  height: 40rem !important;
}
</style>
