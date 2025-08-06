"""
Agent Manager

Manages all transfer counseling agents and their interactions.
"""

import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

from agents import Agent, Runner, set_default_openai_key, SQLiteSession

from .financial_aid import FinancialAidAgent
from .career_counselor import CareerCounselorAgent
from .academic_advisor import AcademicAdvisorAgent
from .coordinator import CoordinatorAgent


class AgentManager:
    """Manages all transfer counseling agents and their execution"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.sessions: Dict[str, Any] = {}
        
        # Initialize API key
        self.api_key = api_key or self._get_api_key()
        if self.api_key and self.api_key.startswith('sk-'):
            set_default_openai_key(self.api_key)
            self.logger.info("OpenAI API key configured successfully")
        else:
            self.logger.warning("No valid API key found - using fallback responses")
        
        # Initialize runner
        self.runner = Runner()
        
        # Initialize agents
        self.agents = self._initialize_agents()
        
        self.logger.info("Agent manager initialized successfully")
    
    def _get_api_key(self) -> Optional[str]:
        """Get API key from environment variables"""
        return os.getenv('OPENAI_API_KEY')
    
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all transfer counseling agents"""
        agents = {}
        
        # Initialize individual agent classes
        financial_aid = FinancialAidAgent()
        career_counselor = CareerCounselorAgent()
        academic_advisor = AcademicAdvisorAgent()
        coordinator = CoordinatorAgent()
        
        # Create OpenAI Agents SDK agents with proper handoffs
        agents['financial_aid'] = self._create_wrapper(
            financial_aid,
            Agent(
                name="Financial Aid Specialist",
                handoff_description="Specialist for FAFSA, scholarships, grants, and financial planning",
                instructions=financial_aid.get_instructions()
            )
        )
        
        agents['career_counselor'] = self._create_wrapper(
            career_counselor,
            Agent(
                name="Career Counselor", 
                handoff_description="Specialist for major selection, career paths, and job prospects",
                instructions=career_counselor.get_instructions()
            )
        )
        
        agents['course_difficulty'] = self._create_wrapper(
            academic_advisor,
            Agent(
                name="Academic Advisor",
                handoff_description="Specialist for course planning, study strategies, and academic support", 
                instructions=academic_advisor.get_instructions()
            )
        )
        
        # Coordinator gets handoffs to all specialists
        agents['coordinator'] = self._create_wrapper(
            coordinator,
            Agent(
                name="Transfer Coordinator",
                handoff_description="Master coordinator for routing queries to appropriate specialists",
                instructions=coordinator.get_instructions(),
                handoffs=[
                    agents['financial_aid']['agent'],
                    agents['career_counselor']['agent'],
                    agents['course_difficulty']['agent']
                ]
            )
        )
        
        self.logger.info("All agents initialized with proper handoffs")
        return agents
    
    def _create_wrapper(self, agent_class, sdk_agent) -> Dict[str, Any]:
        """Create a wrapper combining our agent class with SDK agent"""
        return {
            'class': agent_class,
            'agent': sdk_agent,
            'name': sdk_agent.name
        }
    
    def get_agents(self) -> Dict[str, Any]:
        """Get all initialized agents"""
        return self.agents
    
    def create_session(self, user_id: Optional[str] = None) -> str:
        """Create a new session"""
        session_id = str(uuid.uuid4())
        
        session_data = {
            'id': session_id,
            'user_id': user_id,
            'created_at': datetime.now(),
            'last_updated': datetime.now(),
            'conversation_history': []
        }
        
        self.sessions[session_id] = session_data
        self.logger.info(f"Created new session: {session_id} for user: {user_id}")
        return session_id
    
    def process_with_agent(self, agent_id: str, query: str, session_id: str) -> str:
        """Process query with specified agent using session memory"""
        if agent_id not in self.agents:
            raise ValueError(f"Unknown agent: {agent_id}")
        
        agent = self.agents[agent_id]['agent']
        
        # Create session memory for conversation continuity
        session_memory = SQLiteSession(session_id)
        
        try:
            # Execute with OpenAI Agents SDK
            response = self.runner.run_sync(
                agent,
                query,
                session=session_memory
            )
            
            # Extract response content
            if hasattr(response, 'final_output') and response.final_output:
                return response.final_output
            else:
                raise ValueError("No valid response from agent")
                
        except Exception as e:
            self.logger.error(f"Error processing with agent {agent_id}: {e}")
            raise
    
    def get_agent_info(self, agent_id: str) -> Dict[str, Any]:
        """Get information about a specific agent"""
        if agent_id not in self.agents:
            return {}
        
        agent_data = self.agents[agent_id]
        return {
            'name': agent_data['name'],
            'handoff_description': agent_data['agent'].handoff_description,
            'instructions_preview': agent_data['agent'].instructions[:200] + "...",
            'handoffs_count': len(agent_data['agent'].handoffs) if agent_data['agent'].handoffs else 0
        }
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a session"""
        return self.sessions.get(session_id)