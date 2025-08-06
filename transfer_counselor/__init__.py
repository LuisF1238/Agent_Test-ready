"""
Enhanced Transfer Counselor Agent System

A sophisticated multi-agent system powered by OpenAI's Agents SDK,
designed to help community college students transfer to UC and CSU schools.
"""

__version__ = "2.0.0"
__author__ = "Transfer Counselor Team"
__description__ = "AI-powered UC/CSU transfer counseling system"

from .core.system import EnhancedTransferCounselorSystem
from .agents.manager import AgentManager
from .core.session import SessionManager

__all__ = [
    "EnhancedTransferCounselorSystem",
    "AgentManager", 
    "SessionManager"
]