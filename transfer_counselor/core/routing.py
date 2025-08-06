"""
Query Routing Module

Handles intelligent routing of user queries to appropriate specialist agents.
"""

import logging
from typing import Dict, List


class QueryRouter:
    """Intelligent query router for directing queries to appropriate agents"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Define keyword mappings for each agent
        self.agent_keywords = {
            'financial_aid': [
                'cost', 'money', 'fafsa', 'financial', 'scholarship', 'afford', 
                'tuition', 'grant', 'expensive', 'budget', 'payment', 'aid',
                'funding', 'cal grant', 'pell grant'
            ],
            'course_difficulty': [
                'difficult', 'study', 'academic', 'course', 'struggling', 'calculus', 
                'chemistry', 'physics', 'roadmap', 'transfer', 'plan', 'schedule', 
                'semester', 'prerequisites', 'sequence', 'math', 'science', 'english', 
                'requirements', 'units', 'classes', 'curriculum', 'igetc', 'breadth', 
                'ge', 'general education', 'lower division', 'upper division', 
                'planning', 'pathway', 'preparation', 'recommend', 'suggestion'
            ],
            'career_counselor': [
                'major', 'career', 'job', 'business', 'psychology', 'engineering', 
                'computer science', 'prospects', 'employment', 'profession', 
                'occupation', 'work', 'salary', 'internship', 'networking'
            ]
        }
    
    def route_query(self, query: str) -> str:
        """Route query to appropriate agent based on content"""
        query_lower = query.lower()
        
        # Calculate relevance scores for each agent
        agent_scores = {}
        
        for agent_id, keywords in self.agent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                agent_scores[agent_id] = score
        
        # Route to agent with highest score
        if agent_scores:
            best_agent = max(agent_scores, key=agent_scores.get)
            self.logger.debug(f"Query '{query[:50]}...' routed to {best_agent} (score: {agent_scores[best_agent]})")
            return best_agent
        
        # Default to coordinator if no specific match
        self.logger.debug(f"Query '{query[:50]}...' routed to coordinator (no specific match)")
        return 'coordinator'
    
    def get_routing_explanation(self, query: str) -> Dict[str, any]:
        """Get detailed explanation of routing decision"""
        query_lower = query.lower()
        
        agent_details = {}
        for agent_id, keywords in self.agent_keywords.items():
            matched_keywords = [kw for kw in keywords if kw in query_lower]
            agent_details[agent_id] = {
                'score': len(matched_keywords),
                'matched_keywords': matched_keywords
            }
        
        selected_agent = self.route_query(query)
        
        return {
            'selected_agent': selected_agent,
            'agent_scores': agent_details,
            'reasoning': f"Selected {selected_agent} based on keyword matching"
        }
    
    def add_custom_keywords(self, agent_id: str, keywords: List[str]):
        """Add custom keywords for an agent"""
        if agent_id in self.agent_keywords:
            self.agent_keywords[agent_id].extend(keywords)
            self.logger.info(f"Added {len(keywords)} custom keywords to {agent_id}")
        else:
            self.logger.warning(f"Unknown agent_id: {agent_id}")
    
    def get_agent_keywords(self, agent_id: str) -> List[str]:
        """Get keywords for a specific agent"""
        return self.agent_keywords.get(agent_id, [])