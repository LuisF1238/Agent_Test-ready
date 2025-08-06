# Setup Instructions

## ✅ Installation Complete!

Your enhanced Transfer Counselor Agent System is now installed and ready to use.

## 🔑 Setting Your OpenAI API Key

**Required:** You need to set your OpenAI API key before running the system.

### Option 1: Environment Variable (Recommended)
```bash
export OPENAI_API_KEY="your-actual-api-key-here"
```

### Option 2: Edit the config file
Edit `config.yaml` and replace:
```yaml
openai_api_key: "your-openai-api-key-here"
```

## 🚀 Running the System

### Basic Interactive Mode
```bash
python enhanced_main.py
```

### With User Tracking
```bash
python enhanced_main.py --user-id student123
```

### Single Query (Non-Interactive)
```bash
python enhanced_main.py --non-interactive --query "How do I apply for financial aid?"
```

### System Statistics
```bash
python enhanced_main.py --stats
```

## 🎯 Example Questions to Try

Once you have your API key set, try these questions:

**Financial Aid:**
- "How do I apply for FAFSA for UC schools?"
- "What scholarships are available for transfer students?"
- "Compare the costs of UCLA vs SDSU"

**Career Guidance:**
- "What career paths are available with a psychology major?"
- "Should I choose UC Berkeley or Cal Poly for computer science?"
- "What's the job market like for business majors?"

**Academic Support:**
- "How can I manage organic chemistry while working?"
- "What study strategies work best for STEM courses?"
- "Help me plan my course sequence for engineering"

## 🔧 Features Available

✅ **Intelligent Agent Routing** - Automatically routes questions to the right specialist
✅ **Session Persistence** - Remembers your conversation across sessions  
✅ **Context Awareness** - Maintains context as you talk to different agents
✅ **Error Recovery** - Graceful handling of issues with retry mechanisms
✅ **Performance Monitoring** - Real-time statistics and analytics
✅ **Multi-Agent Handoffs** - Seamless transitions between specialists

## 📊 Interactive Commands

While in interactive mode, you can use these commands:
- `stats` - Show system statistics
- `history` - Show conversation history  
- `help` - Show available commands
- `quit` - End session

## 🛠 Troubleshooting

If you encounter issues:

1. **API Key Error**: Make sure your OpenAI API key is set correctly
2. **Import Errors**: Run `python simple_test.py` to verify installation
3. **Permission Issues**: Check file permissions for `sessions.db`
4. **Network Issues**: Check your internet connection for OpenAI API access

## 🎯 Next Steps

Your system is ready! Set your API key and start exploring the enhanced multi-agent counseling system.