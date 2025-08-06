# Enhanced Transfer Counselor Agent System v2.0.0

🚀 **STATUS: FULLY REFACTORED & OPERATIONAL** 🚀

A sophisticated multi-agent system powered by OpenAI's Agents SDK, designed to help community college students transfer to UC and CSU schools with comprehensive AI assistance.

> ✅ **v2.0.0 Released**: Complete architectural refactoring for maintainability  
> ✅ **Professional Structure**: Organized into clean, modular packages  
> ✅ **API Integration Working**: Real GPT-powered responses with intelligent routing  
> ✅ **Production Ready**: Full session management, tracing, and error handling  

## 🎯 System Overview

This system provides specialized counseling through multiple AI agents with built-in guardrails, session management, tracing, and comprehensive error handling.

### Key Components

- **🤖 Coordinator Agent**: Routes queries and manages multi-agent responses
- **💰 Financial Aid Agent**: FAFSA, scholarships, grants, cost planning
- **💼 Career Counselor Agent**: Major selection, career paths, job prospects
- **📚 Academic Advisor**: Course planning, study strategies, academic success
- **🛡️ Guardrails System**: Ensures responses stay on-topic for transfer counseling
- **📊 Session Management**: Persistent conversations with SQLite database (sessions.db)
- **🔍 Tracing System**: Comprehensive logging and monitoring

## 🚀 Quick Start

### Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your OpenAI API key to .env file:
echo 'OPENAI_API_KEY="sk-your-key-here"' > .env
```

### Run Interactive Session
```bash
python -c "from transfer_counselor import EnhancedTransferCounselorSystem; EnhancedTransferCounselorSystem().interactive_session()"
```

### Use in Code
```python
from transfer_counselor import EnhancedTransferCounselorSystem

system = EnhancedTransferCounselorSystem()
result = system.process_query("How do I apply for financial aid?")
print(result['response'])
```

### Run Tests
```bash
python -m transfer_counselor.tests.test_system
```

## 📋 Features

### Specialized Expertise
- **Financial Aid**: FAFSA deadlines, Cal Grant requirements, scholarship opportunities
- **Career Guidance**: Major selection, salary expectations, career paths
- **Academic Success**: Course planning, study strategies, GPA management
- **Transfer Planning**: UC vs CSU comparison, prerequisite tracking

### Built-in Safety
- Topic guardrails prevent off-topic discussions
- Focused on defensive/educational use only
- Redirects inappropriate queries to transfer-related topics

### Multi-Agent Coordination
- Single queries can consult multiple specialists
- Synthesized responses from relevant experts
- Context preservation across conversation

## 🎓 Example Queries

The system can handle questions like:
- "What financial aid is available for UC transfers?"
- "Which major should I choose for a career in tech?"
- "How do I manage a heavy course load while working?"
- "What's the difference between UC Berkeley and Cal Poly for engineering?"
- "I'm struggling in organic chemistry, what should I do?"

## 🏗️ Architecture

```
TransferCounselorSystem
├── CoordinatorAgent (main router)
├── FinancialAidAgent (specialized counselor)
├── CareerCounselorAgent (specialized counselor)
├── CourseDifficultyAgent (specialized counselor)
└── TransferGuardrails (safety system)
```

## 🛡️ Guardrails

The system includes comprehensive guardrails that:
- Allow transfer, career, financial aid, and academic topics
- Block off-topic discussions (entertainment, personal relationships, etc.)
- Provide helpful redirection messages
- Maintain focus on UC/CSU transfer goals

## 📁 File Structure

```
Agent_Test/
├── transfer_counselor/           # Main package
│   ├── __init__.py              # Package entry point
│   ├── agents/                  # Agent implementations
│   │   ├── manager.py           # Agent orchestration
│   │   ├── financial_aid.py     # Financial aid expertise
│   │   ├── career_counselor.py  # Career guidance
│   │   ├── academic_advisor.py  # Academic planning
│   │   └── coordinator.py       # Master coordination
│   ├── core/                    # Core system components
│   │   ├── system.py           # Main system class
│   │   ├── session.py          # Session management
│   │   ├── routing.py          # Query routing
│   │   ├── tracing.py          # Logging & monitoring
│   │   └── interactive.py      # Interactive session
│   ├── utils/                   # Utility modules
│   │   ├── config.py           # Configuration management
│   │   ├── error_handling.py   # Error handling & recovery
│   │   ├── guardrails.py       # Safety system
│   │   └── fallback_responses.py # Fallback responses
│   └── tests/                   # Test suite
│       └── test_system.py      # System integration tests
├── sessions.db                  # SQLite session database
├── .env                        # Environment variables (API key)
├── config.yaml                 # System configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This documentation
```

## 🎯 Use Cases

Perfect for:
- Community college transfer counseling
- Academic advising systems
- Career guidance platforms
- Financial aid assistance tools
- Educational chatbots with focused expertise

## 📊 Agent Specializations

### Financial Aid Agent
- FAFSA guidance and deadlines
- Cal Grant applications
- UC/CSU cost comparisons
- Scholarship opportunities
- Financial planning strategies

### Career Counselor Agent
- Major selection guidance
- Career path exploration
- Salary expectations
- Industry analysis
- Professional development

### Course Difficulty Agent
- Study strategies and techniques
- Course load management
- GPA improvement plans
- Time management
- Academic success skills

## 🔧 Customization

The system is designed to be easily customizable:
- Add new specialized agents
- Modify guardrails for different topics
- Extend knowledge bases
- Integrate with external APIs
- Customize response formatting

## 🤝 Contributing

This system prioritizes defensive security and educational use. Any modifications should maintain focus on helping students achieve their educational goals safely and effectively.