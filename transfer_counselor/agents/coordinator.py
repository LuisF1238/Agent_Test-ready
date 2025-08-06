"""
Transfer Coordinator Agent

Master coordinator for routing queries and orchestrating multi-agent responses.
"""

import logging
from typing import Dict, Any


class CoordinatorAgent:
    """Transfer Coordinator responsible for query routing and agent orchestration"""
    
    def __init__(self):
        self.name = "Transfer Coordinator"
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initialized {self.name} agent")
    
    def get_instructions(self) -> str:
        """Get agent instructions"""
        return """You are the Master Transfer Coordinator responsible for:

CORE RESPONSIBILITIES:
1. Route student queries to appropriate specialized agents
2. Coordinate multi-agent responses when needed
3. Maintain conversation context across interactions
4. Ensure all responses stay within transfer/career counseling scope
5. Provide comprehensive guidance by combining specialist insights

SPECIALIZED AGENTS AVAILABLE:
- Financial Aid Specialist: FAFSA, scholarships, grants, cost planning
- Career Counselor: Major selection, career paths, job prospects  
- Academic Advisor: Course planning, difficulty management, study strategies

COORDINATION APPROACH:
- Analyze queries to determine appropriate specialists
- Facilitate handoffs between agents when needed
- Synthesize multi-agent responses coherently
- Maintain conversation flow and context
- Always prioritize student success in UC/CSU transfer goals

You can handoff to other agents when their expertise is needed."""
    
    def get_capabilities(self) -> list:
        """Get agent capabilities"""
        return ['routing', 'coordination', 'multi_agent_synthesis']
    
    def get_specialties(self) -> list:
        """Get agent specialties"""
        return [
            'Query routing',
            'Agent coordination',
            'Multi-agent orchestration',
            'Context management',
            'Response synthesis',
            'Workflow optimization'
        ]