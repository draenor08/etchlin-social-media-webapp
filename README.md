# ✨ Etchlin - A Classy Social Media WebApp 👥📸

Welcome to *Etchlin*, a tastefully minimalist social media platform that's like a calmer, more refined cousin of the chaotic social networks we know. Built with grit, raw SQL, and the occasional bout of late-night debugging, Etchlin aims to deliver a stripped-down, performance-driven social experience.

---

## 🎯 What is Etchlin?

Etchlin is a **toned-down media platform** designed for those who appreciate simplicity and clean aesthetics. It's a project built to sharpen full-stack skills without the crutch of high-level abstractions. With Etchlin, you can:

* Create profiles and posts 🖼️
* Add friends (two-way model) 🤝
* Like, comment, and message 🔁
* Flag content for admin review 🚩

All wrapped in a *navy blue & beige* aesthetic.

---

## 🔧 Tech Stack

| Layer        | Tech Used                      |
| ------------ | ------------------------------ |
| Frontend     | React.js                       |
| Styling      | Custom CSS                     |
| Backend      | Django (no ORM, raw SQL!)      |
| Database     | MySQL                          |
| Auth         | Session-based (cookies)🍪      |
| Deployment   | (Planned) Vercel / Self-hosted |
| Version Ctrl | Git + GitHub                   |

---

### 💡 Key Features

👤 **User System**

* Register / Login / Logout
* Edit profile (bio, profile picture)
* Session-based auth with redirect after login

📸 **Posts**

* Create, edit and delete post (image/text)
* View all posts (feed)
* Like & comment
* See your own posts on profile

💬 **Messaging**

* Simple non-real-time messaging (sender → receiver)
* View messages in order

🧭 **Social**

* Add Friends (one-way follow model)
* View friend list
* Search users & posts

⚠️ **Admin Audit**

* Admins are regular users with extra powers
* Flag & view flagged content (posts/comments)
* No special dashboard (just actions)

🖼️ **Media Handling**

* Image uploads are stored **locally**
* Image URLs saved in database

---

## 🚧 Folder Structure (Backend)

```
backend/
├── userapp/
├── postapp/
├── socialapp/
├── messageapp/
├── adminapp/
├── auth/
├── db/
└── main.py (or views.py/router.py depending on split)
```

---

## 🧪 How to Run (Locally)

### Backend Setup

```bash
cd etchlin-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup

```bash
cd etchlin-frontend
npm install
npm start
```

> **Note:** Make sure you ran the database script, MySQL is running, and your `.env` is properly configured!

---

## 🔐 Authentication Logic

* Session-based auth using cookies
* After login, session is stored, user can access protected routes
* No auto-login after registration (redirects to login page instead)

---

## 🌐 Live Demo (Coming Soon...)

> [Watch the Demo](https://youtu.be/QZa5NhSctiY) 👀

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
