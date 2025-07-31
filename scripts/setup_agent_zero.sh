#!/bin/bash
# Agent-Zero Oracle Memory Integration Setup Script

echo "🤖 Agent-Zero Oracle Memory Integration Setup"
echo "=============================================="

# Check if Oracle URL is set
if [ -z "$ORACLE_BASE_URL" ]; then
    echo "❌ ORACLE_BASE_URL environment variable not set"
    echo "   Please set it to your Oracle Cloud pre-authenticated URL"
    echo "   Example: export ORACLE_BASE_URL='https://objectstorage.region.oraclecloud.com/p/TOKEN/n/NAMESPACE/b/BUCKET/o/'"
    exit 1
fi

echo "✅ Oracle URL configured: ${ORACLE_BASE_URL:0:50}..."

# Check Python and dependencies
echo ""
echo "🐍 Checking Python environment..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Install required packages
echo ""
echo "📦 Installing required Python packages..."
pip3 install requests

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Test Oracle connection
echo ""
echo "🌐 Testing Oracle Cloud connection..."

python3 -c "
import requests
import os
import sys

oracle_url = os.getenv('ORACLE_BASE_URL')
test_url = f'{oracle_url}test-connection.txt'

try:
    # Test upload
    response = requests.put(test_url, data='Hello from Agent-Zero setup!', timeout=10)
    if response.status_code in [200, 201]:
        print('✅ Upload test successful')
        
        # Test download
        response = requests.get(test_url, timeout=10)
        if response.status_code == 200:
            print('✅ Download test successful')
            print('✅ Oracle Cloud connection working!')
        else:
            print(f'❌ Download test failed: {response.status_code}')
            sys.exit(1)
    else:
        print(f'❌ Upload test failed: {response.status_code}')
        sys.exit(1)
        
except Exception as e:
    print(f'❌ Connection test failed: {e}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Oracle connection test failed"
    echo "   Please check your ORACLE_BASE_URL and Oracle Cloud setup"
    exit 1
fi

# Create example configuration
echo ""
echo "📝 Creating example configuration..."

cat > agent_zero_config.py << 'EOF'
#!/usr/bin/env python3
"""
Agent-Zero Oracle Memory Configuration
Copy and modify this file for your Agent-Zero setup
"""

import os
from examples.agent_zero_oracle_adapter import AgentZeroWithOracle

# Oracle Cloud configuration
ORACLE_BASE_URL = os.getenv("ORACLE_BASE_URL")

# Initialize Agent-Zero with Oracle memory
def create_agent():
    """Create Agent-Zero instance with Oracle memory"""
    return AgentZeroWithOracle(ORACLE_BASE_URL)

# Example usage
if __name__ == "__main__":
    agent = create_agent()
    agent.show_memory_stats()
    
    # Your Agent-Zero code here
    print("🤖 Agent-Zero ready with Oracle Cloud memory!")
EOF

echo "✅ Created agent_zero_config.py"

# Test the example adapter
echo ""
echo "🧪 Testing Agent-Zero Oracle adapter..."

if [ -f "examples/agent_zero_oracle_adapter.py" ]; then
    cd examples
    python3 agent_zero_oracle_adapter.py
    cd ..
    
    if [ $? -eq 0 ]; then
        echo "✅ Agent-Zero Oracle adapter test successful!"
    else
        echo "❌ Agent-Zero Oracle adapter test failed"
        exit 1
    fi
else
    echo "❌ Agent-Zero Oracle adapter not found"
    echo "   Please ensure examples/agent_zero_oracle_adapter.py exists"
    exit 1
fi

echo ""
echo "🎉 Agent-Zero Oracle Memory Integration Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Copy agent_zero_config.py to your Agent-Zero project"
echo "2. Import and use AgentZeroWithOracle in your code"
echo "3. Enjoy shared AI memory across all your agents!"
echo ""
echo "📚 For detailed integration guide, see AGENT_ZERO_INTEGRATION.md"
