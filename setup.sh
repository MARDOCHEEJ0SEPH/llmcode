#!/bin/bash

# LLMCode Setup Script

set -e

echo "🚀 Setting up LLMCode..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install package in development mode
echo "Installing LLMCode..."
pip install -e .

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  Please edit .env and add your ANTHROPIC_API_KEY"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To get started:"
echo "  1. Edit .env and add your ANTHROPIC_API_KEY"
echo "  2. Activate the virtual environment: source venv/bin/activate"
echo "  3. Run: llmcode"
echo ""
