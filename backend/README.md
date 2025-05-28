# Instruction

## Schema
![Architecture](./asset/Distributed%20system.png)


## 文件說明

### api_doc folder

定義 route 文件

### crud folder

DB logic

### routes folder

Route implement

### db folder

存放連接 db 的相關設定，勿動

### Models folder

定義每個 table 的樣子

### schemas folder

定義狀態角色等等東西

### main.py

執行建立表格 create table 的動作，先 users/ arenas 再 activities -> arena_taken -> ticket，建立活動時會自動建立 arena_taken 和 ticket

### modify.py

執行修改的動作，如買票後更新 ticket.user_id, ticket.status，以及付款後更新 ticket.status

## 測試指令（開發測試）

**Create table**：

```bash
curl -X POST http://localhost:80/dev/create_all
```

**If want to delete table**：

```bash
curl -X DELETE http://localhost:80/dev/drop_all
```

**Register (host)**：

```bash
curl -X POST http://localhost:80/auth/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "host@example.com",
    "password": "123456",
    "username": "host",
    "role": "host",
    "phone_number": "0912345678"
}'

```

**Register (client)**：

```bash
curl -X POST http://localhost:80/auth/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "client@example.com",
    "password": "123456",
    "username": "client",
    "role": "client",
    "phone_number": "0912345622"
}'

```

**Login**：

```bash
curl -X POST http://localhost:80/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "host@example.com",
    "password": "123456"
}'

```

**Get User Info**:

```bash
curl -X GET http://localhost:80/auth/get_user_info \
  -H "Authorization: Bearer [YOUR_ACCESS_TOKEN]"

```

[YOUR_ACCESS_TOKEN] 要改成 login 回傳的

**Update User Info**:

```bash
curl -X PUT http://localhost:80/auth/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer [YOUR_ACCESS_TOKEN]" \
  -d '{
    "username": "updateduser",
    "phone_number": "0987654321"
}'

```

[YOUR_ACCESS_TOKEN] 要改成 login 回傳的

**Create Arena**:

```bash
curl -X POST http://localhost:80/arenas/ \
  -H "Authorization: Bearer [YOUR_TOKEN_HERE]" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Main Sports Hall",
    "address": "123 Arena Street",
    "capacity": 2000
  }'

```

[YOUR_ACCESS_TOKEN] 要改成 login 回傳的

**Get All Arenas**:

```bash
curl http://localhost:80/arenas/

```

**Get Arena by ID**:

```bash
curl http://localhost:80/arenas/<arena_id>

```
**Create Activity**:

```bash
curl -X POST http://localhost:80/activities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer [YOUR_ACCESS_TOKEN]" \
  -d '{
    "title": "Chou",
    "content": "Chou",
    "price": 1000,
    "on_sale_date": "2025-06-01T00:00:00",
    "start_time": "2025-06-09T17:00:00",
    "end_time": "2025-06-09T19:00:00",
    "cover_image": "https://example.com/image.jpg",
    "arena_id": "[YOUR_ARENA_ID]"
  }'

```

[YOUR_ACCESS_TOKEN] 要改成 login 回傳的\
[YOUR_ARENA_ID] 要改成 Create Arena 回傳的

**Get All Activities**:

```bash
curl -X GET http://localhost:80/activities/

```

**Get Activity By ID**:

```bash
curl -X GET http://localhost:80/activities/[YOUR_ACTIVITY_ID]
```
[YOUR_ACTIVITY_ID] 要改成 Create Activity 回傳的


**Update Activity**:

```bash
curl -X PUT http://localhost:80/activities/[YOUR_ACTIVITY_ID] \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer [YOUR_ACCESS_TOKEN]" \
  -d '{
    "title": "New Event Title",
    "content": "Updated content of the event.",
    "price": 250,
    "on_sale_date": "2025-06-01T10:00:00",
    "start_time": "2025-06-15T14:00:00",
    "end_time": "2025-06-15T18:00:00",
    "cover_image": "https://example.com/new-cover.jpg"
  }'


```
[YOUR_ACCESS_TOKEN] 要改成 login 回傳的\
[YOUR_ACTIVITY_ID] 要改成 Create Activity 回傳的
