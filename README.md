```markdown
# ✨ Etchlin - A Classy Social Media WebApp 👥📸

Welcome to **Etchlin**, a tastefully minimalist social media platform that's like a calmer, more refined cousin of social media giants we are accustomed to. Built with love (and raw SQL), Etchlin is designed for simplicity, performance, and learning how full-stack magic works from scratch.

---

## 🎯 What is Etchlin?

Etchlin is a **toned-down media platform** made for learning and fun. You can:
- Create profiles and posts 🖼️
- Add other users (two-way friendship) 🤝
- Like, comment, and message 🔁
- Flag posts/comments for admin review 🚩

All wrapped in a *navy blue & beige* aesthetic.

---

## 🔧 Tech Stack

| Layer         | Tech Used                       |
|--------------|----------------------------------|
| Frontend     | React.js                         |
| Styling      | Custom CSS Styling               |
| Backend      | Django (no ORM, raw SQL!)        |
| Database     | MySQL                            |
| Auth         | Session-based (cookies)🍪        |
| Deployment   | (Planned) Vercel / Self-hosted   |
| Version Ctrl | Git + GitHub                     |

---

## 💡 Key Features

### 👤 User System
- Register / Login / Logout
- Edit profile (bio, profile picture)
- Session-based auth with redirect after login

### 📸 Posts
- Create, edit and delete post (image/text)
- View all posts (feed)
- Like & comment
- See your own posts on profile

### 💬 Messaging
- Simple non-real-time messaging (sender → receiver)
- View messages in order

### 🧭 Social
- Add Friends (like facebook)
- View friend list
- Search users & posts

### ⚠️ Admin Audit
- Admins are regular users with extra powers
- Flag & view flagged content (posts/comments)
- No special dashboard (just actions)

### 🖼️ Media Handling
- Image uploads are stored **locally**
- Image URLs saved in database

---

## 🚧 Folder Structure (Backend)

```

etchlin-backend/
├── userapp/
├── postapp/
├── socialapp/
├── messageapp/
├── adminapp/
├── auth/
├── db/
└── main.py (or views.py/router.py depending on split)

````

---

## 🧪 How to Run (Locally)



### Backend
cd etchlin-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirement.txt
python manage.py runserver
````

### Frontend

```bash
cd etchlin-frontend
npm install
npm start
```

Make sure you ran the database script, MySQL is running, and `.env` is properly configured!

---

## 🔐 Authentication Logic

* Session-based auth using cookies
* After login, session is stored, user can access protected routes
* No auto-login after registration (redirects to login page instead)

---

## 🌐 Live Demo (Coming Soon...)

📦 Will be deployed via **Vercel** and possibly a self-hosted backend.

---

## 📌 To-Do List

* [x] Session-based login/logout ✅
* [x] Post with image upload 🖼️
* [x] Like & comment system ❤️💬
* [x] Messaging 💌
* [ ] Notification system (dynamically queried) 🔔
* [ ] Real-time updates (maybe someday?) ⏱️
* [ ] Mobile responsive version 📱

---

## 🤝 Contributing

This is a personal project, but feel free to open issues or PRs if you're curious and want to help!

---

## 📜 License

MIT License — Free to learn, build, and tweak.

---

## 👑 Author

Made with grit, SQL, and late-night debugging by [@draenor08](https://github.com/draenor08) 🧠💻

---

> Etch your moments. Quietly, beautifully.
> — *Etchlin*
