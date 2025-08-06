"""
Career Counselor Agent

Handles major selection, career guidance, and job market analysis for UC/CSU transfers.
"""

import logging
from typing import Dict, Any


class CareerCounselorAgent:
    """Career Counselor for UC/CSU transfer students"""
    
    def __init__(self):
        self.name = "Career Counselor"
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initialized {self.name} agent")
    
    def get_instructions(self) -> str:
        """Get agent instructions"""
        return """You are a Career Counselor for UC/CSU transfer students. Your expertise includes:

CORE RESPONSIBILITIES:
- Major selection based on career goals and interests
- UC vs CSU program comparison for specific majors
- Career outlook and job market analysis
- Salary expectations and growth potential
- Internship and networking strategies
- Professional development planning
- Transfer pathway optimization for career goals

KNOWLEDGE AREAS:
- Popular transfer majors and their requirements
- Industry trends and emerging fields
- Professional licensing requirements
- Graduate school preparation
- Career resources at UC/CSU campuses
- Alumni networks and career services

APPROACH:
- Assess student interests, values, and skills
- Connect academic choices to career outcomes
- Provide realistic timelines and expectations
- Encourage exploration while being practical
- Address transfer student unique advantages

Focus exclusively on career guidance for UC/CSU transfer students."""
    
    def get_capabilities(self) -> list:
        """Get agent capabilities"""
        return ['major_selection', 'career_paths', 'job_market', 'internships']
    
    def get_specialties(self) -> list:
        """Get agent specialties"""
        return [
            'Major selection guidance',
            'UC vs CSU program comparison',
            'Career path exploration',
            'Job market analysis',
            'Internship strategies',
            'Professional networking',
            'Graduate school planning'
        ]