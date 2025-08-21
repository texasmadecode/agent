"""
Automated Marketing Agent - Main Application Entry Point

This module sets up the FastAPI application with all necessary middleware,
routers, and configuration for the automated marketing agent system.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import logging
import os
from datetime import datetime

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import api_router
from app.core.security import get_current_user


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown events."""
    # Startup
    logger.info("Starting Automated Marketing Agent...")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
    
    # Create upload directory if it doesn't exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    logger.info(f"Upload directory ensured: {settings.UPLOAD_DIR}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Automated Marketing Agent...")


# Create FastAPI application
app = FastAPI(
    title="Automated Marketing Agent",
    description="A comprehensive system for automated social media content management and marketing",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and load balancers."""
    try:
        # Test database connection
        from app.core.database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "services": {
                "database": "connected",
                "api": "running"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint serving the main dashboard."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Automated Marketing Agent</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                     color: white; padding: 20px; border-radius: 10px; margin-bottom: 30px; }
            .feature { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #667eea; }
            .links { margin: 20px 0; }
            .links a { margin-right: 20px; color: #667eea; text-decoration: none; font-weight: bold; }
            .links a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🚀 Automated Marketing Agent</h1>
            <p>Streamline your social media marketing with AI-powered automation</p>
        </div>
        
        <div class="feature">
            <h3>📊 Multi-Platform Management</h3>
            <p>Schedule and post content across Instagram, Facebook, LinkedIn, Twitter, and TikTok</p>
        </div>
        
        <div class="feature">
            <h3>🤖 AI-Powered Content Generation</h3>
            <p>Generate engaging captions, hashtags, and content optimized for each platform</p>
        </div>
        
        <div class="feature">
            <h3>📈 Analytics & Reporting</h3>
            <p>Track engagement metrics and get AI-powered insights for better performance</p>
        </div>
        
        <div class="feature">
            <h3>🔐 Secure & Compliant</h3>
            <p>Enterprise-grade security with encrypted credential storage and compliance checks</p>
        </div>
        
        <div class="links">
            <a href="/docs">📚 API Documentation</a>
            <a href="/api/v1/dashboard">📊 Dashboard</a>
            <a href="/api/v1/health">🏥 Health Check</a>
        </div>
    </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "Automated Marketing Agent is running",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
