# LockDown Browser Bypass

This project demonstrates a security vulnerability in Respondus LockDown Browser by implementing a bypass mechanism using the Helium browser. The implementation includes an AI agent that can assist with exam questions while remaining undetectable by LockDown Browser's monitoring systems.

## ⚠️ Disclaimer

This project is for educational purposes only. Using this tool to bypass security measures in an actual exam environment may violate academic integrity policies and could result in serious consequences. The authors do not condone or encourage the use of this tool for cheating.

## 🚀 Features

- Stealthy browser automation that evades LockDown Browser detection
- AI-powered assistance using OpenAI's GPT models
- Custom Chrome profile to appear as a normal browser
- Process monitoring to detect LockDown Browser presence
- Secure API communication through browser network stack

## 📋 Requirements

### System Requirements

- macOS (tested on macOS High Sierra)
- Python 3.7 or higher
- Chrome/Chromium browser installed
- Helium browser installed

### ⚠️ Mac Compatibility Note

This project has been tested and confirmed working on Intel-based Macs. While it may work on Apple Silicon (M1/M2/M3) Macs through Rosetta 2, this has not been thoroughly tested. I have been hesitant to fully test this on my ARM Mac because this requires the installation of Rosetta 2, which is notoriously painful to uninstall. Do so at your own risk, but I strongly discourage anyone from doing this.

Secondly, Respondus has been known to brick computers, as seen on several occasions in my tutorials. I strongly discourage anyone from using this this software and exploiting this vulnerability, not only because of the ethical implications of attempting to bypass software intended to prevent access to disallowed material in exams, but also because playing around with the intrinsic workings of software that has deep access and permissions to your system is irresponsible. This is also why I have not run this software on my ARM Mac, as it's my primary device that I use for work. Do so at your own risk.

### Python Dependencies

```
selenium>=4.0.0
webdriver_manager>=3.8.0
openai>=1.0.0
python-dotenv>=0.19.0
psutil>=5.8.0
```

## 🔧 Installation

1. Clone the repository

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file:

```bash
cp .env.example .env
```

5. Edit the `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

## ⚙️ Configuration

The project uses a `config.py` file for configuration. Some necessary settings include:

- `EXAM_URL`: The URL of the exam to access
- `OPENAI_MODEL`: The GPT model to use (default: "gpt-4")
- `OPENAI_MAX_TOKENS`: Maximum tokens for API responses
- `OPENAI_TEMPERATURE`: Response creativity level (0.0-1.0)
- `PAGE_LOAD_TIMEOUT`: Timeout for page loading
- `MONITOR_INTERVAL`: Process monitoring interval
- `LOG_LEVEL`: Logging verbosity

## 🏃‍♂️ Usage

1. Start the bypass:

```bash
python lockdown-bypass.py
```

2. The script will:
   - Launch a Chrome/Helium instance
   - Navigate to the exam URL
   - Start monitoring for LockDown Browser detection
   - Initialize the AI agent for assistance

3. To stop the bypass:
   - Press Ctrl+C in the terminal
   - The script will gracefully shut down all processes

## 🔍 How It Works

### Browser Stealth

- Uses a custom Chrome profile that mimics a normal user profile
- Disables automation flags that Respondus looks for
- Hides webdriver presence through CDP commands
- Uses standard browser headers and user agent

### API Communication

- All API requests are made through the browser's network stack
- Requests appear as normal browser traffic
- No separate communication processes
- No suspicious file operations or network sockets

### Process Monitoring

- Continuously monitors for LockDown Browser processes
- Detects and logs any Respondus-related activity
- Maintains browser responsiveness
- Handles errors gracefully

## 🛠️ Development

### Project Structure

```
lockdown-browser-bypass/
├── ai_agent.py          # AI assistance implementation
├── lockdown-bypass.py   # Main bypass script
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── .env.example       # Environment template
└── README.md          # This file
```

## ⚠️ Security Considerations

- The project uses stealth measures to avoid detection
- All communication is done through the browser's network stack
- No suspicious processes or system calls
- No separate communication channels
- No file operations that Respondus might detect

## 🔒 Privacy

- No data is stored locally
- API keys are stored in `.env` file (not committed to git)
- Conversation history is kept in memory only
- No logging of sensitive information

## 🆘 Troubleshooting

### Common Issues

1. **Chrome/Helium not found**
   - Ensure Chrome is installed
   - Install Helium browser
   - Check PATH environment variable

2. **OpenAI API errors**
   - Verify API key in `.env` file
   - Check internet connection
   - Ensure sufficient API credits

3. **Browser automation detection**
   - Clear browser cache
   - Delete Chrome profile directory
   - Restart the script

### Getting Help

If you encounter issues:

1. Check the logs for error messages
2. Verify all requirements are met
3. Ensure proper configuration
4. Open an issue on GitHub

## 📚 Resources

- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [Respondus LockDown Browser](https://web.respondus.com/he/lockdownbrowser/)
