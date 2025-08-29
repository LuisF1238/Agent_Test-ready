#!/usr/bin/env python3
"""
Transfer Counselor AI System - Main Application

A simple command-line interface to run the Enhanced Transfer Counselor Agent System.
Provides easy access to AI-powered UC/CSU transfer counseling.
"""

import sys
import os
import argparse
from typing import Optional

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  Warning: python-dotenv not installed. Install with: pip install python-dotenv")
    print("   You can still set OPENAI_API_KEY as an environment variable manually.")

try:
    from transfer_counselor import EnhancedTransferCounselorSystem
except ImportError as e:
    print("❌ Error importing Transfer Counselor System:")
    print(f"   {e}")
    print("\n💡 Make sure you've installed dependencies:")
    print("   pip install -r requirements.txt")
    sys.exit(1)


def print_banner():
    """Print welcome banner"""
    print("\n" + "="*60)
    print("🎓 Enhanced Transfer Counselor AI System v2.0.0")
    print("="*60)
    print("Your AI-powered UC/CSU transfer counseling assistant")
    print("Specialized agents for: Financial Aid | Career | Academic Support")
    print("="*60 + "\n")


def check_api_key():
    """Check if OpenAI API key is configured"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key.startswith('your-'):
        print("⚠️  OpenAI API Key Required")
        print("\n📝 Set your API key using one of these methods:")
        print("\n1. Create a .env file in this directory:")
        print("   echo 'OPENAI_API_KEY=your-actual-api-key-here' > .env")
        print("\n2. Set as environment variable:")
        print("   export OPENAI_API_KEY='your-actual-api-key-here'")
        print("\n3. Edit config.yaml with your key")
        print("\n💡 The .env file method is recommended for easy setup!")
        return False
    print("✅ API key loaded successfully")
    return True


def run_interactive_session(user_id: Optional[str] = None):
    """Run interactive counseling session"""
    print("🚀 Starting interactive session...")
    print("💬 You can ask about financial aid, career guidance, or academic support")
    print("📝 Type 'help', 'stats', 'history', or 'quit' for commands\n")
    
    try:
        system = EnhancedTransferCounselorSystem()
        system.interactive_session(user_id=user_id)
    except Exception as e:
        print(f"❌ Error starting system: {e}")
        return False
    return True


def run_single_query(query: str, user_id: Optional[str] = None, session_id: Optional[str] = None):
    """Process a single query with optional session context"""
    print(f"🤔 Processing query: {query}")
    
    try:
        system = EnhancedTransferCounselorSystem()
        result = system.process_query(query, session_id=session_id, user_id=user_id)
        
        print("\n" + "="*50)
        print("🤖 AI Counselor Response:")
        print("="*50)
        print(result.get('response', 'No response received'))
        
        metadata = result.get('metadata', {})
        if 'agent_used' in result:
            print(f"\n📋 Handled by: {result['agent_used'].replace('_', ' ').title()}")
        if metadata.get('has_context'):
            print(f"💭 Context: Built on {metadata.get('conversation_turn', 1)} previous exchanges")
        if 'session_id' in result:
            print(f"🔄 Session: {result['session_id'][:8]}...")
            
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"❌ Error processing query: {e}")
        return False
    return True


def show_examples():
    """Show example queries"""
    print("💡 Example Questions You Can Ask:")
    print("\n🏦 Financial Aid:")
    print("  • How do I apply for FAFSA for UC schools?")
    print("  • What scholarships are available for transfer students?")
    print("  • Compare the costs of UCLA vs SDSU")
    
    print("\n💼 Career Guidance:")
    print("  • What career paths are available with a psychology major?")
    print("  • Should I choose UC Berkeley or Cal Poly for computer science?")
    print("  • What's the job market like for business majors?")
    
    print("\n📚 Academic Support:")
    print("  • How can I manage organic chemistry while working?")
    print("  • What study strategies work best for STEM courses?")
    print("  • Help me plan my course sequence for engineering")
    print()


def show_recent_sessions():
    """Show recent sessions for session resumption"""
    print("📋 Recent Sessions:")
    try:
        system = EnhancedTransferCounselorSystem()
        # This would need to be implemented in session manager
        print("   Feature coming soon - check sessions.db for session IDs")
    except Exception as e:
        print(f"❌ Error loading sessions: {e}")
    print()


def run_tests():
    """Run system tests"""
    print("🧪 Running system tests...")
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "transfer_counselor/tests/test_system.py", "-v"
        ], cwd=os.path.dirname(os.path.abspath(__file__)))
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description="Enhanced Transfer Counselor AI System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python app.py                              # Interactive mode
  python app.py --query "How do I apply for FAFSA?"  # Single query
  python app.py --examples                   # Show example questions
  python app.py --sessions                   # Show recent sessions
  python app.py --session-id abc123          # Resume specific session
  python app.py --user-id student123         # Track specific user
  python app.py --test                       # Run system tests
        """
    )
    
    parser.add_argument(
        '--query', '-q',
        help='Ask a single question (non-interactive mode)'
    )
    
    parser.add_argument(
        '--user-id', '-u',
        help='User ID for session tracking'
    )
    
    parser.add_argument(
        '--session-id', '-s',
        help='Resume specific session ID'
    )
    
    parser.add_argument(
        '--examples', '-e',
        action='store_true',
        help='Show example questions'
    )
    
    parser.add_argument(
        '--test', '-t',
        action='store_true',
        help='Run system tests'
    )
    
    parser.add_argument(
        '--sessions',
        action='store_true',
        help='Show recent sessions for resumption'
    )
    
    parser.add_argument(
        '--no-banner',
        action='store_true',
        help='Skip welcome banner'
    )
    
    args = parser.parse_args()
    
    # Show banner unless disabled
    if not args.no_banner:
        print_banner()
    
    # Handle special commands first
    if args.examples:
        show_examples()
        return 0
    
    if args.sessions:
        show_recent_sessions()
        return 0
    
    if args.test:
        success = run_tests()
        return 0 if success else 1
    
    # Check API key for AI operations
    if not check_api_key():
        return 1
    
    # Run the appropriate mode
    if args.query:
        success = run_single_query(args.query, args.user_id, args.session_id)
    else:
        success = run_interactive_session(args.user_id)
    
    return 0 if success else 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for using Transfer Counselor AI System!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)