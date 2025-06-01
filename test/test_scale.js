import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  vus: 50, // 模擬 50 個虛擬用戶
  duration: '30s', // 測試持續 30 秒
  rps: 50, // 每秒發送 50 次請求
};

export default function () {
  http.get('http://localhost:80/'); // 將這行替換為您的目標 URL
  sleep(1); // 每個虛擬用戶之間的間隔
}
