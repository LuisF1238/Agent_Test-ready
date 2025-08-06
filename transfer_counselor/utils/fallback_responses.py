"""
Fallback Responses Module

Provides pre-written responses when AI agents are not available.
"""

from typing import Dict


def get_fallback_response(user_message: str, agent_id: str) -> str:
    """Generate appropriate fallback responses based on agent type and query"""
    user_lower = user_message.lower()
    
    if agent_id == 'financial_aid':
        return _get_financial_aid_fallback(user_lower)
    elif agent_id == 'career_counselor':
        return _get_career_counselor_fallback(user_lower)
    elif agent_id == 'course_difficulty':
        return _get_academic_advisor_fallback(user_lower)
    elif agent_id == 'coordinator':
        return _get_coordinator_fallback(user_lower)
    else:
        return _get_default_fallback(agent_id)


def _get_financial_aid_fallback(user_lower: str) -> str:
    """Financial aid fallback responses"""
    if any(word in user_lower for word in ['cost', 'expensive', 'afford', 'money', 'tuition']):
        return """For UC/CSU costs and financial aid:

**UC Schools (2024-2025):**
- Tuition & Fees: ~$14,000-15,000/year (residents)
- Total Cost: ~$35,000-40,000/year (with room/board)

**CSU Schools:**
- Tuition & Fees: ~$6,000-7,000/year (residents)  
- Total Cost: ~$25,000-30,000/year (with room/board)

**Financial Aid Steps:**
1. Complete FAFSA by March 2nd priority deadline
2. Apply for Cal Grant (automatic with FAFSA)
3. Check school-specific scholarships and grants
4. Consider work-study programs

Visit your campus financial aid office for personalized guidance!"""

    elif any(word in user_lower for word in ['fafsa', 'financial aid', 'scholarship']):
        return """Financial Aid for Transfer Students:

**FAFSA (Free Application for Federal Student Aid):**
- Priority deadline: March 2nd annually
- Required for federal grants, loans, work-study
- Use your tax information from previous year

**Key Programs:**
- Pell Grant: Up to $7,395/year (no repayment needed)
- Cal Grant A: Covers tuition at UC/CSU
- Cal Grant B: Living expenses + tuition (after year 1)
- Federal Direct Loans: Borrow responsibly

**Transfer Tips:**
- Apply early for best aid packages
- Complete verification documents quickly
- Check each campus's scholarship portal

Need help with FAFSA? Visit studentaid.gov or your campus financial aid office."""

    return "I can help with financial aid questions including FAFSA, scholarships, grants, and cost planning for UC/CSU transfer students."


def _get_career_counselor_fallback(user_lower: str) -> str:
    """Career counselor fallback responses"""
    if 'business' in user_lower:
        return """UC vs CSU for Business Majors:

**UC Business Programs:**
- More research-focused, theoretical approach
- Better for graduate school preparation  
- Strong alumni networks in finance/consulting
- Examples: UC Berkeley (Haas), UCLA (Anderson prerequisites)
- More competitive admission, higher costs

**CSU Business Programs:**
- Practical, career-focused curriculum
- Strong industry connections and internships
- Excellent job placement rates
- Examples: SDSU, Cal Poly SLO, SJSU, CSU Fullerton
- More accessible admission, lower costs

**Career Outcomes:**
- Both paths lead to excellent career opportunities
- UC may have slight edge for competitive fields (investment banking, consulting)
- CSU graduates often have strong practical skills valued by employers
- Your performance matters more than the school system

**Recommendation:** Choose based on learning style, career goals, and financial considerations."""

    elif any(word in user_lower for word in ['major', 'career', 'job']):
        return """Choosing Your Transfer Major:

**Popular Transfer-Friendly Majors:**
- Business Administration
- Psychology  
- Engineering (varies by campus)
- Computer Science
- Biology/Pre-health
- Communications
- Liberal Studies (teaching)

**Career Guidance Questions:**
1. What subjects genuinely interest you?
2. What are your natural strengths?
3. What lifestyle do you want (salary, work-life balance)?
4. Are you willing to pursue graduate school?

**Resources:**
- O*NET Interest Profiler (online career assessment)
- Bureau of Labor Statistics for job outlook
- LinkedIn to research professionals in fields
- Informational interviews with alumni

Schedule an appointment with your campus career center for personalized guidance!"""

    return "I can help with career guidance including major selection, career paths, job market analysis, and UC vs CSU program comparisons."


def _get_academic_advisor_fallback(user_lower: str) -> str:
    """Academic advisor fallback responses"""
    if any(word in user_lower for word in ['difficult', 'hard', 'struggling', 'organic chemistry', 'calculus', 'physics']):
        return """Managing Difficult Courses:

**Study Strategies:**
- Active learning: Teach concepts to others
- Spaced repetition: Review material regularly
- Practice problems: Don't just read, DO
- Form study groups with serious students
- Use office hours - professors want to help!

**For STEM Courses:**
- Start homework early, don't procrastinate
- Understand concepts before memorizing formulas  
- Use multiple resources (textbook, online videos, tutoring)
- Practice past exams if available

**Campus Resources:**
- Tutoring centers (often free)
- Supplemental Instruction (SI) sessions
- Professor office hours
- Study skills workshops
- Academic counseling

**Time Management:**
- Block schedule for challenging courses
- Break large assignments into smaller tasks
- Use the Pomodoro Technique (25-min focused sessions)

Remember: Struggling is normal! Seek help early, not after you're already behind."""

    elif any(word in user_lower for word in ['roadmap', 'plan', 'course', 'transfer', 'schedule']):
        return """Creating Your Transfer Course Roadmap:

**Step 1: Research Requirements**
- Check ASSIST.org for transfer requirements
- Review IGETC (Intersegmental General Education Transfer Curriculum)
- Identify major prerequisites for your target schools

**Step 2: Plan Your Path**
- **Year 1**: Focus on English, Math, and basic major prerequisites
- **Year 2**: Complete remaining IGETC and advanced prerequisites
- Balance difficult courses with easier ones each semester

**Step 3: Key Considerations**
- Complete as many prerequisites as possible before transferring
- Maintain a competitive GPA (3.0+ for CSU, 3.2+ for UC)
- Consider course difficulty and your work schedule

**Resources:**
- ASSIST.org for articulation agreements
- Campus transfer counselors
- Academic advisors at your current college
- UC/CSU Transfer Admission Planner (TAP)

Meet with a counselor to create a personalized roadmap for your major and target schools!"""

    return "I can help with academic planning including course roadmaps, study strategies, time management, and transfer preparation."


def _get_coordinator_fallback(user_lower: str) -> str:
    """Coordinator fallback responses"""
    # Route to appropriate specialist based on keywords
    if any(word in user_lower for word in ['cost', 'money', 'fafsa', 'financial', 'scholarship', 'afford']):
        return """I can help you with financial questions! For detailed financial aid guidance including FAFSA help, scholarship opportunities, and cost comparisons between UC and CSU schools, I'd recommend speaking with our Financial Aid Specialist.

**Quick Financial Aid Overview:**
- Complete FAFSA by March 2nd priority deadline
- UC schools: ~$35-40k total cost, CSU: ~$25-30k total cost
- Many grants and scholarships available for transfer students

Would you like me to connect you with our Financial Aid Specialist for more detailed assistance?"""
    
    elif any(word in user_lower for word in ['major', 'career', 'job', 'business', 'psychology']):
        return """I can help you with career and major selection! For guidance on choosing the right major, comparing UC vs CSU programs, and career planning, our Career Counselor would be perfect for your needs.

**Quick Career Guidance:**
- Consider your interests, strengths, and career goals
- Research job market trends and salary expectations  
- UC programs tend to be more research-focused
- CSU programs are often more career-practical

Would you like me to connect you with our Career Counselor for personalized guidance?"""
    
    elif any(word in user_lower for word in ['difficult', 'study', 'academic', 'course', 'struggling']):
        return """I can help you with academic success strategies! For course difficulty management, study techniques, and academic planning, our Academic Advisor is the right specialist.

**Quick Academic Tips:**
- Start studying early, don't cram
- Use active learning techniques
- Take advantage of campus tutoring resources
- Build relationships with professors and TAs

Would you like me to connect you with our Academic Advisor for detailed study strategies?"""
    
    else:
        return """Welcome to your UC/CSU Transfer Counseling System! I'm here to coordinate your questions with our team of specialists:

**Our Specialists:**
🏦 **Financial Aid Specialist** - FAFSA, scholarships, grants, cost planning
👔 **Career Counselor** - Major selection, career paths, job market analysis  
📚 **Academic Advisor** - Study strategies, course planning, academic success

**Example Questions:**
- "How much does it cost to transfer to UC Berkeley?"
- "What's the job market like for psychology majors?"
- "I'm struggling with calculus, what study strategies work best?"
- "Should I choose UC or CSU for my major?"

What aspect of your UC/CSU transfer journey would you like guidance on today?"""


def _get_default_fallback(agent_id: str) -> str:
    """Default fallback response"""
    return f"I'm here to help with your UC/CSU transfer questions. As your {agent_id.replace('_', ' ').title()}, I can assist with topics in my area of expertise. Could you please provide more details about what you'd like to know?"