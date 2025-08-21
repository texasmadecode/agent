<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Automated Marketing Agent - Copilot Instructions

## Project Context
This is an automated marketing agent system built with Python, FastAPI, and Celery. The system manages social media content across multiple platforms, provides AI-powered content generation, handles scheduling and automation, and offers comprehensive analytics and reporting.

## Architecture Guidelines
- Use async/await patterns for I/O operations
- Implement proper error handling and logging
- Follow the Repository pattern for data access
- Use dependency injection for services
- Implement proper API versioning
- Use Pydantic models for data validation

## Code Style Preferences
- Follow PEP 8 for Python code formatting
- Use type hints for all function parameters and return values
- Write comprehensive docstrings for classes and methods
- Use descriptive variable and function names
- Implement proper exception handling

## Key Components
1. **Content Management**: Handle various content types (text, images, videos)
2. **AI Integration**: Use OpenAI API for content generation and optimization
3. **Social Media APIs**: Integrate with multiple platform APIs
4. **Scheduling System**: Use Celery for background task processing
5. **Analytics Engine**: Track and analyze engagement metrics
6. **Security Layer**: Encrypt credentials and ensure data privacy

## Database Design
- Use SQLAlchemy ORM with PostgreSQL
- Implement proper database migrations with Alembic
- Design efficient indexing strategies
- Use relationship mapping for associated data

## API Design
- Follow RESTful principles
- Implement proper HTTP status codes
- Use consistent response formats
- Include comprehensive error messages
- Implement rate limiting and authentication

## Testing Strategy
- Write unit tests for all business logic
- Implement integration tests for API endpoints
- Use mocking for external service calls
- Maintain high test coverage

## Security Considerations
- Never hardcode API keys or sensitive data
- Use environment variables for configuration
- Implement proper authentication and authorization
- Encrypt sensitive data in the database
- Validate all user inputs

## Performance Optimization
- Use connection pooling for database operations
- Implement caching strategies where appropriate
- Optimize database queries to avoid N+1 problems
- Use background tasks for time-consuming operations
