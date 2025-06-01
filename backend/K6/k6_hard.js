import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';

// 載入 tokens（已登入過的 500 隻帳號）
const users = new SharedArray('users', () =>
    JSON.parse(open('./tokens.json'))
);

export const options = {
    vus: 800,         // 虛擬使用者數量
    duration: '30s' // 測試時間
};

export default function () {
    sleep(__VU *0.1 + Math.random()* 0.1);
    const user = users[Math.floor(Math.random() * users.length)];

    const payload = JSON.stringify({
        user_id: user.user_id,
        activity_id: "2ab150d4-2bb4-481f-aedf-f1b7b6371209", // 替換成真實活動 ID
        num_tickets: Math.floor(Math.random() * 1) + 1
    });

    const headers = {
        Authorization: `Bearer ${user.token}`,
        'Content-Type': 'application/json',
    };

    const res = http.post('http://localhost:80/tickets/reserve', payload, { headers });

    // 用條件判斷不同狀況，分開 check

    if (res.status === 201) {
        check(res, { '搶票成功': (r) => true });
    } else if (res.status === 400) {
        const text = res.body;
        
        // 判斷售完的錯誤
        if (text === 'Tickets sold out or invalid data') {
            check(res, { '搶票失敗(該票已售出)': (r) => false });  // 故意 fail，但標記名稱區分
        } else {
            check(res, { '搶票失敗(其他400錯誤)': (r) => false });  // 例如參數錯
        }
    } else {
        check(res, { '伺服器錯誤(非400)' : (r) => false });  // 例如 500
    }




    sleep(1);
}
