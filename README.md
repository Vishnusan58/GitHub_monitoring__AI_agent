# **GitHub Monitoring AI Agent**  

This project is an **AI-powered GitHub monitoring agent** that automatically detects changes in a repository, summarizes the updated code, and provides optimized code suggestions. The agent is deployed on **Vercel** and integrated with **GitHub Webhooks** to trigger automatically on code updates.

---

## **📌 Features**
✔ **Monitors GitHub Repository**: Detects changes in code when a commit is pushed.  
✔ **AI-Powered Code Summary & Optimization**: Uses **Gemini AI** to analyze and suggest improvements.  
✔ **Automated Deployment on Vercel**: Runs as a serverless function using **Vercel GitHub Integration**.  
✔ **Webhook-Driven Execution**: Automatically triggers on `push` events.  

---

## **📂 Project Structure**
```
/your-project
│── /api
│   ├── webhook.py   # Webhook listener (Flask-based serverless function)
│── gitagent.py      # Script that fetches, summarizes, and optimizes code
│── requirements.txt # Dependencies for the project
│── vercel.json      # Vercel deployment configuration
│── README.md        # Project documentation (this file)
```

---

## **🛠️ Technologies Used**
- **Python** (Flask, aiohttp)
- **GitHub Webhooks** (for repository monitoring)
- **Vercel** (serverless deployment)
- **Gemini AI** (Google AI for code analysis)
- **Semantic Kernel** (for advanced AI workflows)

---

## **🚀 How It Works**
1. A **GitHub Webhook** triggers on **push events**.
2. The webhook **sends a request** to the **Vercel-hosted API** (`api/webhook.py`).
3. The API verifies the request and **triggers `gitagent.py`**.
4. `gitagent.py` fetches repository contents and **analyzes code using Gemini AI**.
5. The script **outputs optimized code suggestions**.

---

## **🔧 Setup & Deployment**

### **1️⃣ Fork & Clone the Repository**
```bash
git clone https://github.com/your-username/github-monitoring-ai-agent.git
cd github-monitoring-ai-agent
```

### **2️⃣ Push to Your GitHub Repository**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

### **3️⃣ Deploy to Vercel**
1. Go to [Vercel Dashboard](https://vercel.com/).
2. Click **New Project** → Select **GitHub Repository**.
3. Click **Deploy**.

### **4️⃣ Configure Environment Variables in Vercel**
- Go to **Project Settings → Environment Variables** and add:
  - `GITHUB_WEBHOOK_SECRET` → *(Same as GitHub Webhook Secret)*
  - `GITHUB_TOKEN` → *(Personal access token for API requests)*
  - `GEMINI_API_KEY` → *(Google Gemini API Key)*

### **5️⃣ Set Up GitHub Webhook**
1. Go to **GitHub → Your Repository → Settings → Webhooks**.
2. Click **Add Webhook**.
3. Set **Payload URL** to:
   ```
   https://your-vercel-project.vercel.app/api/webhook
   ```
4. Choose **Content type**: `application/json`.
5. Add **Secret** (same as `GITHUB_WEBHOOK_SECRET` in Vercel).
6. Choose `push` events and **Save**.

---

## **📜 Code Explanation**
### **📌 `api/webhook.py` (Webhook Listener)**
Handles incoming **GitHub Webhook events** and triggers `gitagent.py`:
```python
import os
import sys
import subprocess
import hmac
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

GITHUB_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")

def verify_signature(payload, signature):
    """Verifies GitHub Webhook payload signature."""
    if not GITHUB_SECRET:
        return True  # Allow all if no secret is set (for testing)

    mac = hmac.new(GITHUB_SECRET.encode(), payload, hashlib.sha256).hexdigest()
    expected_signature = f"sha256={mac}"
    return hmac.compare_digest(expected_signature, signature)

@app.route('/api/webhook', methods=['POST'])
def webhook():
    """Handles GitHub webhook and triggers `gitagent.py`."""
    signature = request.headers.get('X-Hub-Signature-256', '')
    payload = request.data

    if not verify_signature(payload, signature):
        return jsonify({"message": "Invalid signature"}), 403

    data = request.json
    if "ref" in data:
        print("🔄 Change detected in repository. Triggering optimization script...")

        try:
            process = subprocess.Popen(
                [sys.executable, os.path.join(os.getcwd(), "gitagent.py")],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()

            print("✅ Optimization script executed successfully!")
            print("📜 STDOUT:", stdout.decode().strip())
            print("⚠️ STDERR:", stderr.decode().strip())

            return jsonify({"message": "Optimization script triggered successfully"}), 200

        except Exception as e:
            return jsonify({"message": f"Error executing script: {str(e)}"}), 500

    return jsonify({"message": "Invalid webhook event"}), 400

# Vercel entry point
def handler(event, context):
    return app(event, context)
```

---

### **📌 `gitagent.py` (Code Summarization & Optimization)**
- Fetches **all files** in the GitHub repository.
- Uses **Google Gemini AI** to **summarize & optimize** code.
- Outputs **performance improvements, structure fixes, and security enhancements**.

Example AI prompt:
```python
summary_prompt = f"""
Summarize the following GitHub repository, including file contents:
1. Identify performance bottlenecks.
2. Suggest code structure improvements.
3. Highlight security vulnerabilities.
4. Provide an optimized version of one file.

Repository: {repo_url}
"""
```

---

## **🧪 Testing the Deployment**
### **1️⃣ Check Webhook Trigger**
Push a commit to GitHub:
```bash
git commit -am "Testing webhook deployment"
git push origin main
```
Go to **GitHub Webhooks → Recent Deliveries** and check the response.

### **2️⃣ View Vercel Logs**
Run:
```bash
vercel logs <your-vercel-project>
```
Or check **Project → Logs** in Vercel.

---

## **🚑 Troubleshooting**
| Issue                        | Solution |
|------------------------------|----------|
| Webhook request failing | Check **GitHub Webhook Logs** under **Recent Deliveries** |
| `403 FORBIDDEN` in logs | Ensure `GITHUB_WEBHOOK_SECRET` is correct in Vercel |
| `gitagent.py` not running | Modify `subprocess.Popen` to print errors |
| `404 NOT FOUND` on webhook | Ensure GitHub webhook URL is `https://your-vercel-project.vercel.app/api/webhook` |
| AI not summarizing | Check if `GEMINI_API_KEY` is valid |

---

## **🎯 Next Steps**
- [ ] Store optimized code **back to GitHub** via API.
- [ ] Improve AI prompt for **better code suggestions**.
- [ ] Add **unit tests** for webhook and AI response validation.
- [ ] Optimize AI model **cost-efficiency**.

---

## **📜 License**
This project is **open-source** under the **MIT License**.

---

## **🙌 Contributing**
Pull requests are welcome! Follow the GitHub **issues** tab for feature requests.

---

### **📩 Questions?**
For support, reach out via **GitHub Issues** or [email](mailto:your-email@example.com). 🚀
