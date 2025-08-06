# Transfer Counselor System - Project Structure

## 🏗️ Refactored Architecture (v2.0.0)

The project has been completely refactored into a clean, professional, maintainable structure:

```
Agent_Test/
├── app.py                           # 🚀 Main application entry point
├── transfer_counselor/              # 📦 Main package
│   ├── __init__.py                  # Package initialization
│   ├── agents/                      # 🤖 Agent-related modules
│   │   ├── __init__.py
│   │   ├── manager.py               # Agent management and coordination
│   │   ├── financial_aid.py         # Financial Aid Specialist
│   │   ├── career_counselor.py      # Career Counselor
│   │   ├── academic_advisor.py      # Academic Advisor
│   │   └── coordinator.py           # Transfer Coordinator
│   ├── core/                        # 🎯 Core system modules
│   │   ├── __init__.py
│   │   ├── system.py                # Main system orchestration
│   │   ├── session.py               # Session management
│   │   ├── routing.py               # Query routing logic
│   │   ├── tracing.py               # Performance monitoring
│   │   └── interactive.py           # Interactive session manager
│   ├── utils/                       # 🛠️ Utility modules
│   │   ├── __init__.py
│   │   ├── config.py                # Configuration management
│   │   ├── error_handling.py        # Error handling and recovery
│   │   ├── guardrails.py            # Input validation and safety
│   │   └── fallback_responses.py    # Fallback response generation
│   └── tests/                       # 🧪 Test modules
│       ├── __init__.py
│       └── test_system.py           # System integration tests
├── config.yaml                     # 📋 System configuration
├── requirements.txt                 # 📝 Python dependencies
├── README_Enhanced.md               # 📚 Comprehensive documentation
└── logs/                           # 📊 Log files and traces
    └── agent_trace.jsonl           # Structured trace data
```

## 🔄 Refactoring Benefits

### ✅ **Improved Organization**
- **Separation of Concerns**: Each module has a clear, single responsibility
- **Package Structure**: Logical grouping of related functionality
- **Import Clarity**: Clean import paths and dependencies

### ✅ **Enhanced Maintainability**
- **Modular Design**: Easy to modify individual components
- **Clear Interfaces**: Well-defined APIs between modules
- **Code Reusability**: Shared utilities and common patterns

### ✅ **Better Testing**
- **Unit Testing**: Each module can be tested independently
- **Integration Testing**: System-level tests verify end-to-end functionality
- **Test Organization**: Tests grouped logically with code

### ✅ **Professional Structure**
- **Industry Standards**: Follows Python packaging best practices
- **Scalability**: Easy to add new agents or features
- **Documentation**: Clear module documentation and interfaces

## 📦 Module Responsibilities

### 🤖 **Agents Package**
- **manager.py**: Coordinates all agents, handles OpenAI SDK integration
- **Individual Agent Files**: Each specialist has its own module
- **Clean Separation**: Agent logic separated from system orchestration

### 🎯 **Core Package** 
- **system.py**: Main system orchestration and coordination  
- **session.py**: Persistent session management with SQLite
- **routing.py**: Intelligent query routing with keyword matching
- **interactive.py**: Command-line interface management

### 🛠️ **Utils Package**
- **config.py**: Centralized configuration with YAML and environment support
- **error_handling.py**: Robust error handling with circuit breakers
- **fallback_responses.py**: Pre-written responses for offline mode
- **guardrails.py**: Input validation and safety checks

## 🚀 **Usage Examples**

### **As a Package**
```python
from transfer_counselor import EnhancedTransferCounselorSystem

# Initialize system
system = EnhancedTransferCounselorSystem()

# Process queries
result = system.process_query("How much does UC Berkeley cost?")
print(result['response'])
```

### **Command Line Interface**
```bash
# Interactive mode
python app.py --user-id student123

# Single query
python app.py --non-interactive --query "What careers are available for psychology majors?"

# System statistics
python app.py --stats

# Help
python app.py --help
```

### **Testing**
```bash
# Run integration tests
python transfer_counselor/tests/test_system.py

# Test with API key
export OPENAI_API_KEY="your-key"
python transfer_counselor/tests/test_system.py
```

## 🔧 **Configuration Management**

The refactored system uses a sophisticated configuration system:

- **YAML Configuration**: Primary config in `config.yaml`
- **Environment Variables**: Override any config with env vars
- **Validation**: Automatic config validation and error reporting
- **Defaults**: Sensible defaults for all settings

## 🧪 **Testing Framework**

Comprehensive testing at multiple levels:

- **Unit Tests**: Individual module testing
- **Integration Tests**: End-to-end system testing  
- **API Tests**: OpenAI integration verification
- **Memory Tests**: Conversation continuity validation

## 📈 **Performance & Monitoring**

Built-in observability:

- **Structured Logging**: JSON-formatted logs with context
- **Performance Tracing**: Request timing and performance metrics
- **Error Tracking**: Comprehensive error reporting and recovery
- **Session Analytics**: Conversation flow and usage patterns

This refactored architecture makes the Transfer Counselor System more professional, maintainable, and ready for production deployment!