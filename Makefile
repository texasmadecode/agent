# Marketing Agent Makefile
# Provides convenient commands for development and deployment

.PHONY: help build up down logs shell test clean setup dev

# Default target
help:
	@echo "Marketing Agent - Available Commands:"
	@echo ""
	@echo "🚀 Quick Start:"
	@echo "  make setup     - Run interactive setup"
	@echo "  make up        - Start all services"
	@echo "  make dev       - Start development environment"
	@echo ""
	@echo "🐳 Docker Commands:"
	@echo "  make build     - Build Docker images"
	@echo "  make down      - Stop all services"
	@echo "  make restart   - Restart all services"
	@echo "  make logs      - View application logs"
	@echo "  make shell     - Access application shell"
	@echo ""
	@echo "🛠️  Development:"
	@echo "  make install   - Install Python dependencies"
	@echo "  make migrate   - Run database migrations"
	@echo "  make init-db   - Initialize database with sample data"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  make test      - Run all tests"
	@echo "  make test-unit - Run unit tests only"
	@echo "  make test-integration - Run integration tests only"
	@echo "  make test-security - Run security tests only"
	@echo "  make test-performance - Run performance tests only"
	@echo "  make test-coverage - Run tests with coverage report"
	@echo "  make test-watch - Run tests in watch mode"
	@echo ""
	@echo "🧹 Maintenance:"
	@echo "  make clean     - Clean up Docker resources"
	@echo "  make reset     - Reset everything (⚠️  destroys data)"

# Setup and configuration
setup:
	@echo "🔧 Running interactive setup..."
	@./setup.sh

# Quick development start
dev:
	@echo "🚀 Starting development environment..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "📝 Created .env file - please configure your API keys"; fi
	@docker-compose -f docker-compose.dev.yml up --build

# Docker operations
build:
	@echo "🏗️  Building Docker images..."
	@docker-compose build

up:
	@echo "🚀 Starting all services..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "📝 Created .env file - please configure your API keys"; fi
	@docker-compose up -d
	@echo "✅ Services started. Access at http://localhost:8000"

down:
	@echo "🛑 Stopping all services..."
	@docker-compose down

restart:
	@echo "🔄 Restarting services..."
	@docker-compose restart

logs:
	@echo "📋 Viewing logs (Ctrl+C to exit)..."
	@docker-compose logs -f

shell:
	@echo "🐚 Accessing application shell..."
	@docker-compose exec api bash

# Development commands
install:
	@echo "📦 Installing Python dependencies..."
	@python -m pip install --upgrade pip
	@pip install -r requirements.txt

migrate:
	@echo "📊 Running database migrations..."
	@if [ -f venv/bin/activate ]; then \
		. venv/bin/activate && alembic upgrade head; \
	else \
		docker-compose exec api alembic upgrade head; \
	fi

init-db:
	@echo "🗃️  Initializing database..."
	@if [ -f venv/bin/activate ]; then \
		. venv/bin/activate && python -m app.core.init_db; \
	else \
		docker-compose exec api python -m app.core.init_db; \
	fi

# Testing commands
test:
	@echo "🧪 Running all tests..."
	@./run_tests.sh all

test-unit:
	@echo "🧪 Running unit tests..."
	@./run_tests.sh unit

test-integration:
	@echo "🧪 Running integration tests..."
	@./run_tests.sh integration

test-security:
	@echo "🔒 Running security tests..."
	@./run_tests.sh security

test-performance:
	@echo "⚡ Running performance tests..."
	@./run_tests.sh performance

test-coverage:
	@echo "📊 Running tests with coverage report..."
	@if [ -f venv/bin/activate ]; then \
		. venv/bin/activate && pytest --cov=app --cov-report=html --cov-report=term; \
	else \
		docker-compose exec api pytest --cov=app --cov-report=html --cov-report=term; \
	fi

test-watch:
	@echo "👀 Running tests in watch mode..."
	@if [ -f venv/bin/activate ]; then \
		. venv/bin/activate && pytest-watch; \
	else \
		echo "❌ Watch mode only available in local development"; \
	fi

test-docker:
	@echo "🐳 Running tests in Docker..."
	@docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
	@docker-compose -f docker-compose.test.yml down

# Maintenance
clean:
	@echo "🧹 Cleaning up Docker resources..."
	@docker-compose down -v --remove-orphans
	@docker system prune -f

reset:
	@echo "⚠️  This will destroy all data! Are you sure? [y/N]" && read ans && [ $${ans:-N} = y ]
	@echo "🗑️  Resetting everything..."
	@docker-compose down -v --remove-orphans
	@docker volume prune -f
	@rm -f marketing_agent.db .env
	@echo "✅ Reset complete. Run 'make setup' to start fresh."

# Status and health checks
status:
	@echo "📊 Service Status:"
	@docker-compose ps
	@echo ""
	@echo "🏥 Health Check:"
	@curl -s http://localhost:8000/health | python -m json.tool 2>/dev/null || echo "Service not responding"

# Production deployment
deploy:
	@echo "🚀 Deploying to production..."
	@docker-compose -f docker-compose.yml up -d --build
	@echo "✅ Production deployment complete"
