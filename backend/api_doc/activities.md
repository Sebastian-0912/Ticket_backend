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

| key            | required | data type      | description          |
| -------------- | -------- | -------------- | -------------------- |
| `title`        | true     | string         | Activity title       |
| `content`      | true     | string         | Optional description |
| `price`        | true     | int            | price                |
| `on_sale_date` | true     | date.isoformat | on_sale_date         |
| `start_time`   | true     | date.isoformat | start_time           |
| `end_time`     | true     | date.isoformat | end_time             |
| `cover_image`  | true     | string (url)   | cover_image          |
| `arena_id`     | true     | string         | arena_id             |

<!-- | `creator_id`   | true     | string    | user_id of creator   | -->

##### Responses

| http code | content-type       | response                                             |
| --------- | ------------------ | ---------------------------------------------------- |
| `201`     | `application/json` | `{"id": "uuid", "title": "...", "time": "...", ...}` |
| `400`     | `text/plain`       | `Invalid data`                                       |
| `401`     | `text/plain`       | `Unauthorized`                                       |
| `500`     | `text/plain`       | `Internal server error`                              |

activity response example
``` shell
{
    "arena_id": "eaed0fa6-999c-41c5-9e2d-c631622dd454",
    "content": "Chou",
    "cover_image": "https://example.com/image.jpg",
    "creator_id": "80421ec0-45f1-485b-8133-d373903d244f",
    "end_time": "2025-06-09T19:00:00",
    "id": "6c99684a-56bf-4837-8453-b4222d6e4676",
    "is_achieved": false,
    "num_ticket": 2000,
    "on_sale_date": "2025-06-01T00:00:00",
    "price": 1000,
    "start_time": "2025-06-09T17:00:00",
    "title": "Chou"
}
```
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

| key            | required | data type      | description          |
| -------------- | -------- | -------------- | -------------------- |
| `title`        | false    | string         | Activity title       |
| `content`      | false    | string         | Optional description |
| `price`        | false    | string         | price                |
| `on_sale_date` | false    | date.isoformat | on_sale_date         |
| `start_time`   | false    | date.isoformat | start_time           |
| `end_time`     | false    | date.isoformat | end_time             |
| `cover_image`  | false    | string         | cover_image          |

date format: 2025-06-01T00:00:00

##### Responses

| http code | content-type       | response                                       |
| --------- | ------------------ | ---------------------------------------------- |
| `200`     | `application/json` | `{"message": "Activity updated successfully"}` |
| `401`     | `text/plain`       | `Unauthorized`                                 |
| `404`     | `text/plain`       | `Activity not found`                           |
| `500`     | `text/plain`       | `Internal server error`                        |

</details>

---

### **List Activity By Host**

<details>
<summary><code>GET</code> <code><b>/list_activities/host</b></code> <code>(List activities created by host)</code></summary>

##### Headers

| key             | required | data type | description             |
| --------------- | -------- | --------- | ----------------------- |
| `Authorization` | true     | string    | Bearer token from login |


##### Responses

| http code | content-type       | response                                                    |
| --------- | ------------------ | ----------------------------------------------------------- |
| `200`     | `application/json` | `{"id": "uuid", "title": "...", "description": "...", ...}` |
| `401`     | `text/plain`       | `Unauthorized`                                              |
| `500`     | `text/plain`       | `Internal server error`                                     |

</details>

---

### **List Activity By Client**

<details>
<summary><code>GET</code> <code><b>/list_activities/client</b></code> <code>(List activities which user participated)</code></summary>

##### Headers

| key             | required | data type | description             |
| --------------- | -------- | --------- | ----------------------- |
| `Authorization` | true     | string    | Bearer token from login |


##### Responses

| http code | content-type       | response                                                    |
| --------- | ------------------ | ----------------------------------------------------------- |
| `200`     | `application/json` | `{"id": "uuid", "title": "...", "description": "...", ...}` |
| `500`     | `text/plain`       | `Internal server error`                                     |

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
