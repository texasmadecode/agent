#!/bin/bash

# Marketing Agent Setup Script
# This script helps you set up the Marketing Agent application quickly

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo ""
    echo -e "${BLUE}============================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}============================================${NC}"
    echo ""
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker and try again."
        echo "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose and try again."
        echo "Visit: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed"
}

# Create .env file from template
setup_env_file() {
    print_header "Environment Configuration"
    
    if [ -f ".env" ]; then
        print_warning ".env file already exists. Backing up to .env.backup"
        cp .env .env.backup
    fi
    
    print_status "Creating .env file from template..."
    cp .env.example .env
    
    echo ""
    echo "Please edit the .env file to add your API keys:"
    echo ""
    echo "Required API Keys:"
    echo "- OPENAI_API_KEY: Get from https://platform.openai.com/api-keys"
    echo ""
    echo "Optional Social Media API Keys (for full functionality):"
    echo "- Facebook/Instagram: https://developers.facebook.com/"
    echo "- Twitter/X: https://developer.twitter.com/"
    echo "- LinkedIn: https://www.linkedin.com/developers/"
    echo "- TikTok: https://developers.tiktok.com/"
    echo ""
    
    read -p "Do you want to open the .env file for editing now? (y/N): " edit_env
    if [[ $edit_env =~ ^[Yy]$ ]]; then
        if command -v code &> /dev/null; then
            code .env
        elif command -v nano &> /dev/null; then
            nano .env
        elif command -v vim &> /dev/null; then
            vim .env
        else
            print_warning "No suitable editor found. Please edit .env manually."
        fi
    fi
}

# API Key Setup Helper
setup_api_keys() {
    print_header "API Key Setup Helper"
    
    echo "This helper will guide you through setting up the most important API keys."
    echo ""
    
    # OpenAI API Key
    echo -e "${YELLOW}OpenAI API Key (Required for AI content generation):${NC}"
    echo "1. Go to https://platform.openai.com/api-keys"
    echo "2. Create a new API key"
    echo "3. Copy the key (starts with 'sk-')"
    echo ""
    read -p "Enter your OpenAI API key (or press Enter to skip): " openai_key
    
    if [ ! -z "$openai_key" ]; then
        sed -i.bak "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$openai_key/" .env
        print_success "OpenAI API key updated"
    fi
    
    echo ""
    echo -e "${YELLOW}Social Media API Keys (Optional but recommended):${NC}"
    echo ""
    
    # Facebook API
    echo "Facebook/Instagram API:"
    echo "1. Go to https://developers.facebook.com/"
    echo "2. Create a new app"
    echo "3. Get App ID and App Secret"
    echo ""
    read -p "Enter Facebook App ID (or press Enter to skip): " fb_id
    read -p "Enter Facebook App Secret (or press Enter to skip): " fb_secret
    
    if [ ! -z "$fb_id" ]; then
        sed -i.bak "s/FACEBOOK_APP_ID=.*/FACEBOOK_APP_ID=$fb_id/" .env
    fi
    if [ ! -z "$fb_secret" ]; then
        sed -i.bak "s/FACEBOOK_APP_SECRET=.*/FACEBOOK_APP_SECRET=$fb_secret/" .env
    fi
    
    echo ""
    echo "For additional social media platforms, please edit the .env file manually."
    echo "Detailed setup instructions are provided in the README.md file."
}

# Build and start the application
start_application() {
    print_header "Starting Marketing Agent"
    
    print_status "Building Docker images..."
    docker-compose build
    
    print_status "Starting services..."
    docker-compose up -d
    
    print_status "Waiting for services to start..."
    sleep 10
    
    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        print_success "Application started successfully!"
        echo ""
        echo "Access your application at:"
        echo "- Main Application: http://localhost:8000"
        echo "- API Documentation: http://localhost:8000/docs"
        echo "- Interactive API Docs: http://localhost:8000/redoc"
        echo ""
        echo "Database connection:"
        echo "- PostgreSQL: localhost:5432"
        echo "- Redis: localhost:6379"
        echo ""
        echo "To view logs: docker-compose logs -f"
        echo "To stop: docker-compose down"
    else
        print_error "Some services failed to start. Check logs with: docker-compose logs"
    fi
}

# Development mode setup
setup_development() {
    print_header "Development Mode Setup"
    
    print_status "Setting up Python virtual environment..."
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.8+ and try again."
        exit 1
    fi
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
    
    # Activate virtual environment and install dependencies
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    
    print_success "Dependencies installed"
    
    # Setup local database (SQLite for development)
    print_status "Setting up local development database..."
    python -m app.core.init_db
    
    print_success "Development environment ready!"
    echo ""
    echo "To start development server:"
    echo "1. source venv/bin/activate"
    echo "2. python -m uvicorn app.main:app --reload"
    echo ""
    echo "Or use VS Code tasks (Ctrl+Shift+P -> Tasks: Run Task)"
}

# Main menu
show_menu() {
    echo ""
    echo -e "${GREEN}=== Marketing Agent Setup ===${NC}"
    echo ""
    echo "Choose setup mode:"
    echo "1) Docker Setup (Recommended for production)"
    echo "2) Development Setup (Local Python environment)"
    echo "3) API Key Configuration Helper"
    echo "4) View Application Status"
    echo "5) Stop Application"
    echo "6) Exit"
    echo ""
}

# Application status
show_status() {
    print_header "Application Status"
    
    if docker-compose ps &> /dev/null; then
        echo "Docker services:"
        docker-compose ps
        echo ""
        
        # Check if main service is responding
        if curl -s http://localhost:8000/health &> /dev/null; then
            print_success "Application is running and responding"
            echo "Access at: http://localhost:8000"
        else
            print_warning "Application is starting or not responding"
        fi
    else
        print_warning "Docker Compose services not found"
    fi
    
    if [ -f "venv/bin/activate" ]; then
        print_status "Development environment detected"
    fi
}

# Stop application
stop_application() {
    print_header "Stopping Application"
    
    if docker-compose ps &> /dev/null; then
        docker-compose down
        print_success "Docker services stopped"
    else
        print_warning "No Docker services running"
    fi
}

# Main script
main() {
    print_header "Marketing Agent Setup"
    
    while true; do
        show_menu
        read -p "Enter your choice (1-6): " choice
        
        case $choice in
            1)
                check_docker
                setup_env_file
                setup_api_keys
                start_application
                ;;
            2)
                setup_env_file
                setup_api_keys
                setup_development
                ;;
            3)
                if [ ! -f ".env" ]; then
                    cp .env.example .env
                fi
                setup_api_keys
                ;;
            4)
                show_status
                ;;
            5)
                stop_application
                ;;
            6)
                print_success "Setup complete. Happy marketing!"
                exit 0
                ;;
            *)
                print_error "Invalid choice. Please try again."
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
}

# Run main function
main
