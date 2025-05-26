# /tickets routes

---

### Reserve a Ticket

<details>
<summary><code>POST</code> <code><b>/reserve</b></code></summary>

**Description:**  
Reserves a ticket for a user for a given activity. Sets ticket status to `UNPAID`.

**Headers**

| key             | required | data type | description             |
| --------------- | -------- | --------- | ----------------------- |
| `Authorization` | true     | string    | Bearer token from login |

**Request Body:**

| Field         | Type | Required | Description        |
| ------------- | ---- | -------- | ------------------ |
| `user_id`     | UUID | true     | ID of the user     |
| `activity_id` | UUID | true     | ID of the activity |
| `num_tickets` | int  | true     | Number of tickets  |

**Responses:**

| Code | Description                      |
| ---- | -------------------------------- |
| 201  | Ticket reserved successfully     |
| 400  | Tickets sold out or invalid data |
| 500  | Internal server error            |

</details>

---

### Buy a Ticket

<details>
<summary><code>POST</code> <code><b>/buy</b></code></summary>

**Description:**  
Completes a previously reserved ticket. Updates status from `UNPAID` to `SOLD`.

**Headers**

| key             | required | data type | description             |
| --------------- | -------- | --------- | ----------------------- |
| `Authorization` | true     | string    | Bearer token from login |

**Request Body:**

| Field       | Type | Required | Description             |
| ----------- | ---- | -------- | ----------------------- |
| `ticket_id` | UUID | true     | ID of the ticket to buy |

**Responses:**

| Code | Description                   |
| ---- | ----------------------------- |
| 200  | Ticket purchased successfully |
| 400  | Ticket not in unpaid state    |
| 404  | Ticket not found              |
| 500  | Internal server error         |

</details>

---

### Refund a Ticket

<details>
<summary><code>POST</code> <code><b>/refund</b></code></summary>

**Description:**  
Refunds a ticket. Sets status back to `UNSOLD`.


**Headers**

| key             | required | data type | description             |
| --------------- | -------- | --------- | ----------------------- |
| `Authorization` | true     | string    | Bearer token from login |

**Request Body:**

| Field       | Type | Required | Description                |
| ----------- | ---- | -------- | -------------------------- |
| `ticket_id` | UUID | true     | ID of the ticket to refund |

**Responses:**

| Code | Description                          |
| ---- | ------------------------------------ |
| 200  | Ticket refunded successfully         |
| 400  | Ticket already used or cannot refund |
| 404  | Ticket not found                     |
| 500  | Internal server error                |

</details>

---

### Get Ticket by ID

<details>
<summary><code>GET</code> <code><b>/&lt;ticket_id&gt;</b></code></summary>

**Description:**  
Retrieves details of a single ticket.


**Headers**

| key             | required | data type | description             |
| --------------- | -------- | --------- | ----------------------- |
| `Authorization` | true     | string    | Bearer token from login |

**Responses:**

| Code | Description           |
| ---- | --------------------- |
| 200  | Ticket details        |
| 404  | Ticket not found      |
| 500  | Internal server error |

</details>

---

### Delete a Ticket (Admin Only)

<details>
<summary><code>DELETE</code> <code><b>/&lt;ticket_id&gt;</b></code></summary>

**Description:**  
Deletes a ticket (usually soft-delete or admin only).


**Headers**

| key             | required | data type | description             |
| --------------- | -------- | --------- | ----------------------- |
| `Authorization` | true     | string    | Bearer token from login |

**Responses:**

| Code | Description           |
| ---- | --------------------- |
| 204  | Ticket deleted        |
| 404  | Ticket not found      |
| 500  | Internal server error |

</details>

---

### Ticket Status Enum

```python
class TicketStatus(str, Enum):
    UNSOLD = "unsold"   # Available but not reserved
    UNPAID = "unpaid"   # Reserved but not paid
    SOLD   = "sold"     # Paid and confirmed
