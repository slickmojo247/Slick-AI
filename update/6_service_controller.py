# Merges: services.py, S.py, U.py
import subprocess

class ServiceManager:
    SERVICES = {
        "ai": "python -m ai_server",
        "telegram": "python -m telegram_bot"
    }
    
    def restart(self, service):
        subprocess.run(["pkill", "-f", self.SERVICES[service]])
        subprocess.Popen(self.SERVICES[service].split())
    
    def update(self):
        subprocess.run(["git", "pull"])
        [self.restart(s) for s in self.SERVICES]