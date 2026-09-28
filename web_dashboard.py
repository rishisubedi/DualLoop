import http.server
import socketserver
import json
import subprocess
import os

class AgentDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
            
        elif self.path == '/api/state':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            try:
                with open('state.json', 'rb') as f:
                    self.wfile.write(f.read())
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return
            
        elif self.path == '/api/qualified_jobs':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            try:
                with open('qualified_jobs.json', 'rb') as f:
                    self.wfile.write(f.read())
            except Exception:
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
