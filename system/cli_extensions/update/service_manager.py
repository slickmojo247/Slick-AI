# services/service_manager.py
import subprocess
from typing import Dict

class ServiceManager:
    SERVICES = {
        "ai": "python -m ai_server",
        "telegram": "python -m telegram_bot",
        "vscode": "python -m vscode_bridge"
    }
    
    def __init__(self):
        self.status = {name: "stopped" for name in self.SERVICES}
    
    def restart(self, service: str) -> Dict:
        subprocess.run(["pkill", "-f", self.SERVICES[service]])
        subprocess.Popen(self.SERVICES[service].split())
        self.status[service] = "running"
        return {"status": "success", "service": service}
    
    def update_all(self) -> Dict:
        subprocess.run(["git", "pull"])
        results = {}
        for service in self.SERVICES:
            results[service] = self.restart(service)
        return results
    
    def get_status(self) -> Dict:
        return self.status