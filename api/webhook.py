import os
import sys
import subprocess
import hmac
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

# GitHub Webhook Secret (Set this in Vercel Environment Variables)
GITHUB_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")

def verify_signature(payload, signature):
    """Verifies GitHub Webhook payload signature."""
    if not GITHUB_SECRET:
        return True  # Skip verification if no secret is set

    mac = hmac.new(GITHUB_SECRET.encode(), payload, hashlib.sha256).hexdigest()
    expected_signature = f"sha256={mac}"

    return hmac.compare_digest(expected_signature, signature)

@app.route('/api/webhook', methods=['POST'])
def webhook():
    """Listens for GitHub webhook events and triggers the optimization script."""
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
            print(f"❌ Error while executing gitagent.py: {e}")
            return jsonify({"message": f"Error executing script: {str(e)}"}), 500

    return jsonify({"message": "Invalid webhook event"}), 400

# Vercel entry point
def handler(event, context):
    return app(event, context)
