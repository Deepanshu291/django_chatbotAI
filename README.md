## **Django Chatbot API with Google Gemini**
This is a Django REST API for a chatbot using **Django REST Framework (DRF)** and **Google Gemini AI**. It supports **user authentication, chat sessions, and AI-generated responses**.

---

## **🚀 Features**
- User **Registration & Login** (JWT Authentication)  
- **Chat Sessions** (Create, Retrieve, Update, Delete)  
- **Messages** (Store User Prompts & AI Responses)  
- **Google Gemini AI Integration**  

---

## **📌 Tech Stack**
- **Backend:** Django, Django REST Framework  
- **Auth:** JWT (Simple JWT)  
- **AI Model:** Google Gemini  
- **Database:** SQLite (Default)  

---

## **🛠️ Installation Guide**
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/yourusername/django-chatbot.git
cd django-chatbot
```

### **2️⃣ Create & Activate Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Configure Environment Variables**
Create a `.env` file in the project root and add your **Google Gemini API Key**:

```
GOOGLE_GEMINI_API_KEY=your_api_key_here
```

### **5️⃣ Apply Migrations**
```sh
python manage.py makemigrations
python manage.py migrate
```

### **6️⃣ Create a Superuser**
```sh
python manage.py createsuperuser
```

### **7️⃣ Run the Server**
```sh
python manage.py runserver
```

Your API is now running at:  
📌 **http://127.0.0.1:8000/**  

---

## **🔐 Authentication**
### **1️⃣ Register a User**
```sh
curl -X POST http://127.0.0.1:8000/register/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "email": "test@example.com", "password": "testpass"}'
```

### **2️⃣ Login to Get JWT Token**
```sh
curl -X POST http://127.0.0.1:8000/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "testpass"}'
```
**Response:**
```json
{
    "refresh": "your_refresh_token",
    "access": "your_access_token"
}
```
**Use the `access_token` for authentication in further requests.**

---

## **🛠️ JWT Authentication (Login & Token Refresh)**
This project uses **JWT authentication** via `SimpleJWT`.  

### **1️⃣ Get Access & Refresh Token**
```sh
curl -X POST http://127.0.0.1:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "testpass"}'
```
**Response:**
```json
{
    "refresh": "your_refresh_token",
    "access": "your_access_token"
}
```

### **2️⃣ Refresh Access Token**
If your access token expires, use the **refresh token** to get a new access token.

```sh
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh": "your_refresh_token"}'
```
**Response:**
```json
{
    "access": "new_access_token"
}
```

### **3️⃣ Verify Token**
Check if a token is still valid.

```sh
curl -X POST http://127.0.0.1:8000/api/token/verify/ \
     -H "Content-Type: application/json" \
     -d '{"token": "your_access_token"}'
```
**Response (Valid Token):**
```json
{}
```
**Response (Invalid Token):**
```json
{
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
}
```

---

## **📡 Updated API Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/api/token/` | Get access & refresh token |
| **POST** | `/api/token/refresh/` | Refresh expired access token |
| **POST** | `/api/token/verify/` | Verify if token is valid |
| **POST** | `/register/` | Register a new user |
| **POST** | `/login/` | Login and get JWT token |

---

## **📡 API Endpoints**
### **🔹 Chat Sessions**
| Method | Endpoint | Description |
|--------|----------|-------------|
| **GET** | `/chatsessions/` | List user’s chat sessions |
| **POST** | `/chatsessions/` | Create a new chat session |
| **GET** | `/chatsessions/{session_id}/` | Retrieve a chat session |
| **PUT** | `/chatsessions/{session_id}/` | Update a chat session |
| **DELETE** | `/chatsessions/{session_id}/` | Delete a chat session |

### **🔹 Messages**
| Method | Endpoint | Description |
|--------|----------|-------------|
| **GET** | `/chatsessions/{session_id}/messages/` | List messages in a session |
| **POST** | `/chatsessions/{session_id}/messages/` | Send a message (AI will respond) |

---

## **💬 Example API Usage**
### **1️⃣ Create a Chat Session**
```sh
curl -X POST http://127.0.0.1:8000/chatsessions/ \
     -H "Authorization: Bearer <your_token>"
```
**Response:**
```json
{
    "id": 1,
    "user": 1,
    "title": null,
    "started_at": "2025-03-22T12:00:00Z",
    "updated_at": "2025-03-22T12:00:00Z"
}
```

### **2️⃣ Send a Message**
```sh
curl -X POST http://127.0.0.1:8000/chatsessions/1/messages/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello, chatbot!"}'
```
**Response:**
```json
{
    "id": 1,
    "session": 1,
    "prompt": "Hello, chatbot!",
    "response": "Hi there! How can I assist you today?",
    "created_at": "2025-03-22T12:05:00Z"
}
```


---

## **📜 License**
This project is licensed under the **MIT License**.

---

## **💡 Need Help?**
🐙 GitHub: **[@deepanshu291](https://github.com/deepanshu291)**  

---

Would you like to add **frontend setup instructions** too? 🚀
