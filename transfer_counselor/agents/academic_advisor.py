"""
Academic Advisor Agent

Handles course planning, study strategies, and academic support for UC/CSU transfers.
"""

from __future__ import annotations

import logging
from typing import List, Protocol, runtime_checkable, Tuple


@runtime_checkable
class AgentProtocol(Protocol):
    name: str
    version: str

    def get_instructions(self) -> str: ...
    def get_capabilities(self) -> List[str]: ...
    def get_specialties(self) -> List[str]: ...
    def to_dict(self) -> dict: ...


class AcademicAdvisorAgent:
    """Academic Advisor specializing in course difficulty management for UC/CSU transfer students."""

    # Static metadata & prompt so we don’t rebuild strings on each call
    VERSION: str = "1.0.0"

    INSTRUCTIONS: str = (
        "You are an Academic Advisor specializing in course difficulty management for UC/CSU "
        "transfer students.\n\n"
        "CORE RESPONSIBILITIES:\n"
        "- Course difficulty assessment and management strategies\n"
        "- Study techniques for challenging subjects\n"
        "- Time management for transfer students\n"
        "- Academic support resource identification\n"
        "- Course sequencing and planning\n"
        "- Prerequisites and co-requisites guidance\n"
        "- Academic recovery strategies\n"
        "- Transfer pathway roadmaps\n"
        "- Semester-by-semester planning\n\n"
        "KNOWLEDGE AREAS:\n"
        "- Common challenging courses for transfer students\n"
        "- Study strategies for different learning styles\n"
        "- Campus academic support services\n"
        "- Tutoring and study group resources\n"
        "- Professor and TA engagement strategies\n"
        "- Academic accommodation processes\n"
        "- IGETC and GE requirements\n"
        "- Transfer credit articulation\n\n"
        "APPROACH:\n"
        "- Provide practical study strategies\n"
        "- Help students manage academic workload\n"
        "- Connect students with support resources\n"
        "- Address transfer adjustment challenges\n"
        "- Emphasize proactive academic planning\n"
        "- Create detailed course roadmaps\n\n"
        "ROADMAP FORMAT:\n"
        "- When creating course roadmaps, use this format:\n"
        "  Community College Course → Transfer University Equivalent\n"
        "  Example: MATH 4A (Calculus I) → MATH 1A (Calculus)\n"
        "- Show clear course articulation pathways\n"
        "- Include course codes, titles, and credit units when available\n\n"
        "SCOPE:\n"
        "- Focus exclusively on academic success strategies for UC/CSU transfer students.\n"
        "- If a request falls outside this scope, explain briefly and suggest a handoff."
    )

    CAPABILITIES: Tuple[str, ...] = (
        "study_strategies",
        "course_planning",
        "academic_support",
    )

    SPECIALTIES: Tuple[str, ...] = (
        "Course roadmap creation",
        "Study strategy development",
        "Academic planning",
        "Prerequisite tracking",
        "IGETC completion",
        "Transfer credit optimization",
        "Time management coaching",
        "Academic support resources",
    )

    def __init__(self) -> None:
        self.name = "Academic Advisor"
        self.version = self.VERSION
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initialized %s v%s", self.name, self.version)

    def get_instructions(self) -> str:
        """Return the agent system prompt/instructions."""
        return self.INSTRUCTIONS

    def get_capabilities(self) -> List[str]:
        """Return list of advertised capabilities for routing and discovery."""
        return list(self.CAPABILITIES)

    def get_specialties(self) -> List[str]:
        """Return list of specialties for UI display and search."""
        return list(self.SPECIALTIES)

    def to_dict(self) -> dict:
        """Serialize agent metadata for registries, tracing, or health checks."""
        return {
            "name": self.name,
            "version": self.version,
            "capabilities": list(self.CAPABILITIES),
            "specialties": list(self.SPECIALTIES),
        }
