# CyberSentinels CTF Machine by Sujal Adhikari

Welcome to the beginner-friendly but DevOps-style CTF machine designed for hands-on learning and real-world security practice.

## 👨‍💻 Developer

**Sujal Adhikari**  
President, CyberSentinels Cybersecurity Club  
Discord Community: [Join Here](https://discord.gg/vuqfzVkzRe)

## 🚩 Flags Included

- HTML comment clue
- Brute force attack
- Cryptography puzzle
- XSS alert
- Steganography
- Base64 decode
- Obfuscated HTML source
- Hidden URL clue
- URL encoding challenge
- Final SSL login (username + password from previous flags)

## ⚙️ Tech Stack

- Python (Flask)
- HTML, CSS, JavaScript
- SQLite database
- Docker
- DevOps best practices

## 🚀 Deployment Instructions

### Windows Deployment

1. Install Python 3.11 or higher
   ```bash
   # Download Python from https://www.python.org/downloads/
   # During installation, check "Add Python to PATH"
   ```

2. Install Git
   ```bash
   # Download from https://git-scm.com/download/win
   ```

3. Clone the repository
   ```bash
   git clone https://github.com/YOUR-USERNAME/ctf-cybersentinels.git
   cd ctf-cybersentinels
   ```

4. Set up virtual environment
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

5. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

6. Set up environment variables
   ```bash
   copy .env.example .env
   # Edit .env file with your preferred settings
   ```

7. Initialize database
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

8. Run the application
   ```bash
   python run.py
   ```

### Kali Linux Deployment

1. Update system packages
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. Install Python and Git
   ```bash
   sudo apt install -y python3 python3-pip python3-venv git
   ```

3. Clone the repository
   ```bash
   git clone https://github.com/YOUR-USERNAME/ctf-cybersentinels.git
   cd ctf-cybersentinels
   ```

4. Set up virtual environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

5. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

6. Set up environment variables
   ```bash
   cp .env.example .env
   # Edit .env as needed using nano or your preferred editor
   nano .env
   ```

7. Initialize database
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

8. Run the application
   ```bash
   python3 run.py
   ```

### Docker Deployment (Both Windows and Kali)

1. Install Docker
   - Windows: Download Docker Desktop from https://www.docker.com/products/docker-desktop
   - Kali: `sudo apt install -y docker.io docker-compose`

2. Build and run with Docker Compose
   ```bash
   docker-compose up --build
   ```

Access the application at: http://localhost:5000

## 📊 Project Structure

```
ctf-machine/
├── app/                    # Application package
│   ├── __init__.py         # Initialize app
│   ├── config.py           # Configuration settings
│   ├── models.py           # Database models
│   ├── extensions.py       # Flask extensions
│   ├── utils/              # Utility functions
│   ├── forms/              # Form classes
│   ├── routes/             # Route handlers
│   ├── static/             # Static files (CSS, JS)
│   └── templates/          # HTML templates
├── migrations/             # Database migrations
├── logs/                   # Application logs
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose config
├── .env.example            # Example environment variables
└── README.md              # Project documentation
```

## 🎓 Made for Learning

This CTF is designed to simulate real-world DevSecOps setups and secure development. Enjoy the challenge and join our community to share progress!

## 📝 Hints

Each challenge includes a hint button if you get stuck. Remember, the goal is to learn, so don't hesitate to use hints when needed.

## 🔒 Security Note

This application intentionally contains security vulnerabilities for educational purposes. Do not use any code from this project in production environments without proper security hardening.