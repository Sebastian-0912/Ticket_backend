# /auth routes

---

### **Register a New User**

<details>
<summary><code>POST</code> <code><b>/</b></code> <code>(Register a new user)</code></summary>

##### Body (application/json)

| key            | required | data type | description           |
| -------------- | -------- | --------- | --------------------- |
| `email`        | true     | string    | User's email          |
| `password`     | true     | string    | User's password       |
| `username`     | true     | string    | User's name           |
| `role`         | true     | string    | `"user"` or `"admin"` |
| `phone_number` | true     | string    | User's phone number   |

##### Responses

| http code | content-type       | response                                                                             |
| --------- | ------------------ | ------------------------------------------------------------------------------------ |
| `201`     | `application/json` | `{"id": "uuid", "email": "x", "username": "x", "role": "user", "phone_number": "x"}` |
| `409`     | `text/plain`       | `Email or username already exists`                                                   |
| `500`     | `text/plain`       | `Internal server error`                                                              |

</details>

---

### **Login**

<details>
<summary><code>POST</code> <code><b>/login</b></code> <code>(Login and get JWT token)</code></summary>

##### Body (application/json)

| key        | required | data type | description     |
| ---------- | -------- | --------- | --------------- |
| `email`    | true     | string    | User's email    |
| `password` | true     | string    | User's password |

##### Responses

| http code | content-type       | response                                                |
| --------- | ------------------ | ------------------------------------------------------- |
| `200`     | `application/json` | `{"access_token": "jwt-token", "token_type": "bearer"}` |
| `401`     | `text/plain`       | `Invalid credentials`                                   |
| `500`     | `text/plain`       | `Internal server error`                                 |

</details>

---

### **Get My User Info**

<details>
<summary><code>GET</code> <code><b>/get_user_info</b></code> <code>(Get current user's info)</code></summary>

##### Headers

| key             | required | data type | description             |
| --------------- | -------- | --------- | ----------------------- |
| `Authorization` | true     | string    | Bearer token from login |

##### Responses

| http code | content-type       | response                                                                             |
| --------- | ------------------ | ------------------------------------------------------------------------------------ |
| `200`     | `application/json` | `{"id": "uuid", "email": "x", "username": "x", "role": "user", "phone_number": "x"}` |
| `401`     | `text/plain`       | `Unauthorized`                                                                       |
| `500`     | `text/plain`       | `Internal server error`                                                              |

</details>

---

### **Update My Info**

<details>
<summary><code>PUT</code> <code><b>/</b></code> <code>(Update user info)</code></summary>

##### Headers

| key             | required | data type | description             |
| --------------- | -------- | --------- | ----------------------- |
| `Authorization` | true     | string    | Bearer token from login |

##### Body (application/json)

| key            | required | data type | description             |
| -------------- | -------- | --------- | ----------------------- |
| `username`     | false    | string    | Updated username        |
| `phone_number` | false    | string    | Updated phone number    |
| `role`         | false    | string    | Admin-only: change role |

##### Responses

| http code | content-type       | response                                   |
| --------- | ------------------ | ------------------------------------------ |
| `200`     | `application/json` | `{"message": "User updated successfully"}` |
| `403`     | `text/plain`       | `Forbidden`                                |
| `404`     | `text/plain`       | `User not found`                           |
| `500`     | `text/plain`       | `Internal server error`                    |

</details>
