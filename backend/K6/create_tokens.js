const axios = require("axios");
const fs = require("fs");

const BASE_URL = "http://localhost:80/auth";
const PASSWORD = "12345678";
const COUNT = 800;

async function main() {
  const tokens = [];
  const registeredUsers = []; // 存 email 與 user_id

  for (let i = 1; i <= COUNT; i++) {
    const email = `user${i}@test.com`;
    const username = `user${i}`;
    const payload = {
      email,
      password: PASSWORD,
      username,
      role: "user",
      phone_number: `09${Math.floor(100000000 + Math.random() * 900000000)}`,
    };

    let userId = null;
    try {
        const res = await axios.post(`${BASE_URL}/`, payload); // 註冊
        userId = res.data.id;  // 註冊成功就拿id
        registeredUsers.push({ email, userId });
        console.log(`Registered: ${email} with id: ${userId}`);
    } catch (e) {
        if (e.response?.status === 409) {
            console.log(`User already exists: ${email}`);
            // 已存在時用登入拿token，接著呼叫 get_user_info 拿 user_id
            try {
                const loginRes = await axios.post(`${BASE_URL}/login`, {
                    email,
                    password: PASSWORD,
                });
                const token = loginRes.data.access_token;
                // 用 token 呼叫 get_user_info 拿 user資料
                const userInfoRes = await axios.get(`${BASE_URL}/get_user_info`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                userId = userInfoRes.data.id;
                registeredUsers.push({ email, userId });
                tokens.push({ token, user_id: userId });
                console.log(`Fetched user_id for existing user: ${email} id: ${userId}`);
                continue;  // 跳過後面登入流程，因為token已存
            } catch (err) {
                console.error(`Failed to get user info for ${email}`, err.message);
                continue;
            }
        } else {
            console.error(`Register failed for ${email}`, e.message);
            continue;
        }
    }


    try {
      const res = await axios.post(`${BASE_URL}/login`, {
        email,
        password: PASSWORD,
      });

      const token = res.data.access_token;
      // 找剛剛存的 userId
      const user = registeredUsers.find(u => u.email === email);
      const id = user ? user.userId : "unknown-user-id";

      tokens.push({
        token,
        user_id: id,
      });

      console.log(`Logged in: ${email}`);
    } catch (e) {
      console.error(`Login failed for ${email}`, e.message);
    }
  }

  fs.writeFileSync("tokens.json", JSON.stringify(tokens, null, 2));
  console.log(`Saved ${tokens.length} tokens to tokens.json`);
}

main();
