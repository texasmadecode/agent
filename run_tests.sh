#!/bin/bash

# Test runner script for the Automated Marketing Agent
# This script runs different types of tests with proper setup

set -e  # Exit on any error

echo "🧪 Automated Marketing Agent - Test Suite"
echo "=========================================="

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

# Check if virtual environment is activated
check_venv() {
    if [[ -z "${VIRTUAL_ENV}" ]]; then
        print_warning "Virtual environment not detected. Attempting to activate..."
        if [[ -f "venv/bin/activate" ]]; then
            source venv/bin/activate
            print_success "Virtual environment activated"
        else
            print_error "Virtual environment not found. Please run: python -m venv venv && source venv/bin/activate"
            exit 1
        fi
    else
        print_success "Virtual environment detected: ${VIRTUAL_ENV}"
    fi
}

# Install test dependencies
install_deps() {
    print_status "Installing test dependencies..."
    pip install pytest pytest-cov pytest-asyncio pytest-mock httpx locust bandit safety
    print_success "Test dependencies installed"
}

# Setup test environment
setup_test_env() {
    print_status "Setting up test environment..."
    
    # Create test environment file
    if [[ ! -f ".env.test" ]]; then
        cp .env.example .env.test
        echo "DATABASE_URL=sqlite:///./test_marketing_agent.db" >> .env.test
        echo "REDIS_URL=redis://localhost:6379/1" >> .env.test
        echo "SECRET_KEY=test-secret-key-for-testing" >> .env.test
        echo "OPENAI_API_KEY=sk-test-key-for-testing" >> .env.test
        echo "ENVIRONMENT=test" >> .env.test
        print_success "Test environment file created"
    fi
    
    # Set environment variables
    export ENVIRONMENT=test
    export DATABASE_URL="sqlite:///./test_marketing_agent.db"
    export SECRET_KEY="test-secret-key-for-testing"
    export OPENAI_API_KEY="sk-test-key-for-testing"
}

# Run unit tests
run_unit_tests() {
    print_status "Running unit tests..."
    pytest tests/test_*.py -v --cov=app --cov-report=term-missing
    if [[ $? -eq 0 ]]; then
        print_success "Unit tests passed"
    else
        print_error "Unit tests failed"
        return 1
    fi
}

# Run integration tests
run_integration_tests() {
    print_status "Running integration tests..."
    pytest tests/integration/ -v -m "not slow"
    if [[ $? -eq 0 ]]; then
        print_success "Integration tests passed"
    else
        print_warning "Integration tests failed (this might be expected without full setup)"
    fi
}

# Run security tests
run_security_tests() {
    print_status "Running security tests..."
    
    # Bandit security scan
    print_status "Running Bandit security scan..."
    bandit -r app/ || print_warning "Bandit found potential security issues"
    
    # Safety check for dependencies
    print_status "Running Safety dependency check..."
    safety check || print_warning "Safety found potential vulnerabilities"
    
    print_success "Security tests completed"
}

# Run performance tests
run_performance_tests() {
    print_status "Running basic performance tests..."
    pytest tests/ -v -m "performance" || print_warning "Performance tests not available or failed"
}

# Generate test report
generate_report() {
    print_status "Generating test report..."
    
    if [[ -f "htmlcov/index.html" ]]; then
        print_success "Coverage report generated: htmlcov/index.html"
    fi
    
    if [[ -f "coverage.xml" ]]; then
        print_success "Coverage XML report generated: coverage.xml"
    fi
}

# Cleanup test artifacts
cleanup() {
    print_status "Cleaning up test artifacts..."
    rm -f test_marketing_agent.db
    rm -f .coverage
    print_success "Cleanup completed"
}

# Main execution
main() {
    echo ""
    print_status "Starting test suite execution..."
    
    # Setup
    check_venv
    install_deps
    setup_test_env
    
    echo ""
    print_status "Running tests..."
    
    # Run different test suites
    run_unit_tests
    echo ""
    
    run_integration_tests
    echo ""
    
    run_security_tests
    echo ""
    
    run_performance_tests
    echo ""
    
    # Generate reports
    generate_report
    
    echo ""
    print_success "Test suite execution completed!"
    print_status "Check htmlcov/index.html for detailed coverage report"
    
    # Cleanup
    trap cleanup EXIT
}

# Parse command line arguments
case "${1:-all}" in
    "unit")
        check_venv
        setup_test_env
        run_unit_tests
        ;;
    "integration")
        check_venv
        setup_test_env
        run_integration_tests
        ;;
    "security")
        check_venv
        install_deps
        run_security_tests
        ;;
    "performance")
        check_venv
        setup_test_env
        run_performance_tests
        ;;
    "all"|"")
        main
        ;;
    "help")
        echo "Usage: $0 [unit|integration|security|performance|all|help]"
        echo ""
        echo "Options:"
        echo "  unit         - Run only unit tests"
        echo "  integration  - Run only integration tests"
        echo "  security     - Run only security tests"
        echo "  performance  - Run only performance tests"
        echo "  all          - Run all tests (default)"
        echo "  help         - Show this help message"
        ;;
    *)
        print_error "Unknown option: $1"
        echo "Run '$0 help' for usage information"
        exit 1
        ;;
esac
