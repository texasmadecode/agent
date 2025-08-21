#!/usr/bin/env python3
"""
API Key Configuration Helper for Marketing Agent

This script helps users configure their API keys interactively.
"""

import os
import sys
import re
from typing import Dict, Optional


class APIKeyManager:
    """Manages API key configuration for the Marketing Agent."""
    
    def __init__(self, env_file: str = ".env"):
        self.env_file = env_file
        self.env_vars = {}
        self.load_env_file()
    
    def load_env_file(self):
        """Load existing environment variables from .env file."""
        if os.path.exists(self.env_file):
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        self.env_vars[key.strip()] = value.strip()
    
    def update_env_var(self, key: str, value: str):
        """Update an environment variable."""
        self.env_vars[key] = value
    
    def save_env_file(self):
        """Save environment variables back to .env file."""
        # Read the template to preserve structure and comments
        template_lines = []
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as f:
                template_lines = f.readlines()
        
        # Update the template with our values
        output_lines = []
        for line in template_lines:
            if '=' in line and not line.strip().startswith('#'):
                key = line.split('=')[0].strip()
                if key in self.env_vars:
                    # Replace with our value
                    output_lines.append(f"{key}={self.env_vars[key]}\n")
                else:
                    output_lines.append(line)
            else:
                output_lines.append(line)
        
        # Write to .env file
        with open(self.env_file, 'w') as f:
            f.writelines(output_lines)
    
    def get_current_value(self, key: str) -> str:
        """Get current value of an environment variable."""
        return self.env_vars.get(key, "")
    
    def is_configured(self, key: str) -> bool:
        """Check if an API key is already configured."""
        value = self.get_current_value(key)
        return value and not value.startswith('your-') and not value.startswith('sk-your-')


def print_header(text: str):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_section(text: str):
    """Print a formatted section header."""
    print(f"\n--- {text} ---")


def validate_openai_key(key: str) -> bool:
    """Validate OpenAI API key format."""
    return key.startswith('sk-') and len(key) > 20


def get_user_input(prompt: str, current_value: str = "", required: bool = False) -> Optional[str]:
    """Get user input with validation."""
    if current_value:
        prompt += f" (current: {current_value[:10]}...)"
    
    while True:
        value = input(f"{prompt}: ").strip()
        
        if not value:
            if required and not current_value:
                print("This field is required. Please enter a value.")
                continue
            return None
        
        return value


def setup_openai_api():
    """Setup OpenAI API key."""
    print_section("OpenAI API Configuration")
    print("OpenAI is required for AI-powered content generation.")
    print("Get your API key from: https://platform.openai.com/api-keys")
    print("The key should start with 'sk-'")
    
    manager = APIKeyManager()
    current = manager.get_current_value('OPENAI_API_KEY')
    
    if manager.is_configured('OPENAI_API_KEY'):
        print(f"✅ OpenAI API key is already configured")
        update = input("Do you want to update it? (y/N): ").lower().startswith('y')
        if not update:
            return manager
    
    while True:
        key = get_user_input("Enter your OpenAI API key", current, required=True)
        if key and validate_openai_key(key):
            manager.update_env_var('OPENAI_API_KEY', key)
            print("✅ OpenAI API key configured successfully")
            break
        elif key:
            print("❌ Invalid OpenAI API key format. It should start with 'sk-'")
        else:
            break
    
    return manager


def setup_social_media_apis(manager: APIKeyManager):
    """Setup social media API keys."""
    print_section("Social Media API Configuration")
    print("These are optional but required for posting to respective platforms.")
    
    apis = {
        'Facebook/Instagram': {
            'FACEBOOK_APP_ID': {
                'name': 'Facebook App ID',
                'url': 'https://developers.facebook.com/',
                'description': 'Required for Facebook and Instagram posting'
            },
            'FACEBOOK_APP_SECRET': {
                'name': 'Facebook App Secret',
                'url': 'https://developers.facebook.com/',
                'description': 'Required for Facebook and Instagram posting'
            }
        },
        'Twitter/X': {
            'TWITTER_API_KEY': {
                'name': 'Twitter API Key',
                'url': 'https://developer.twitter.com/',
                'description': 'Required for Twitter/X posting'
            },
            'TWITTER_API_SECRET': {
                'name': 'Twitter API Secret',
                'url': 'https://developer.twitter.com/',
                'description': 'Required for Twitter/X posting'
            },
            'TWITTER_BEARER_TOKEN': {
                'name': 'Twitter Bearer Token',
                'url': 'https://developer.twitter.com/',
                'description': 'Required for Twitter/X API v2'
            }
        },
        'LinkedIn': {
            'LINKEDIN_CLIENT_ID': {
                'name': 'LinkedIn Client ID',
                'url': 'https://www.linkedin.com/developers/',
                'description': 'Required for LinkedIn posting'
            },
            'LINKEDIN_CLIENT_SECRET': {
                'name': 'LinkedIn Client Secret',
                'url': 'https://www.linkedin.com/developers/',
                'description': 'Required for LinkedIn posting'
            }
        },
        'TikTok': {
            'TIKTOK_CLIENT_KEY': {
                'name': 'TikTok Client Key',
                'url': 'https://developers.tiktok.com/',
                'description': 'Required for TikTok posting'
            },
            'TIKTOK_CLIENT_SECRET': {
                'name': 'TikTok Client Secret',
                'url': 'https://developers.tiktok.com/',
                'description': 'Required for TikTok posting'
            }
        }
    }
    
    for platform, keys in apis.items():
        print(f"\n🔹 {platform}")
        
        # Check if any keys for this platform are configured
        configured_keys = [k for k in keys.keys() if manager.is_configured(k)]
        if configured_keys:
            print(f"✅ Some {platform} keys are configured: {', '.join(configured_keys)}")
        
        setup_platform = input(f"Configure {platform} API keys? (y/N): ").lower().startswith('y')
        if not setup_platform:
            continue
        
        print(f"Get your {platform} API keys from: {list(keys.values())[0]['url']}")
        
        for key, info in keys.items():
            current = manager.get_current_value(key)
            value = get_user_input(f"Enter {info['name']}", current)
            if value:
                manager.update_env_var(key, value)
                print(f"✅ {info['name']} configured")
    
    return manager


def setup_database_config(manager: APIKeyManager):
    """Setup database configuration."""
    print_section("Database Configuration")
    print("Configure database settings (optional - defaults are provided)")
    
    db_configs = {
        'POSTGRES_DB': 'Database name',
        'POSTGRES_USER': 'Database user',
        'POSTGRES_PASSWORD': 'Database password'
    }
    
    for key, description in db_configs.items():
        current = manager.get_current_value(key)
        value = get_user_input(f"Enter {description}", current)
        if value:
            manager.update_env_var(key, value)


def generate_security_keys(manager: APIKeyManager):
    """Generate secure keys for the application."""
    import secrets
    import string
    
    print_section("Security Configuration")
    
    # Generate secret key if not set
    current_secret = manager.get_current_value('SECRET_KEY')
    if not current_secret or current_secret == 'your-super-secret-key-change-this-in-production':
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        secret_key = ''.join(secrets.choice(alphabet) for _ in range(32))
        manager.update_env_var('SECRET_KEY', secret_key)
        print("✅ Generated secure SECRET_KEY")
    else:
        print("✅ SECRET_KEY already configured")
    
    # Generate Redis password if not set
    current_redis = manager.get_current_value('REDIS_PASSWORD')
    if not current_redis or current_redis == 'redis_password_123':
        redis_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
        manager.update_env_var('REDIS_PASSWORD', redis_password)
        print("✅ Generated secure REDIS_PASSWORD")
    else:
        print("✅ REDIS_PASSWORD already configured")


def main():
    """Main configuration function."""
    print_header("Marketing Agent API Key Configuration")
    print("This tool will help you configure API keys for the Marketing Agent.")
    print("You can skip any optional configurations and set them up later.")
    
    # Ensure .env file exists
    if not os.path.exists('.env') and os.path.exists('.env.example'):
        with open('.env.example', 'r') as src, open('.env', 'w') as dst:
            dst.write(src.read())
        print("📝 Created .env file from template")
    
    # Setup OpenAI (required)
    manager = setup_openai_api()
    
    # Setup social media APIs (optional)
    setup_social = input("\nConfigure social media API keys? (y/N): ").lower().startswith('y')
    if setup_social:
        manager = setup_social_media_apis(manager)
    
    # Setup database (optional)
    setup_db = input("\nConfigure database settings? (y/N): ").lower().startswith('y')
    if setup_db:
        setup_database_config(manager)
    
    # Generate security keys
    generate_security_keys(manager)
    
    # Save configuration
    manager.save_env_file()
    
    print_header("Configuration Complete")
    print("✅ Configuration saved to .env file")
    print("\nNext steps:")
    print("1. Review the .env file if needed")
    print("2. Start the application with: ./start.sh or make up")
    print("3. Access the application at: http://localhost:8000")
    
    # Show configuration summary
    openai_configured = manager.is_configured('OPENAI_API_KEY')
    social_keys = ['FACEBOOK_APP_ID', 'TWITTER_API_KEY', 'LINKEDIN_CLIENT_ID', 'TIKTOK_CLIENT_KEY']
    social_configured = any(manager.is_configured(key) for key in social_keys)
    
    print(f"\nConfiguration Summary:")
    print(f"  OpenAI API: {'✅ Configured' if openai_configured else '❌ Not configured'}")
    print(f"  Social Media APIs: {'✅ Some configured' if social_configured else '⚠️  None configured'}")
    
    if not openai_configured:
        print("\n⚠️  OpenAI API key is required for content generation features.")
    
    if not social_configured:
        print("\n⚠️  Social media API keys are required for posting to respective platforms.")
        print("   You can configure them later by running this script again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nConfiguration cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
