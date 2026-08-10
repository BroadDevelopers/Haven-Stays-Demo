# 🏡 Haven-Stays-Demo

[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)](https://nodejs.org/)
[![Express.js](https://img.shields.io/badge/Express.js-000000?style=for-the-badge&logo=express&logoColor=white)](https://expressjs.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Gemini API](https://img.shields.io/badge/Gemini_API-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A full-stack, AI-powered vacation rental web application that allows users to explore, book, and list accommodations such as houses, villas, and farmhouses.[reference:1] This is a demo version of the **HavenStay** platform, built to showcase modern full-stack development with AI integration.[reference:2]

🔗 **Live Demo:** [View the App](https://havenstay-pp3y.onrender.com/)[reference:3]

---

## 📸 Preview

> *Coming soon — add screenshots of your landing page, property listings, and booking flow here.*

---

## 📂 Project Structure

HavenStay/
├── controllers/ # Business logic and route handlers
├── init/ # Initialization and seed files
├── models/ # MongoDB data models
├── routes/ # Express route definitions
├── views/ # EJS templates (frontend views)
├── public/ # Static assets (CSS, JS, images)
├── middleware/ # Custom middleware (auth, validation)
├── utils/ # Utility functions
├── .env # Environment variables
├── app.js # Main application entry point
├── package.json # Dependencies and scripts
└── README.md # Project documentation


---

## 🧩 Features

### Core Functionality[reference:6]
- Browse and explore vacation rentals
- Create, edit, and manage property listings
- Seamless booking & reservation workflow
- ⭐ User reviews & ratings system
- Secure authentication with sessions & cookies

### AI-Powered Features[reference:7]
- **AI-Based Smart Search** – Understands user intent and returns the most relevant listings
- **AI-Generated Titles & Descriptions** – Automatically generates optimized titles and descriptions for new listings using the **Gemini API 2.5 Flash**

### Map Integration[reference:8]
- **Leaflet Maps** for real-time property location visualization
- Interactive markers for better geographic context

### User Experience[reference:9]
- Fully responsive design (mobile, tablet & desktop)
- Clean, intuitive UI inspired by real-world rental platforms
- Advanced search and filters for faster discovery

---

## 🛠️ Tech Stack[reference:10]

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | HTML, CSS, JavaScript, Bootstrap, EJS, React.js |
| **Backend** | Node.js, Express.js |
| **Database** | MongoDB Atlas |
| **AI Integration** | Gemini API 2.5 Flash (Smart search & content generation) |
| **Maps** | Leaflet + OpenStreetMap |
| **Deployment** | Render |

---

## 🏗️ Architecture[reference:11]

- **MVC (Model–View–Controller) Architecture**
- RESTful routing
- Server-side & client-side validation
- Secure authentication & authorization
- Scalable project structure

---

## 🔒 Authentication & Security[reference:12]

- Cookie-based sessions
- Flash messages for user feedback
- Input validation using middleware
- Protected routes for authorized actions

---

## 🚀 Getting Started

### Prerequisites
- [Node.js](https://nodejs.org/) (v14 or higher)
- [MongoDB Atlas](https://www.mongodb.com/atlas) account (or local MongoDB instance)
- [Gemini API Key](https://ai.google.dev/) (for AI features)

### Installation[reference:13]

1. **Clone the repository**
   ```bash
   git clone https://github.com/BroadDevelopers/Haven-Stays-Demo.git
   cd Haven-Stays-Demo

   
---

## 🧩 Features

### Core Functionality[reference:6]
- Browse and explore vacation rentals
- Create, edit, and manage property listings
- Seamless booking & reservation workflow
- ⭐ User reviews & ratings system
- Secure authentication with sessions & cookies

### AI-Powered Features[reference:7]
- **AI-Based Smart Search** – Understands user intent and returns the most relevant listings
- **AI-Generated Titles & Descriptions** – Automatically generates optimized titles and descriptions for new listings using the **Gemini API 2.5 Flash**

### Map Integration[reference:8]
- **Leaflet Maps** for real-time property location visualization
- Interactive markers for better geographic context

### User Experience[reference:9]
- Fully responsive design (mobile, tablet & desktop)
- Clean, intuitive UI inspired by real-world rental platforms
- Advanced search and filters for faster discovery

---

## 🛠️ Tech Stack[reference:10]

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | HTML, CSS, JavaScript, Bootstrap, EJS, React.js |
| **Backend** | Node.js, Express.js |
| **Database** | MongoDB Atlas |
| **AI Integration** | Gemini API 2.5 Flash (Smart search & content generation) |
| **Maps** | Leaflet + OpenStreetMap |
| **Deployment** | Render |

---

## 🏗️ Architecture[reference:11]

- **MVC (Model–View–Controller) Architecture**
- RESTful routing
- Server-side & client-side validation
- Secure authentication & authorization
- Scalable project structure

---

## 🔒 Authentication & Security[reference:12]

- Cookie-based sessions
- Flash messages for user feedback
- Input validation using middleware
- Protected routes for authorized actions

---

## 🚀 Getting Started

### Prerequisites
- [Node.js](https://nodejs.org/) (v14 or higher)
- [MongoDB Atlas](https://www.mongodb.com/atlas) account (or local MongoDB instance)
- [Gemini API Key](https://ai.google.dev/) (for AI features)

### Installation[reference:13]

1. **Clone the repository**
   ```bash
   git clone https://github.com/BroadDevelopers/Haven-Stays-Demo.git
   cd Haven-Stays-Demo

   Install dependencies
   npm install

   Set up environment variables
Create a .env file in the root directory:
PORT=3000
MONGODB_URI=your_mongodb_connection_string
SESSION_SECRET=your_session_secret
GEMINI_API_KEY=your_gemini_api_key

Run the application
npm start

Responsive Design
The application is fully responsive and works seamlessly across:

Desktop – Full layout with all features

Tablet – Adjusted spacing and optimized navigation

Mobile – Touch-friendly interface with stacked layout

🤝 Contributing
Contributions are welcome! If you have ideas for improvements, new features, or bug fixes:

Fork the repository.

Create your feature branch (git checkout -b feature/AmazingFeature).

Commit your changes (git commit -m 'Add some AmazingFeature').

Push to the branch (git push origin feature/AmazingFeature).

Open a Pull Request.

📜 License
Distributed under the MIT License. See LICENSE for more information.

👥 Authors
BroadDevelopers – Initial work – BroadDevelopers

Based on the original HavenStay project by Tushar Parmar

🙏 Acknowledgments
Gemini API – For AI-powered search and content generation

Leaflet & OpenStreetMap – For interactive maps

Render – For hosting the live demo

MongoDB Atlas – For cloud database hosting

