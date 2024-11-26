import { defineStore } from "pinia";
import { ref } from "vue";

// 이미지 파일을 직접 가져오기
import KBImage from "@/assets/images/금융아이콘_SVG_KB.svg";
import NonghyupImage from "@/assets/images/금융아이콘_SVG_농협.svg";
import WooriImage from "@/assets/images/금융아이콘_SVG_우리.svg";
import KDBImage from "@/assets/images/금융아이콘_SVG_KDB.svg";
import IBKImage from "@/assets/images/금융아이콘_SVG_IBK.svg";
import GwangjuImage from "@/assets/images/금융아이콘_SVG_광주.svg";
import PostOfficeImage from "@/assets/images/금융아이콘_SVG_우체국.svg";
import ShinhanImage from "@/assets/images/금융아이콘_SVG_신한.svg";
import SCImage from "@/assets/images/금융아이콘_SVG_SC제일.svg";
import JeonbukImage from "@/assets/images/전북은행.jpg";
import KEBHanaImage from "@/assets/images/금융아이콘_SVG_하나.svg";
import ShImage from "@/assets/images/금융아이콘_SVG_Sh수협.svg";
import BNKImage from "@/assets/images/금융아이콘_SVG_BNK.svg";
import MGImage from "@/assets/images/금융아이콘_SVG_MG새마을금고.svg";
import ShinheungImage from "@/assets/images/금융아이콘_SVG_신협.svg";
import CitiImage from "@/assets/images/금융아이콘_SVG_씨티.svg";
import DaeguImage from "@/assets/images/아이엠뱅크.jpg";
import JejuImage from "@/assets/images/제주은행.png";
import Toss from "@/assets/images/금융아이콘_SVG_토스.svg";
import Kakao from "@/assets/images/금융아이콘_SVG_카카오뱅크.svg";
import Kbank from "@/assets/images/금융아이콘_SVG_케이뱅크.svg";

export const useBankStore = defineStore("bank", () => {
  const bankImage = ref({
    국민은행: KBImage,
    농협은행주식회사: NonghyupImage,
    우리은행: WooriImage,
    산업은행: KDBImage,
    기업은행: IBKImage,
    광주은행: GwangjuImage,
    우체국: PostOfficeImage,
    신한은행: ShinhanImage,
    한국스탠다드차타드은행: SCImage,
    전북은행: JeonbukImage,
    하나은행: KEBHanaImage,
    수협은행: ShImage,
    경남은행: BNKImage,
    새마을금고: MGImage,
    신협은행: ShinheungImage,
    씨티은행: CitiImage,
    대구은행: DaeguImage,
    부산은행: BNKImage,
    중소기업은행: IBKImage,
    한국산업은행: KDBImage,
    제주은행: JejuImage,
    아이엠뱅크: DaeguImage,
    "주식회사 카카오뱅크": Kakao,
    "토스뱅크 주식회사": Toss,
    "주식회사 케이뱅크": Kbank,
  });

  return { bankImage };
});
