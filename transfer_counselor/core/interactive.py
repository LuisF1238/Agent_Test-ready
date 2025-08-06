"""
Interactive Session Manager

Handles interactive command-line conversations with the counseling system.
"""

import logging
from typing import Optional, Dict, Any


class InteractiveSessionManager:
    """Manages interactive command-line counseling sessions"""
    
    def __init__(self, system):
        self.system = system
        self.logger = logging.getLogger(__name__)
    
    def run(self, user_id: Optional[str] = None):
        """Run interactive counseling session"""
        print("\n🌟 Welcome to your Enhanced UC/CSU Transfer Counseling Session!")
        print("✨ Powered by advanced AI with intelligent handoffs and context awareness")
        print("Ask me anything about transferring, financial aid, careers, or academics.")
        print("\n💡 Commands: 'quit', 'stats', 'history', 'help'\n")
        
        # Create session
        session_id = self.system.create_session(user_id)
        print(f"📋 Session ID: {session_id[:8]}...")
        
        conversation_count = 0
        
        while True:
            try:
                # Get user input
                query = input("\n📝 Your question: ").strip()
                
                if query.lower() in ['quit', 'exit', 'bye']:
                    self._show_session_summary(session_id, conversation_count)
                    print("\n🎯 Good luck with your transfer journey!")
                    print("Remember: You've got this! 💪")
                    break
                
                elif query.lower() == 'stats':
                    self.system._show_system_stats()
                    continue
                    
                elif query.lower() == 'history':
                    self._show_conversation_history(session_id)
                    continue
                    
                elif query.lower() == 'help':
                    self._show_help()
                    continue
                
                if not query:
                    print("Please enter a question about UC/CSU transfer, financial aid, careers, or academics.")
                    continue
                
                # Process query
                print("\n🤔 Processing your question with AI agent orchestration...")
                result = self.system.process_query(query, session_id)
                conversation_count += 1
                
                # Display response
                self._display_response(result, conversation_count)
                
            except KeyboardInterrupt:
                print("\n\n🎯 Session ended. Good luck with your transfer goals!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again or contact support if the issue persists.")
    
    def _display_response(self, result: Dict[str, Any], conversation_count: int):
        """Display formatted response"""
        print("\n" + "="*80)
        agent_name = result['agent_used'].replace('_', ' ').title()
        print(f"📍 Response #{conversation_count} from: {agent_name}")
        if 'session_id' in result:
            print(f"🔄 Session: {result['session_id'][:8]}...")
        print("="*80)
        print(result['response'])
        
        if result.get('metadata'):
            print(f"\n🔍 Metadata: {result['metadata']}")
        
        print("\n" + "-"*60)
    
    def _show_session_summary(self, session_id: str, conversation_count: int):
        """Show session summary"""
        print(f"\n📊 Session Summary:")
        print(f"   Conversations: {conversation_count}")
        print(f"   Session ID: {session_id[:8]}...")
    
    def _show_conversation_history(self, session_id: str):
        """Show conversation history"""
        print(f"\n📜 Recent Conversation History:")
        print("   [History feature would show recent interactions]")
    
    def _show_help(self):
        """Show help information"""
        print("\n🆘 Help & Commands:")
        print("   - Ask any transfer-related question")
        print("   - 'stats' - Show system statistics")
        print("   - 'history' - Show conversation history")
        print("   - 'quit' - End session")
        print("\n🎯 Example Questions:")
        print("   • How do I apply for financial aid for UC schools?")
        print("   • What career paths are available with a psychology major?")
        print("   • How can I manage difficult courses while working?")
        print("   • What's the difference between UC and CSU for my major?")