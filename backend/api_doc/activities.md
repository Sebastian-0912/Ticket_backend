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

| key           | required | data type | description               |
| ------------- | -------- | --------- | ------------------------- |
| `title`       | true     | string    | Activity title            |
| `description` | false    | string    | Optional description      |
| `location`    | false    | string    | Where the activity occurs |
| `time`        | true     | string    | ISO 8601 datetime string  |

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

| key           | required | data type | description            |
| ------------- | -------- | --------- | ---------------------- |
| `title`       | false    | string    | Updated activity title |
| `description` | false    | string    | Updated description    |
| `location`    | false    | string    | Updated location       |
| `time`        | false    | string    | Updated ISO 8601 time  |

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
