from typing import List, Dict, Any
import re

class TransferGuardrails:
    """Guardrails system to ensure agents only respond to transfer and career-related queries"""
    
    ALLOWED_TOPICS = {
        'transfer': [
            'uc', 'csu', 'university of california', 'california state university',
            'transfer requirements', 'prerequisites', 'igetc', 'csu ge', 'assist.org',
            'transfer admission guarantee', 'tag', 'major preparation', 'articulation',
            'transfer application', 'application deadlines', 'gpa requirements'
        ],
        'career': [
            'career counseling', 'career planning', 'major selection', 'career paths',
            'job prospects', 'salary expectations', 'internships', 'professional development',
            'career resources', 'networking', 'resume', 'interview preparation'
        ],
        'financial_aid': [
            'financial aid', 'scholarships', 'grants', 'fafsa', 'cal grant',
            'tuition', 'cost of attendance', 'student loans', 'work study',
            'financial planning', 'college affordability'
        ],
        'academic': [
            'course selection', 'course difficulty', 'study strategies', 'academic planning',
            'grade requirements', 'course sequencing', 'academic support',
            'tutoring', 'study groups', 'time management'
        ]
    }
    
    BLOCKED_TOPICS = [
        'personal relationships', 'dating', 'social media', 'entertainment',
        'politics', 'religion', 'medical advice', 'legal advice',
        'financial investment', 'cryptocurrency', 'gambling'
    ]
    
    def is_query_allowed(self, query: str) -> Dict[str, Any]:
        """Check if a query is related to allowed transfer/career topics"""
        query_lower = query.lower()
        
        # Check for blocked topics first
        for blocked_topic in self.BLOCKED_TOPICS:
            if blocked_topic in query_lower:
                return {
                    'allowed': False,
                    'reason': f"Query contains blocked topic: {blocked_topic}",
                    'category': 'blocked'
                }
        
        # Check for allowed topics
        for category, keywords in self.ALLOWED_TOPICS.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return {
                        'allowed': True,
                        'category': category,
                        'matched_keyword': keyword
                    }
        
        # If no specific keywords found, apply contextual analysis
        transfer_indicators = ['transfer', 'college', 'university', 'degree', 'major', 'career']
        if any(indicator in query_lower for indicator in transfer_indicators):
            return {
                'allowed': True,
                'category': 'general_academic',
                'matched_keyword': 'contextual_match'
            }
        
        return {
            'allowed': False,
            'reason': "Query does not appear to be related to transfer or career topics",
            'category': 'off_topic'
        }
    
    def get_redirect_message(self, category: str) -> str:
        """Generate appropriate redirect message for blocked queries"""
        if category == 'blocked':
            return "I'm designed to help with college transfer and career planning questions only. Please ask about UC/CSU transfers, financial aid, career counseling, or academic planning."
        elif category == 'off_topic':
            return "I can only assist with questions related to transferring to UC/CSU schools, career planning, financial aid, and academic guidance. How can I help you with your transfer goals?"
        return "Please ask questions related to college transfer or career planning."