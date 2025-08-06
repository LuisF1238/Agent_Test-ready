# Setting Up OpenAI API Key

The Enhanced Transfer Counselor System now uses the official OpenAI Agents SDK, which requires a valid OpenAI API key to make actual AI-powered responses.

## 🔑 How to Set Your API Key

### Method 1: Environment Variable (Recommended)

1. **Get your OpenAI API key** from https://platform.openai.com/api-keys

2. **Set the environment variable**:
   ```bash
   export OPENAI_API_KEY="sk-your-actual-api-key-here"
   ```

3. **Verify it's set**:
   ```bash
   echo $OPENAI_API_KEY
   ```

### Method 2: Configuration File

1. Edit `config.yaml` and add your API key:
   ```yaml
   openai_api_key: "sk-your-actual-api-key-here"
   ```

## 🧪 Testing Your API Key

Run the test script to verify your API key works:

```bash
python test_api_integration.py
```

Expected output with valid API key:
```
🔑 Testing OpenAI API Key Integration
--------------------------------------------------
✅ API key found: sk-proj...xyz1
🔧 Configuring OpenAI Agents SDK...
✅ API key configured successfully
🤖 Creating test agent...
✅ Test agent created successfully
🚀 Testing Runner.run_sync...
✅ API call successful!
📝 Response: Hello! I can confirm that I'm successfully connected to the OpenAI API.
```

## 🚀 Using the System with API Key

Once your API key is configured, the system will use actual AI responses instead of fallback responses:

```bash
# Interactive mode with AI responses
python enhanced_main.py

# Single query with AI responses
python enhanced_main.py --non-interactive --query "How much does UC Berkeley cost?"
```

## 📊 System Behavior

### With Valid API Key:
- ✅ Uses OpenAI GPT models for intelligent responses
- ✅ Proper agent handoffs and coordination
- ✅ Contextual, personalized advice
- ✅ Dynamic conversation flow

### Without API Key (Fallback Mode):
- ⚠️ Uses pre-written fallback responses
- ⚠️ Limited interactivity
- ⚠️ Static, templated responses
- ✅ All system features still work (sessions, tracing, etc.)

## 💡 API Key Requirements

- **Format**: Must start with `sk-`
- **Permissions**: Needs access to GPT models (GPT-4 recommended)
- **Credits**: Ensure you have sufficient API credits
- **Rate Limits**: Be aware of your account's rate limits

## 🔒 Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for production deployments
3. **Rotate keys regularly** for security
4. **Monitor usage** through OpenAI dashboard
5. **Set spending limits** to avoid unexpected charges

## 📞 Support

If you're having issues with API key configuration:

1. Check the troubleshooting section in README_Enhanced.md
2. Run `python test_api_integration.py` for diagnostics
3. Verify your API key at https://platform.openai.com/api-keys
4. Check your OpenAI account credits and limits