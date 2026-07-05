from collections import defaultdict
import time
from flask import request
from extension import db
from models import Alert, BlockedIP
from urllib.parse import unquote



class IDS:
    def __init__(self):
        self.request_log = defaultdict(list)
        self.failed_logins = defaultdict(list)


    # -----------------------------
    # 🚨 SAVE ALERT
    # -----------------------------
    def log_alert(self, ip, attack_type, risk, endpoint, user_id=None):
        alert = Alert(
            ip_address=ip,
            attack_type=attack_type,
            risk_level=risk,
            endpoint=endpoint,
            user_id=user_id
        )
        db.session.add(alert)
        db.session.commit()

    # -----------------------------
    # 🚫 SAVE BLOCKED IP
    # -----------------------------
    def save_blocked_ip(self, ip, attack_type):
        blocked = BlockedIP.query.filter_by(ip_address=ip).first()

        if not blocked:
            new_block = BlockedIP(ip_address=ip, reason=attack_type)
            db.session.add(new_block)
            db.session.commit()

    def record_failed_login(self, ip):
     now = time.time()

     self.failed_logins[ip].append(now)

    # keep only last 60 seconds
     self.failed_logins[ip] = [
        t for t in self.failed_logins[ip] if now - t < 60
    ]

     print(f"🔐 Failed login attempts for {ip}: {len(self.failed_logins[ip])}")

     if len(self.failed_logins[ip]) >= 5:
            print("🚨 BRUTE FORCE DETECTED")

            self.log_alert(ip, "Brute Force Attack", "High", "/login")
            self.save_blocked_ip(ip, "Brute Force Attack")

            return True
        
     return False
    # -----------------------------
    # 🛡️ MAIN IDS ENGINE
    # -----------------------------
    def inspect_request(self, request):

        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        if ip and "," in ip:
              ip = ip.split(",")[0].strip()      
        
        # ip = request.remote_addr
        endpoint = request.path
        now = time.time()
        
        print(f"✅ IDS CHECK IP: {ip} ENDPOINT: {endpoint}")
        print("📊 Requests for", ip, ":", len(self.request_log[ip]))

        # -----------------------------
        # SAFE ROUTES
        # -----------------------------
        safe_routes = ["/login", "/static"]

        if any(endpoint.startswith(route) for route in safe_routes):
            return None

        # -----------------------------
        # BLOCKED IP CHECK
        # -----------------------------
        blocked = BlockedIP.query.filter_by(ip_address=ip).first()
        if blocked:
            return "Access Denied (Blocked by IDS)", 403

        # -----------------------------
        # BUILD REQUEST STRING (FIXED)
        # -----------------------------
        full_request = unquote(
            str(request.args) +
            str(request.form) +
            str(request.data) +
            request.url
        ).lower()

        print("🔍 FULL REQUEST:", full_request)

# -----------------------------
# SQL INJECTION DETECTION
# -----------------------------
        patterns = [
            " or ",
            "'or",
            "1=1",
            "'='",
            "--",
            "select",
            "drop",
            "insert"
        ]

        for p in patterns:
            if p in full_request:

                print("⚠️ SQLi DETECTED:", p)

                self.log_alert(ip, "SQL Injection", "High", endpoint)
                self.save_blocked_ip(ip, "SQL Injection")

                return "Blocked: SQL Injection detected", 403
            
            
# -----------------------------
# 🧪 XSS Detection
# -----------------------------
        xss_patterns = [
                       "<script>",
                       "</script>",
                       "javascript:",
                       "onerror=",
                       "onload=",
                       "<img",
                       "<svg"
                       ]

        for pattern in xss_patterns:
            if pattern in full_request:

                attack_type = "XSS Attack"

                print("⚠️ XSS detected:", full_request)

                self.log_alert(ip, attack_type, "High", endpoint)
                self.save_blocked_ip(ip, attack_type)

                return "Blocked: XSS detected", 403   

        
# -----------------------------
# 🚨 DoS Detection
# -----------------------------
        self.request_log[ip].append(now)

# keep only last 1 second
        self.request_log[ip] = [t for t in self.request_log[ip] if now - t < 1]

        if len(self.request_log[ip]) > 10:
           print("🚨 DoS DETECTED")

           attack_type = "DoS Attack"

           self.log_alert(ip, attack_type, "High", endpoint)
           self.save_blocked_ip(ip, attack_type)

           return "Blocked: DoS detected", 403
    
    
    
    