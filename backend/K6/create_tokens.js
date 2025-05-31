const axios = require("axios");
const fs = require("fs");

const BASE_URL = "http://localhost:80/auth";
const PASSWORD = "12345678";
const COUNT = 10;

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
      userId = res.data.id;  // 註冊 API 回傳的 user_id
      registeredUsers.push({ email, userId });
      console.log(`Registered: ${email} with id: ${userId}`);
    } catch (e) {
      if (e.response?.status === 409) {
        console.log(`User already exists: ${email}`);
        // 你可在此嘗試用其他方法拿到 userId (例如查資料庫或其他API)，
        // 目前先略過
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
