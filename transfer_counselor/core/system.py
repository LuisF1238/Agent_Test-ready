#!/usr/bin/env python3
"""
Enhanced Transfer Counselor Agent System

A sophisticated multi-agent system with proper handoffs, context management,
session persistence, tracing, and error handling for UC/CSU transfer guidance.
"""

import os
import sys
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from ..utils.config import ConfigManager
from ..utils.error_handling import ErrorHandler, with_retry, RetryConfig
from ..utils.guardrails import TransferGuardrails
from ..agents.manager import AgentManager
from .session import SessionManager
from .tracing import TracingManager
from .routing import QueryRouter


class EnhancedTransferCounselorSystem:
    """Enhanced multi-agent system with comprehensive orchestration capabilities"""
    
    def __init__(self, config_file: Optional[str] = None):
        # Initialize configuration
        self.config_manager = ConfigManager(config_file)
        self.config = self.config_manager.get_config()
        
        # Initialize core components
        self.session_manager = SessionManager(
            persistent=self.config.session_persistence,
            db_path=self.config.session_db_path
        )
        self.tracer = TracingManager()
        self.error_handler = ErrorHandler()
        self.guardrails = TransferGuardrails()
        self.query_router = QueryRouter()
        self.logger = logging.getLogger(__name__)
        
        # Initialize agent management system
        try:
            self.agent_manager = AgentManager()
            self.agents = self.agent_manager.get_agents()
        except Exception as e:
            # Fall back to basic agent structure if initialization fails
            self.agent_manager = None
            self.agents = self._create_fallback_agents()
            self.logger.warning(f"Agent initialization failed, using fallback: {e}")
        
        # Setup error handling patterns
        self._setup_error_handling()
        
        self._print_system_status()
    
    def _create_fallback_agents(self) -> Dict[str, Any]:
        """Create fallback agents when main system fails"""
        return {
            'financial_aid': type('Agent', (), {'agent': None, 'name': 'Financial Aid Specialist'})(),
            'career_counselor': type('Agent', (), {'agent': None, 'name': 'Career Counselor'})(),
            'course_difficulty': type('Agent', (), {'agent': None, 'name': 'Academic Advisor'})(),
            'coordinator': type('Agent', (), {'agent': None, 'name': 'Transfer Coordinator'})()
        }
    
    def _setup_error_handling(self):
        """Setup error handling patterns and fallbacks"""
        from ..utils.error_handling import CircuitBreakerConfig
        
        # Register circuit breakers for external services
        self.error_handler.register_circuit_breaker(
            'openai_api', 
            CircuitBreakerConfig(failure_threshold=3, recovery_timeout=30)
        )
        
        # Register fallback handlers
        self.error_handler.register_fallback_handler(
            'query_processing', 
            self._fallback_response
        )
    
    def _fallback_response(self, error_context):
        """Fallback response when primary systems fail"""
        return {
            'response': "I'm experiencing technical difficulties right now. Please try your question again in a moment, or contact your transfer counselor directly for immediate assistance.",
            'agent_used': 'fallback',
            'status': 'fallback_executed',
            'error_id': error_context.error_id
        }
    
    def _print_system_status(self):
        """Print system initialization status"""
        print("🎓 Enhanced Transfer Counselor System Initialized")
        print("\n🔧 System Features:")
        print("  ✅ OpenAI Agents SDK integration with proper handoffs")
        print("  ✅ Persistent session management")
        print("  ✅ Comprehensive tracing and monitoring")
        print("  ✅ Robust error handling and recovery")
        print("  ✅ Context propagation across interactions")
        print("\n🤖 Available Specialists:")
        print("  💰 Financial Aid - FAFSA, scholarships, cost planning")
        print("  💼 Career Counseling - Major selection, career paths")
        print("  📚 Academic Planning - Course difficulty, study strategies")
        print("  🎯 Coordinator - Intelligent routing and multi-agent coordination")
        print("-" * 70)
    
    @with_retry(RetryConfig(max_attempts=2, initial_delay=0.5))
    def process_query(self, student_query: str, session_id: Optional[str] = None, 
                     student_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a student query through the enhanced agent system"""
        # Create or get session
        if session_id is None:
            session_id = self.create_session()
        
        # Prepare messages
        messages = [
            {"role": "user", "content": student_query}
        ]
        
        try:
            # Process through agents
            span_id = self.tracer.trace_session_start(session_id)
            
            # Determine which agent to use based on query content
            agent_to_use = self.query_router.route_query(student_query)
            
            # Try to use OpenAI API with agents
            api_key = os.getenv('OPENAI_API_KEY')
            
            if api_key and api_key.startswith('sk-') and self.agent_manager:
                try:
                    response_content = self.agent_manager.process_with_agent(
                        agent_to_use, student_query, session_id
                    )
                    self.logger.info(f"Generated AI response using {agent_to_use} agent")
                        
                except Exception as e:
                    self.logger.warning(f"OpenAI Agents API call failed: {e}")
                    response_content = self._generate_fallback_response(student_query, agent_to_use)
            else:
                # Use fallback response when API key is not available
                response_content = self._generate_fallback_response(student_query, agent_to_use)
                if not api_key:
                    self.logger.info(f"Using fallback response (no API key set) for {agent_to_use}")
                else:
                    self.logger.info(f"Using fallback response (invalid API key format) for {agent_to_use}")
            
            self.tracer.trace_session_end(session_id, span_id)
            
            return {
                'response': response_content,
                'agent_used': agent_to_use,
                'session_id': session_id,
                'status': 'success',
                'metadata': {'agent_capabilities': self._get_agent_capabilities(agent_to_use)},
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            error_context = self.error_handler.handle_error(e, {
                'component': 'query_processing',
                'operation': 'process_query',
                'session_id': session_id,
                'query': student_query
            })
            
            # Use fallback response
            agent_to_use = self.query_router.route_query(student_query)
            fallback_response = self._generate_fallback_response(student_query, agent_to_use)
            
            return {
                'response': fallback_response,
                'agent_used': agent_to_use,
                'session_id': session_id,
                'status': 'fallback',
                'error_id': error_context.error_id,
                'timestamp': datetime.now().isoformat()
            }
    
    def create_session(self, user_id: Optional[str] = None) -> str:
        """Create a new session"""
        if self.agent_manager:
            return self.agent_manager.create_session(user_id)
        else:
            # Fallback session creation
            import uuid
            return str(uuid.uuid4())
    
    def _get_agent_capabilities(self, agent_id: str) -> list:
        """Get capabilities for an agent"""
        capabilities_map = {
            'financial_aid': ['FAFSA', 'scholarships', 'grants', 'financial_planning'],
            'career_counselor': ['major_selection', 'career_paths', 'job_market', 'internships'],
            'course_difficulty': ['study_strategies', 'course_planning', 'academic_support'],
            'coordinator': ['routing', 'coordination', 'multi_agent_synthesis']
        }
        return capabilities_map.get(agent_id, [])
    
    def _generate_fallback_response(self, user_message: str, agent_id: str) -> str:
        """Generate appropriate fallback responses based on agent type and query"""
        # Import the fallback responses from a dedicated module
        from ..utils.fallback_responses import get_fallback_response
        return get_fallback_response(user_message, agent_id)
    
    def interactive_session(self, user_id: Optional[str] = None):
        """Run enhanced interactive counseling session with full tracing"""
        from .interactive import InteractiveSessionManager
        session_manager = InteractiveSessionManager(self)
        session_manager.run(user_id)
    
    def _show_system_stats(self):
        """Show system statistics"""
        print("\n📊 System Statistics:")
        
        # Session statistics
        session_count = len(self.agent_manager.sessions) if self.agent_manager else 0
        print(f"   Active sessions: {session_count}")
        
        # Agent information
        agent_count = len(self.agents)
        print(f"   Available agents: {agent_count}")
        for agent_id in self.agents:
            print(f"   - {agent_id}")
        
        # Error statistics
        error_stats = self.error_handler.get_error_statistics(24)
        print(f"\n🚨 Errors (24h): {error_stats['total_errors']}")
        
        # Performance report
        if hasattr(self.tracer, 'get_performance_report'):
            perf_report = self.tracer.get_performance_report(1)
            print(f"\n⚡ Performance: {len(perf_report.get('metrics', {}))} metrics tracked")