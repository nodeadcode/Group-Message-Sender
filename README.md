# 🚀 Spinify Ads - Telegram Group Advertisement Scheduler

A beautiful, modern web application for scheduling and automating advertisement messages across multiple Telegram groups. Built with a premium glassmorphic UI and powered by Python backend.

![Spinify Ads](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.8+-blue)

## ✨ Features

### 🎨 Premium UI/UX
- **Glassmorphic Design** - Modern translucent cards with backdrop blur
- **Vibrant Gradients** - Eye-catching purple and pink color schemes
- **Smooth Animations** - Micro-interactions throughout the app
- **Fully Responsive** - Works seamlessly on mobile, tablet, and desktop
- **Dark Theme** - Professional dark mode interface

### 🔧 Core Functionality
- **Multi-Group Support** - Manage up to 10 Telegram groups
- **Message Scheduling** - Automated message forwarding with configurable intervals
- **Smart Delays** - 60-second delays between groups and messages to avoid spam detection
- **Night Mode** - Auto-pause campaigns during night hours (10 PM - 6 AM)
- **Saved Messages** - Messages saved to Telegram first, then forwarded to groups
- **Session Management** - Persistent user sessions across server restarts

### ⚙️ Campaign Configuration
- **Flexible Intervals** - Choose from 20 minutes to 4 hours between campaigns
- **Custom Delays** - Configurable delays between groups and messages
- **Night Mode Toggle** - Prevent messaging during specified night hours
- **Real-time Status** - Live campaign status monitoring

## 🎯 Use Cases

- **Business Promotion** - Advertise products/services to multiple groups
- **Event Announcements** - Share event details across communities
- **Content Distribution** - Broadcast content to your audience
- **Community Management** - Send updates to multiple groups efficiently

## 📸 Screenshots

### Step 1: API Credentials
Beautiful glassmorphic design with gradient accents

### Step 5: Campaign Configuration
![Campaign Configuration](https://via.placeholder.com/800x400?text=Campaign+Configuration+Interface)

Advanced scheduling with interval selector and night mode toggle

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Telegram API credentials ([Get them here](https://my.telegram.org/apps))
- Node.js (optional, for development)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Group-Message-Sender.git
cd Group-Message-Sender
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Start the web server**
```bash
# Simple HTTP server for testing
python -m http.server 8080 --directory webapp

# Or use the FastAPI backend
cd backend
uvicorn main:app --reload
```

4. **Open your browser**
```
http://localhost:8080
```

## 🏗️ Project Structure

```
Group-Message-Sender/
├── webapp/                 # Frontend application
│   ├── index.html         # Main HTML file
│   ├── style.css          # Premium CSS styling (1000+ lines)
│   └── app.js             # JavaScript logic (700+ lines)
├── backend/               # Python backend
│   ├── main.py           # FastAPI application
│   ├── scheduler.py      # Campaign scheduling logic
│   ├── telegram_auth.py  # Telegram authentication
│   ├── telethon_login.py # Telethon integration
│   └── group_verify.py   # Group verification
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 📝 Configuration

### Telegram API Setup

1. Visit [my.telegram.org/apps](https://my.telegram.org/apps)
2. Log in with your phone number
3. Create a new application
4. Copy your `API ID` and `API Hash`
5. Enter these in Step 1 of the web app

### Campaign Settings

- **Max Groups**: Up to 10 groups per campaign
- **Group Delay**: 60 seconds between each group
- **Message Delay**: 60 seconds between each message
- **Min Interval**: 20 minutes between campaign cycles
- **Night Mode**: 10 PM - 6 AM (configurable)

## 🔒 Security Features

- **Encrypted Sessions** - User sessions stored securely
- **No Data Leaks** - Messages only forwarded, never stored on server
- **Rate Limiting** - Built-in delays to prevent spam detection
- **Secure Storage** - API credentials encrypted in database

## 🛠️ Technology Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Glassmorphism, gradients, animations
- **JavaScript ES6+** - Modern async/await patterns
- **Google Fonts** - Inter font family

### Backend
- **Python 3.8+** - Core language
- **FastAPI** - Modern web framework
- **Telethon** - Telegram client library
- **SQLAlchemy** - Database ORM (planned)

## 📖 Usage Guide

### Step-by-Step Workflow

1. **API Credentials** - Enter your Telegram API ID and Hash
2. **Authentication** - Verify your phone number via Telegram OTP
3. **Add Groups** - Input up to 10 Telegram group links
4. **Create Messages** - Write and save your advertisement messages
5. **Configure Campaign** - Set interval and enable night mode if needed
6. **Launch** - Start your automated campaign!

### Message Flow

```
User Message → Saved Messages → Group 1 (60s) → Group 2 (60s) → ... → Group 10
                                     ↓
                              Wait for Interval (20min - 4hr)
                                     ↓
                              Repeat with Next Message
```

## 🎨 Design Philosophy

The UI follows modern design principles:

- **Glassmorphism** - Translucent surfaces with backdrop blur
- **Vibrant Colors** - Carefully selected gradient combinations
- **Micro-interactions** - Smooth animations on every interaction
- **Mobile-first** - Responsive design that works everywhere
- **Accessibility** - High contrast and readable fonts

## 🔄 Roadmap

- [ ] Database integration (SQLite/PostgreSQL)
- [ ] User authentication system
- [ ] Campaign analytics dashboard
- [ ] Image/media support for ads
- [ ] Scheduled campaigns (date/time picker)
- [ ] Group performance tracking
- [ ] Multi-user support
- [ ] Admin panel

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**@spinify**

- Telegram: [@spinify](https://t.me/spinify)
- GitHub: [@yourusername](https://github.com/yourusername)

## 🙏 Acknowledgments

- Built with ❤️ using modern web technologies
- Inspired by the need for efficient group management
- Thanks to the Telethon community for their excellent library

## 📞 Support

If you have any questions or need help, feel free to:

- Open an issue on GitHub
- Contact [@spinify](https://t.me/spinify) on Telegram
- Check the [Documentation](docs/)

---

**⭐ Star this repo if you find it useful!**

Made with ✨ by @spinify