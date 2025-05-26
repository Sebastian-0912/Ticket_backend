# /arenas routes

---

### **Create Arena**

<details>
<summary><code>POST</code> <code><b>/</b></code> <code>(Create a new arena)</code></summary>

##### Headers

| key             | required | data type | description             |
| --------------- | -------- | --------- | ----------------------- |
| `Authorization` | true     | string    | Bearer token from login |


##### Body (application/json)

| key        | required | data type | description         |
| ---------- | -------- | --------- | ------------------- |
| `title`    | true     | string    | Name of the arena   |
| `address`  | true     | string    | Arena's address     |
| `capacity` | true     | integer   | Max number of seats |

##### Responses

| http code | content-type       | response                                                             |
| --------- | ------------------ | -------------------------------------------------------------------- |
| `201`     | `application/json` | `{"id": "uuid", "title": "...", "address": "...", "capacity": 1000}` |
| `400`     | `text/plain`       | `Invalid data`                                                       |
| `500`     | `text/plain`       | `Internal server error`                                              |

</details>

---

### **Get All Arenas**

<details>
<summary><code>GET</code> <code><b>/</b></code> <code>(List all arenas)</code></summary>

##### Responses

| http code | content-type       | response                                                                   |
| --------- | ------------------ | -------------------------------------------------------------------------- |
| `200`     | `application/json` | `[{"id": "...", "title": "...", "address": "...", "capacity": 1000}, ...]` |
| `500`     | `text/plain`       | `Internal server error`                                                    |

</details>

---

### **Get Arena By ID**

<details>
<summary><code>GET</code> <code><b>/&lt;arena_id&gt;</b></code> <code>(Get a specific arena)</code></summary>

##### Responses

| http code | content-type       | response                                                            |
| --------- | ------------------ | ------------------------------------------------------------------- |
| `200`     | `application/json` | `{"id": "...", "title": "...", "address": "...", "capacity": 1000}` |
| `404`     | `text/plain`       | `Arena not found`                                                   |
| `500`     | `text/plain`       | `Internal server error`                                             |

</details>

<!-- --- -->

<!-- ### **Update Arena**

<details>
<summary><code>PUT</code> <code><b>/arenas/&lt;arena_id&gt;</b></code> <code>(Update arena info)</code></summary>

##### Body (application/json)

| key        | required | data type | description              |
| ---------- | -------- | --------- | ------------------------ |
| `title`    | false    | string    | Updated title            |
| `address`  | false    | string    | Updated address          |
| `capacity` | false    | integer   | Updated seating capacity |

##### Responses

| http code | content-type       | response                                    |
| --------- | ------------------ | ------------------------------------------- |
| `200`     | `application/json` | `{"message": "Arena updated successfully"}` |
| `404`     | `text/plain`       | `Arena not found`                           |
| `500`     | `text/plain`       | `Internal server error`                     |

</details>

---

### **Delete Arena**

<details>
<summary><code>DELETE</code> <code><b>/arenas/&lt;arena_id&gt;</b></code> <code>(Delete an arena)</code></summary>

##### Responses

| http code | content-type | response                |
| --------- | ------------ | ----------------------- |
| `204`     | `text/plain` | No content              |
| `404`     | `text/plain` | `Arena not found`       |
| `500`     | `text/plain` | `Internal server error` |

</details> -->
