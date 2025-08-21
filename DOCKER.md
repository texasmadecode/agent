# Docker Deployment Guide

This guide covers Docker deployment options for the Marketing Agent application.

## 🏗️ Architecture

The Docker setup includes:

- **PostgreSQL Database** - Primary data storage
- **Redis** - Task queue and caching
- **API Server** - FastAPI application
- **Celery Worker** - Background task processing
- **Celery Beat** - Scheduled task management

## 🚀 Quick Start

### 1. Preparation

```bash
# Clone the repository
git clone <your-repo-url>
cd agent

# Make scripts executable
chmod +x setup.sh start.sh configure_api_keys.py
```

### 2. Configuration

#### Option A: Interactive Setup
```bash
./setup.sh
```

#### Option B: Manual Configuration
```bash
# Copy environment template
cp .env.example .env

# Configure API keys
python configure_api_keys.py

# Or edit .env manually
nano .env
```

### 3. Start Services

#### Option A: Quick Start Script
```bash
./start.sh
```

#### Option B: Docker Compose
```bash
docker-compose up -d
```

#### Option C: Make Commands
```bash
make up
```

## 🛠️ Development Setup

For development with hot reloading:

```bash
# Start development environment
make dev

# Or manually
docker-compose -f docker-compose.dev.yml up
```

Development setup differences:
- Runs on port 8001 (instead of 8000)
- Enables hot reloading
- Uses separate database (marketing_agent_dev)
- Mounts source code for live editing

## 📋 Available Commands

### Make Commands (Recommended)
```bash
make help           # Show all available commands
make setup          # Interactive setup
make up             # Start production
make dev            # Start development
make down           # Stop services
make logs           # View logs
make shell          # Access container shell
make clean          # Clean Docker resources
make reset          # Reset everything (destroys data)
```

### Docker Compose Commands
```bash
# Production
docker-compose up -d                    # Start services
docker-compose down                     # Stop services
docker-compose logs -f                  # View logs
docker-compose ps                       # Check status

# Development
docker-compose -f docker-compose.dev.yml up -d
```

### Direct Docker Commands
```bash
# Build images
docker-compose build

# Access container shell
docker-compose exec api bash

# Run migrations
docker-compose exec api alembic upgrade head

# Initialize database
docker-compose exec api python -m app.core.init_db
```

## 🔧 Configuration

### Environment Variables

Key configuration options in `.env`:

#### Database
```bash
POSTGRES_DB=marketing_agent
POSTGRES_USER=marketing_admin
POSTGRES_PASSWORD=your_secure_password
```

#### API Keys (Required)
```bash
OPENAI_API_KEY=sk-your-openai-key
```

#### Social Media APIs (Optional)
```bash
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret
TWITTER_API_KEY=your_api_key
# ... etc
```

#### Security
```bash
SECRET_KEY=your-super-secure-secret-key
REDIS_PASSWORD=your-redis-password
```

### Volume Mounts

The setup creates persistent volumes for:
- `postgres_data` - Database storage
- `redis_data` - Redis persistence
- `uploads_data` - File uploads

## 🌐 Service Access

After starting, access services at:

| Service | URL | Description |
|---------|-----|-------------|
| Main App | http://localhost:8000 | Marketing Agent interface |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| Health Check | http://localhost:8000/health | Service health status |
| PostgreSQL | localhost:5432 | Database (external access) |
| Redis | localhost:6379 | Cache/Queue (external access) |

## 🔍 Monitoring & Logs

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f worker
docker-compose logs -f postgres
```

### Health Checks
```bash
# Application health
curl http://localhost:8000/health

# Service status
docker-compose ps

# Or use Make command
make status
```

### Container Shell Access
```bash
# API container
docker-compose exec api bash

# Database
docker-compose exec postgres psql -U marketing_admin -d marketing_agent
```

## 🚀 Production Deployment

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- 2GB+ RAM
- 10GB+ disk space

### Production Checklist

1. **Secure Configuration**
   ```bash
   # Generate secure passwords
   openssl rand -base64 32  # For SECRET_KEY
   openssl rand -base64 16  # For database passwords
   ```

2. **Environment Setup**
   ```bash
   # Set production environment
   ENVIRONMENT=production
   DEBUG=false
   
   # Configure strong passwords
   POSTGRES_PASSWORD=your_super_secure_password
   REDIS_PASSWORD=your_redis_password
   SECRET_KEY=your_super_secure_secret_key
   ```

3. **Network Security**
   - Remove port exposures for internal services
   - Use reverse proxy (nginx) for HTTPS
   - Configure firewall rules

4. **Backup Strategy**
   ```bash
   # Database backup
   docker-compose exec postgres pg_dump -U marketing_admin marketing_agent > backup.sql
   
   # Volume backup
   docker run --rm -v marketing_agent_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz /data
   ```

### Production Docker Compose

For production, modify `docker-compose.yml`:

```yaml
# Remove port exposures for internal services
postgres:
  # ports:
  #   - "5432:5432"  # Remove this line

redis:
  # ports:
  #   - "6379:6379"  # Remove this line

# Add resource limits
api:
  deploy:
    resources:
      limits:
        memory: 1G
        cpus: '0.5'
```

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Check what's using the port
lsof -i :8000

# Stop conflicting services
docker-compose down
```

#### Database Connection Issues
```bash
# Check database status
docker-compose exec postgres pg_isready -U marketing_admin

# Reset database
make reset  # ⚠️ This destroys all data
```

#### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER ./uploads
```

#### Container Won't Start
```bash
# Check logs
docker-compose logs api

# Restart specific service
docker-compose restart api
```

### Performance Tuning

#### Database
```bash
# Increase shared_buffers for better performance
# Add to docker-compose.yml postgres service:
command: postgres -c shared_buffers=256MB -c max_connections=200
```

#### API Server
```bash
# Scale API servers
docker-compose up --scale api=3
```

## 🔄 Updates & Maintenance

### Update Application
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose up --build -d
```

### Database Migrations
```bash
# Run migrations
docker-compose exec api alembic upgrade head

# Create new migration
docker-compose exec api alembic revision --autogenerate -m "Description"
```

### Cleanup
```bash
# Remove unused Docker resources
make clean

# Or manually
docker system prune -f
docker volume prune -f
```

## 📊 Monitoring Setup

### Basic Monitoring
```bash
# Add to docker-compose.yml for resource monitoring
version: '3.8'
services:
  api:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Health Check Integration
The application includes a `/health` endpoint that can be used with:
- Load balancers
- Container orchestration
- Monitoring systems

Example health check response:
```json
{
  "status": "healthy",
  "timestamp": "2025-08-21T10:00:00Z",
  "version": "1.0.0",
  "services": {
    "database": "connected",
    "api": "running"
  }
}
```
