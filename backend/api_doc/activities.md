# /activities routes

---

### **Create Activity**

<details>
<summary><code>POST</code> <code><b>/</b></code> <code>(Create a new activity)</code></summary>

##### Headers

| key             | required | data type | description             |
| --------------- | -------- | --------- | ----------------------- |
| `Authorization` | true     | string    | Bearer token from login |

##### Body (application/json)

| key            | required | data type | description          |
| -------------- | -------- | --------- | -------------------- |
| `title`        | true     | string    | Activity title       |
| `content`      | true     | string    | Optional description |
| `price`        | true     | string    | price                |
| `on_sale_date` | true     | string    | on_sale_date         |
| `start_time`   | true     | string    | start_time           |
| `end_time`     | true     | string    | end_time             |
| `cover_image`  | true     | string    | cover_image          |
| `arena_id`     | true     | string    | arena_id             |
| `creator_id`   | true     | string    | user_id of creator   |


##### Responses

| http code | content-type       | response                                             |
| --------- | ------------------ | ---------------------------------------------------- |
| `201`     | `application/json` | `{"id": "uuid", "title": "...", "time": "...", ...}` |
| `400`     | `text/plain`       | `Invalid data`                                       |
| `401`     | `text/plain`       | `Unauthorized`                                       |
| `500`     | `text/plain`       | `Internal server error`                              |

</details>

---

### **Get All Activities**

<details>
<summary><code>GET</code> <code><b>/</b></code> <code>(List all activities)</code></summary>

##### Responses

| http code | content-type       | response                                              |
| --------- | ------------------ | ----------------------------------------------------- |
| `200`     | `application/json` | `[{"id": "...", "title": "...", "time": "...", ...}]` |
| `500`     | `text/plain`       | `Internal server error`                               |

</details>

---

### **Get One Activity By ID**

<details>
<summary><code>GET</code> <code><b>/&lt;activity_id&gt;</b></code> <code>(Retrieve an activity)</code></summary>

##### Responses

| http code | content-type       | response                                                    |
| --------- | ------------------ | ----------------------------------------------------------- |
| `200`     | `application/json` | `{"id": "uuid", "title": "...", "description": "...", ...}` |
| `404`     | `text/plain`       | `Activity not found`                                        |
| `500`     | `text/plain`       | `Internal server error`                                     |

</details>

---

### **Update Activity**

<details>
<summary><code>PUT</code> <code><b>/&lt;activity_id&gt;</b></code> <code>(Update an activity)</code></summary>

##### Headers

| key             | required | data type | description             |
| --------------- | -------- | --------- | ----------------------- |
| `Authorization` | true     | string    | Bearer token from login |

##### Body (application/json)

| key            | required | data type | description          |
| -------------- | -------- | --------- | -------------------- |
| `title`        | false    | string    | Activity title       |
| `content`      | false    | string    | Optional description |
| `price`        | false    | string    | price                |
| `on_sale_date` | false    | string    | on_sale_date         |
| `start_time`   | false    | string    | start_time           |
| `end_time`     | false    | string    | end_time             |
| `cover_image`  | false    | string    | cover_image          |
| `arena_id`     | false    | string    | arena_id             |
| `creator_id`   | false    | string    | user_id of creator   |

##### Responses

| http code | content-type       | response                                       |
| --------- | ------------------ | ---------------------------------------------- |
| `200`     | `application/json` | `{"message": "Activity updated successfully"}` |
| `401`     | `text/plain`       | `Unauthorized`                                 |
| `404`     | `text/plain`       | `Activity not found`                           |
| `500`     | `text/plain`       | `Internal server error`                        |

</details>

<!-- ---

### **Delete Activity**

<details>
<summary><code>DELETE</code> <code><b>/&lt;activity_id&gt;</b></code> <code>(Delete an activity)</code></summary>

##### Headers

| key             | required | data type | description             |
| --------------- | -------- | --------- | ----------------------- |
| `Authorization` | true     | string    | Bearer token from login |

##### Responses

| http code | content-type | response                |
| --------- | ------------ | ----------------------- |
| `204`     | `text/plain` | No content              |
| `401`     | `text/plain` | `Unauthorized`          |
| `404`     | `text/plain` | `Activity not found`    |
| `500`     | `text/plain` | `Internal server error` |

</details> -->
