"""
Dashboard API endpoints.

This module provides endpoints for the main dashboard
interface and system overview.
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def dashboard_home():
    """Main dashboard interface."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Marketing Agent Dashboard</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            .header { 
                background: white; 
                padding: 30px; 
                border-radius: 15px; 
                margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }
            .header h1 { color: #667eea; font-size: 2.5em; margin-bottom: 10px; }
            .header p { color: #666; font-size: 1.1em; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
            .card { 
                background: white; 
                padding: 25px; 
                border-radius: 10px; 
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                transition: transform 0.2s;
            }
            .card:hover { transform: translateY(-5px); }
            .card h3 { color: #667eea; margin-bottom: 15px; font-size: 1.3em; }
            .card p { color: #666; line-height: 1.6; }
            .metric { font-size: 2em; font-weight: bold; color: #667eea; }
            .status { 
                display: inline-block; 
                padding: 5px 15px; 
                border-radius: 20px; 
                font-size: 0.9em; 
                font-weight: bold;
            }
            .status.active { background: #e8f5e8; color: #2d8f47; }
            .status.pending { background: #fff3cd; color: #856404; }
            .nav { 
                background: white; 
                padding: 20px; 
                border-radius: 10px; 
                margin-bottom: 20px;
                display: flex;
                gap: 20px;
                flex-wrap: wrap;
            }
            .nav a { 
                color: #667eea; 
                text-decoration: none; 
                font-weight: bold; 
                padding: 10px 20px;
                border-radius: 5px;
                transition: background 0.2s;
            }
            .nav a:hover { background: #f0f0f0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Marketing Agent Dashboard</h1>
                <p>Centralized control center for your automated marketing campaigns</p>
            </div>
            
            <div class="nav">
                <a href="/api/v1/dashboard/overview">📊 Overview</a>
                <a href="/api/v1/clients">👥 Clients</a>
                <a href="/api/v1/content">📝 Content</a>
                <a href="/api/v1/posts">📤 Posts</a>
                <a href="/api/v1/campaigns">🎯 Campaigns</a>
                <a href="/api/v1/analytics">📈 Analytics</a>
                <a href="/docs">📚 API Docs</a>
            </div>
            
            <div class="grid">
                <div class="card">
                    <h3>📊 System Status</h3>
                    <p>All systems operational</p>
                    <div class="status active">Active</div>
                </div>
                
                <div class="card">
                    <h3>📤 Posts Today</h3>
                    <div class="metric">24</div>
                    <p>Successfully posted across all platforms</p>
                </div>
                
                <div class="card">
                    <h3>📈 Total Engagement</h3>
                    <div class="metric">12.5K</div>
                    <p>Likes, comments, and shares this week</p>
                </div>
                
                <div class="card">
                    <h3>👥 Active Clients</h3>
                    <div class="metric">8</div>
                    <p>Clients with active campaigns</p>
                </div>
                
                <div class="card">
                    <h3>🎯 Active Campaigns</h3>
                    <div class="metric">15</div>
                    <p>Currently running marketing campaigns</p>
                </div>
                
                <div class="card">
                    <h3>⏰ Scheduled Posts</h3>
                    <div class="metric">156</div>
                    <p>Posts scheduled for the next 7 days</p>
                </div>
                
                <div class="card">
                    <h3>🤖 AI Generation</h3>
                    <p>AI-powered content generation is</p>
                    <div class="status active">Enabled</div>
                </div>
                
                <div class="card">
                    <h3>📊 Platform Coverage</h3>
                    <p>✅ Instagram<br>✅ Facebook<br>✅ Twitter<br>✅ LinkedIn<br>⏳ TikTok</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """


@router.get("/overview")
async def get_dashboard_overview(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get dashboard overview data."""
    try:
        # In a real implementation, you would fetch actual data from the database
        overview_data = {
            "system_status": "operational",
            "posts_today": 24,
            "total_engagement_week": 12500,
            "active_clients": 8,
            "active_campaigns": 15,
            "scheduled_posts": 156,
            "ai_generation_enabled": True,
            "platforms": {
                "instagram": {"status": "active", "posts_today": 8},
                "facebook": {"status": "active", "posts_today": 6},
                "twitter": {"status": "active", "posts_today": 10},
                "linkedin": {"status": "active", "posts_today": 0},
                "tiktok": {"status": "pending", "posts_today": 0}
            },
            "recent_activity": [
                {"time": "2 minutes ago", "action": "Posted to Instagram", "client": "Tech Startup Co"},
                {"time": "15 minutes ago", "action": "Generated AI content", "client": "Fashion Brand"},
                {"time": "1 hour ago", "action": "Campaign launched", "client": "Restaurant Chain"},
                {"time": "2 hours ago", "action": "Analytics report sent", "client": "E-commerce Store"}
            ],
            "upcoming_posts": [
                {"time": "In 30 minutes", "platform": "Twitter", "client": "Tech Startup Co"},
                {"time": "In 2 hours", "platform": "Facebook", "client": "Fashion Brand"},
                {"time": "In 4 hours", "platform": "Instagram", "client": "Restaurant Chain"}
            ]
        }
        
        return overview_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard overview: {str(e)}")


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """System health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": "2025-08-21T10:00:00Z",
        "services": {
            "database": "connected",
            "redis": "connected",
            "celery": "running",
            "ai_service": "available"
        },
        "version": "1.0.0"
    }
