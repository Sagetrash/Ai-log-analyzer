# 🛠️ Ai-log-analyzer (WIP)

**Ai-log-analyzer** is a developer-focused tool for extracting insights, summaries, and anomalies from application logs using AI. It combines a Python backend with a simple HTML web interface.

> **Note:** This project is under active development. Features and CLI commands are subject to change.

---

## ✨ Features

- **Summarization:** Turn massive log files into human-readable reports.
- **Natural Language Search:** Query logs using plain English (e.g., "Find all 500 errors from last night").
- **Anomaly Detection:** Automatically flag unusual patterns or spikes.
- **Extensible:** Support for various LLM providers (OpenAI, Anthropic) or local models.

---

## 🚀 Quickstart

### 1. Installation

```bash
git clone [https://github.com/Sagetrash/Ai-log-analyzer.git](https://github.com/Sagetrash/Ai-log-analyzer.git)
cd Ai-log-analyzer
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Configuration

Create a .env file in the root directory:

```env
AI_PROVIDER=openai
AI_API_KEY=your_api_key_here
```

3. Usage

CLI Mode:

```Bash

python -m ai_log_analyzer.cli analyze --input logs/app.log
```

Web UI:
Bash

```bsh
python -m ai_log_analyzer.webapp
# Navigate to http://localhost:5000
```

```
📂 Project Structure

    ai_log_analyzer/ - Core logic and AI connectors.

    web/ - UI templates and assets.

    tests/ - Unit and integration tests.
```

🔒 Security & Privacy

Logs often contain sensitive data. Before processing:

    Use local LLMs for private/sensitive data.

    Ensure PII is redacted before sending to third-party APIs.

🤝 Contributing

Feel free to open issues or submit pull requests.

Maintainer: Sagetrash

```

```
