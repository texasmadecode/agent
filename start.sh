#!/bin/bash

# Quick Docker Start Script for Marketing Agent

echo "🚀 Starting Marketing Agent with Docker..."

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys before running again!"
    echo "   Required: OPENAI_API_KEY"
    echo "   Optional: Social media API keys for full functionality"
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "🏗️  Building and starting services..."
docker-compose up --build -d

echo "⏳ Waiting for services to start..."
sleep 15

# Check if services are healthy
if docker-compose ps | grep -q "Up.*healthy"; then
    echo "✅ Marketing Agent is running!"
    echo ""
    echo "🌐 Access your application:"
    echo "   • Main App: http://localhost:8000"
    echo "   • API Docs: http://localhost:8000/docs"
    echo "   • Health Check: http://localhost:8000/health"
    echo ""
    echo "🛠️  Useful commands:"
    echo "   • View logs: docker-compose logs -f"
    echo "   • Stop services: docker-compose down"
    echo "   • Restart: docker-compose restart"
else
    echo "❌ Some services failed to start properly."
    echo "📋 Check status: docker-compose ps"
    echo "📝 View logs: docker-compose logs"
fi
