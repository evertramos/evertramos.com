#!/bin/bash

# Run all tests
echo "🧪 Running Ezyba test suite..."

# Backend tests
echo "📋 Running backend tests..."
cd backend
python -m pytest tests/ -v --cov=app --cov-report=html
BACKEND_EXIT_CODE=$?

# Frontend tests (when implemented)
echo "🎨 Frontend tests..."
cd ../frontend
# npm test (uncomment when tests are added)
FRONTEND_EXIT_CODE=0

cd ..

# Security check
echo "🔒 Security check..."
echo "✅ Checking for hardcoded secrets..."
if grep -r "sk_live_\|pk_live_\|sk_test_\|pk_test_" --exclude-dir=node_modules --exclude-dir=.git --exclude="*.md" .; then
    echo "❌ Found potential hardcoded secrets!"
    exit 1
else
    echo "✅ No hardcoded secrets found"
fi

# Check if all tests passed
if [ $BACKEND_EXIT_CODE -eq 0 ] && [ $FRONTEND_EXIT_CODE -eq 0 ]; then
    echo "🎉 All tests passed!"
    exit 0
else
    echo "❌ Some tests failed!"
    exit 1
fi