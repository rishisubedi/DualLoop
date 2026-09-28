import http.server
import socketserver
import json
import subprocess
import os
import time
import sqlite3

DB_NAME = 'career_agent.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS applied_jobs (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    company TEXT,
                    url TEXT,
                    applied_timestamp REAL,
                    status TEXT
                )''')
    # Migrate existing data from state.json if present
    try:
        with open('state.json', 'r') as f:
            state = json.load(f)
            for j in state.get('applied_jobs', []):
                if isinstance(j, dict):
                    c.execute("INSERT OR IGNORE INTO applied_jobs (id, title, company, url, applied_timestamp, status) VALUES (?, ?, ?, ?, ?, ?)", 
                              (j['id'], j.get('title',''), j.get('company',''), j.get('url',''), j.get('applied_timestamp', time.time()), 'Applied'))
    except Exception as e:
        print(f"Migration check: {e}")
    conn.commit()
    conn.close()

init_db()

class AgentDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
            
        elif self.path == '/api/state':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            try:
                with open('state.json', 'r') as f:
                    state = json.load(f)
                
                # Get accurate applied count from DB
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("SELECT COUNT(*) FROM applied_jobs")
                state['applied_db_count'] = c.fetchone()[0]
                conn.close()
                
                self.wfile.write(json.dumps(state).encode())
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return
            
        elif self.path == '/api/qualified_jobs':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            try:
                with open('qualified_jobs.json', 'r') as f:
                    qualified = json.load(f)
                
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("SELECT id FROM applied_jobs")
                applied_ids = {r[0] for r in c.fetchall()}
                conn.close()
                    
                filtered = [q for q in qualified if q.get('id') not in applied_ids]
                self.wfile.write(json.dumps(filtered).encode('utf-8'))
            except Exception:
                self.wfile.write(json.dumps([]).encode())
            return
            
        elif self.path == '/api/applied_jobs':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            try:
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("SELECT id, title, company, url, applied_timestamp, status FROM applied_jobs ORDER BY applied_timestamp DESC")
                rows = c.fetchall()
                conn.close()
                
                jobs = []
                for r in rows:
                    jobs.append({
                        "id": r[0], "title": r[1], "company": r[2], 
                        "url": r[3], "applied_timestamp": r[4], "status": r[5]
                    })
                self.wfile.write(json.dumps(jobs).encode('utf-8'))
            except Exception as e:
                self.wfile.write(json.dumps([]).encode())
            return
            
        return super().do_GET()

    def do_POST(self):
        if self.path.startswith('/api/run/'):
            agent = self.path.split('/')[-1]
            script_map = {
                'agent1': 'visa_sponsorship_qualifier.py',
                'agent2': 'profile_alignment_engine.py',
                'agent5': 'micro_challenge_generator.py'
            }
            
            if agent in script_map:
                script = script_map[agent]
                print(f"Running {script}...")
                result = subprocess.run(["python", script], capture_output=True, text=True)
                self._send_json({"log": result.stdout, "status": result.returncode})
            else:
                self.send_response(404)
                self.end_headers()
                
        elif self.path == '/api/apply':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            job_data = json.loads(post_data.decode('utf-8'))
            
            try:
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("INSERT OR REPLACE INTO applied_jobs (id, title, company, url, applied_timestamp, status) VALUES (?, ?, ?, ?, ?, ?)",
                          (job_data['id'], job_data.get('title',''), job_data.get('company',''), job_data.get('url',''), time.time(), 'Applied'))
                conn.commit()
                conn.close()
                self._send_json({"status": "success"})
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                
        elif self.path.startswith('/api/update_status/'):
            job_id = self.path.split('/')[-1]
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            new_status = post_data.get('status', 'Applied')
            
            try:
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("UPDATE applied_jobs SET status = ? WHERE id = ?", (new_status, job_id))
                conn.commit()
                conn.close()
                self._send_json({"status": "success"})
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                
        elif self.path.startswith('/api/remove_application/'):
            job_id = self.path.split('/')[-1]
            try:
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("DELETE FROM applied_jobs WHERE id = ?", (job_id,))
                conn.commit()
                conn.close()
                self._send_json({"status": "success"})
            except Exception as e:
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def _send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

if __name__ == "__main__":
    PORT = 8080
    print("==================================================")
    print(f"Dual-Loop Agent GUI active!")
    print(f"Open your browser to: http://localhost:{PORT}")
    print("==================================================")
    with socketserver.TCPServer(("", PORT), AgentDashboardHandler) as httpd:
        httpd.serve_forever()
