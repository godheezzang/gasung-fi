<template>
  <div class="modal" v-if="isVisible">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <p class="modal-title">{{ productDetail.fin_prdt_nm }}</p>
      <!-- 그래프 관련 내용 -->
      <div class="chart-container" v-if="options.length">
        <BarChart :chartData="chartData" :chartOptions="chartOptions" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, defineProps, ref } from "vue";
import { BarChart } from "vue-chart-3";
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, BarController } from "chart.js";

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, BarController);

// props 정의
const props = defineProps({
  productDetail: {
    type: Object,
    required: true,
  },
  isVisible: {
    type: Boolean,
    required: true,
  },
  closeModal: {
    type: Function,
    required: true,
  },
});

// options computed property
const options = computed(() => {
  return Array.isArray(props.productDetail?.options) ? props.productDetail.options : [];
});

// 평균 금리 계산
const averageRate = computed(() => {
  if (options.value.length === 0) return 0; // options가 비어있으면 0 반환
  const sum = options.value.reduce((acc, option) => acc + option.intr_rate, 0);
  return (sum / options.value.length).toFixed(2); // 소수점 두 자리로 제한
});

const averageBestRate = computed(() => {
  if (options.value.length === 0) return 0; // options가 비어있으면 0 반환
  const sum = options.value.reduce((acc, option) => acc + option.intr_rate2, 0);
  return (sum / options.value.length).toFixed(2); // 소수점 두 자리로 제한
});

// 차트 데이터
const chartData = computed(() => ({
  labels: [
    "평균 금리",
    ...options.value.map((option) => {
      // 조건에 따라 레이블 생성
      if (option.rsrv_type_nm) {
        return option.rsrv_type_nm === "정액적립식" ? `${option.save_trm}개월 (${option.rsrv_type_nm})` : `${option.save_trm}개월 (${option.rsrv_type_nm})`;
      } else {
        return `${option.save_trm}개월`;
      }
    }),
  ],
  datasets: [
    {
      label: "저축 금리",
      data: [averageRate.value, ...options.value.map((option) => option.intr_rate)],
      backgroundColor: "rgba(75, 192, 192, 0.6)",
    },
    {
      label: "최고 우대금리",
      data: [averageBestRate.value, ...options.value.map((option) => option.intr_rate2)],
      backgroundColor: "rgba(153, 102, 255, 0.6)",
    },
  ],
}));

// 차트 옵션
const chartOptions = ref({
  responsive: true,
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: "금리 (%)",
      },
    },
    x: {
      title: {
        display: true,
        text: "저축 기간 (개월)",
      },
    },
  },
});
</script>

<style scoped>
.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  background-color: var(--color-white);
  padding: 2rem;
  border-radius: 5px;
  box-sizing: border-box;
  width: 50rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.modal-title {
  font-size: var(--font-size-mlarge);
  font-weight: var(--font-weight-medium);
  text-align: center;
  margin-bottom: 2rem;
}

.close {
  cursor: pointer;
  position: absolute; /* 절대 위치 설정 */
  top: 1.5rem; /* 상단 여백 */
  right: 2rem; /* 오른쪽 여백 */
  font-size: var(--font-size-large); /* 크기 조정 */
  display: inline-block;
  width: 3rem;
  height: 3rem;
  text-align: center;
}

.close:hover {
  background-color: var(--color-gray-01);
  border-radius: 10px;
}

.chart-container {
  display: flex;
  justify-content: center; /* 수평 가운데 정렬 */
  align-items: center; /* 수직 가운데 정렬 */
  width: 100%; /* 전체 너비 사용 */
  margin-top: 1rem; /* 차트와 제목 사이의 여백 */
}
</style>
