# Jira AI Duplicate Detector

**A project that automatically detects duplicate Jira issues using AI embedding.**

---

## 📋 Features

- Retrieve Jira issues in bulk via API
- Compare existing issues without creating new ones to detect similarity
- Use OpenAI `text-embedding-ada-002` model to embed title + description
- Detect duplicate issues based on a similarity threshold of **0.98 or higher**
- Output duplicate issue pairs to console + save to log file + export to Excel (.xlsx)
- Display the number of compared pairs, AI usage statistics, and estimated costs
- Exclude issues containing specific keywords (e.g., [UI])

---

## 📋 Project Structure

```
jira-ai-duplicate-detector/
├── main.py
├── config.py
├── setup_logger.py
├── modules/
│   ├── jira_client.py
│   ├── embedding_service.py
│   ├── cache_manager.py
│   ├── duplicate_checker.py
├── logs/
├── outputs/
├── requirements.txt
├── .env
└── README.md
```

---

## 📋 Installation and Usage

### 1. Create Virtual Environment & Install Packages

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 2. Setup .env File

```plaintext
OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXX
JIRA_URL=https://your-domain.atlassian.net
JIRA_USER=your-email@example.com
JIRA_TOKEN=your-jira-api-token
MAX_ISSUES=50       # Default
JQL_QUERY=project = 'YOUR_PROJECT' AND type IN ('Bug', 'Improvement', 'New Feature') AND summary !~ "\\[UI\\]" ORDER BY created DESC
CACHE_FILE=issue_embeddings_cache.json
```

✅ Note: Ensure you use single quotes (') and double backslashes (\\) correctly inside `JQL_QUERY`.

### 3. Run

```bash
python main.py
```

---

## 📋 Main Workflow

1. Fetch up to 1500 issues via Jira API
2. Exclude issues containing [UI] in their summary
3. Generate embeddings based on full text (title + description)
4. Calculate cosine similarity between issues
5. Filter pairs with similarity greater than or equal to 0.98
6. Output results to console, log file, and Excel file

---

## 📋 Example Output

```plaintext
[Similarity Results (threshold: 0.98)]
- [YOUR-388] TitleA ↔ [YOUR-386] TitleB (Similarity: 0.94)
- [YOUR-2175] TitleC ↔ [YOUR-2037] TitleD (Similarity: 0.95)
...

[INFO] Total 8 duplicate issue pairs detected.

[AI Usage Summary]
- Embedding API calls: 1440
- Total input length: 120,000 characters
- Total input tokens: 49,819 tokens
- Estimated embedding cost: $0.00498
```

- Log files saved in `/logs/`
- Excel result files saved in `/outputs/`

---

## 📋 Cost Reference

| Item | Value |
|:---|:---|
| Model | text-embedding-ada-002 |
| Price | $0.0001 per 1K tokens |
| 49.819K tokens usage cost | Approximately $0.00498 |

✅ Very low cost even for large-scale comparisons.

---

## 📋 How to Obtain API Keys

### OpenAI API Key

1. Visit [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
2. Log in to your OpenAI account.
3. Click "Create new secret key" and copy the generated key.

### Jira API Token

1. Visit [https://id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Log in with your Atlassian (Jira) account.
3. Click "Create API token", give it a label, and copy the generated token.
4. Use this token together with your Jira email when accessing the Jira REST API.

---

## 📋 Planned Improvements

- Add CLI option for threshold input
- Group results by left-side issue key
- Support multiple keyword exclusions
- Auto-post results to Slack or Discord

---

# Special Thanks

- This project was built based on my practical need for automated duplicate issue management.
- I developed it to improve QA workflow quality and save valuable time.

---
