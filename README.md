# Automated Marketing Agent

A comprehensive automated marketing agent system that schedules, generates, and posts content across multiple social media platforms while optimizing for engagement and maintaining brand consistency.

## Features

### 🎯 Content Management
- Centralized content repository for text, images, and videos
- AI-powered caption and hashtag generation
- Brand voice and style guideline enforcement
- Content categorization and tagging

### 📅 Scheduling & Posting
- Multi-platform support (Instagram, Facebook, LinkedIn, Twitter, TikTok)
- Optimal engagement time analysis
- Automatic posting with error handling and retry logic
- Campaign sequence automation

### 📊 Analytics & Reporting
- Real-time engagement metrics tracking
- Weekly/monthly automated reports
- AI-powered engagement improvement suggestions
- Performance trend analysis

### 🤖 Automation & Workflow
- Rule-based recurring post management
- CRM and email marketing integration
- Smart notifications for approvals and errors
- Adaptive posting frequency based on engagement

### 🔐 Security & Compliance
- Encrypted credential storage
- Platform-specific compliance checks
- Secure API key management
- Data privacy protection

## Quick Start

### Prerequisites
- Python 3.8+
- Redis server
- PostgreSQL database

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd agent
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
alembic upgrade head
```

6. Start the application:
```bash
# Start Redis server
redis-server

# Start Celery worker (in another terminal)
celery -A app.core.celery worker --loglevel=info

# Start the web application
uvicorn app.main:app --reload
```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Database
DATABASE_URL=postgresql://username:password@localhost/marketing_agent

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI API
OPENAI_API_KEY=your-openai-api-key

# Social Media APIs
TWITTER_API_KEY=your-twitter-api-key
TWITTER_API_SECRET=your-twitter-api-secret
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret
INSTAGRAM_CLIENT_ID=your-instagram-client-id
INSTAGRAM_CLIENT_SECRET=your-instagram-client-secret
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret
```

## API Documentation

Once the application is running, visit:
- API Documentation: http://localhost:8000/docs
- Web Dashboard: http://localhost:8000

## Project Structure

```
agent/
├── app/
│   ├── api/                 # API endpoints
│   ├── core/                # Core functionality
│   ├── models/              # Database models
│   ├── services/            # Business logic
│   ├── utils/               # Utility functions
│   └── templates/           # Web templates
├── tests/                   # Test files
├── migrations/              # Database migrations
├── static/                  # Static assets
└── config/                  # Configuration files
```

## Usage

### 1. Content Management
- Upload content to the centralized repository
- Set brand guidelines and voice parameters
- Tag and categorize content for easy organization

### 2. Campaign Setup
- Create posting schedules for different platforms
- Configure automation rules
- Set up approval workflows

### 3. Analytics Monitoring
- View real-time engagement metrics
- Generate custom reports
- Review AI suggestions for optimization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue on GitHub or contact the development team.
