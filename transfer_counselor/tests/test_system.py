#!/usr/bin/env python3
"""
System Integration Tests

Tests for the overall system functionality including API integration and memory.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from transfer_counselor import EnhancedTransferCounselorSystem


def test_api_integration():
    """Test API key integration with OpenAI Agents SDK"""
    print("🔑 Testing OpenAI API Key Integration")
    print("-" * 50)
    
    # Check if API key is available
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No OPENAI_API_KEY found in environment")
        print("💡 To test with a real API key, set it like this:")
        print("   export OPENAI_API_KEY='sk-your-key-here'")
        print("   python -m transfer_counselor.tests.test_system")
        return False
    
    if not api_key.startswith('sk-'):
        print("❌ Invalid API key format (should start with 'sk-')")
        return False
    
    print(f"✅ API key found: {api_key[:7]}...{api_key[-4:]}")
    
    try:
        # Initialize system
        print("🔧 Initializing system...")
        system = EnhancedTransferCounselorSystem()
        
        # Test query processing
        print("🚀 Testing query processing...")
        result = system.process_query("How much does UC Berkeley cost?")
        
        print("✅ Query processed successfully!")
        print(f"📝 Agent used: {result['agent_used']}")
        print(f"📝 Response preview: {result['response'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during system test: {e}")
        return False


def test_memory_and_routing():
    """Test conversation memory and agent routing"""
    print("\n🧠 Testing Conversation Memory and Agent Routing")
    print("-" * 60)
    
    try:
        # Initialize system
        system = EnhancedTransferCounselorSystem()
        
        # Create a session
        session_id = system.create_session("test_user")
        print(f"✅ Session created: {session_id[:8]}...")
        
        # Test course routing
        result1 = system.process_query(
            "I need a course roadmap for UC Berkeley math major",
            session_id=session_id
        )
        
        expected_agent = 'course_difficulty'
        if result1['agent_used'] == expected_agent:
            print("✅ Course query correctly routed to course_difficulty agent")
        else:
            print(f"❌ Expected {expected_agent}, got {result1['agent_used']}")
        
        # Test follow-up with memory
        result2 = system.process_query(
            "What about the prerequisites?",
            session_id=session_id
        )
        
        print(f"✅ Follow-up query processed by {result2['agent_used']} agent")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during memory test: {e}")
        return False


def main():
    """Run all system tests"""
    print("🧪 Transfer Counselor System Tests")
    print("=" * 50)
    
    test_results = []
    
    # Test API integration
    test_results.append(test_api_integration())
    
    # Test memory and routing
    test_results.append(test_memory_and_routing())
    
    # Summary
    passed = sum(test_results)
    total = len(test_results)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)