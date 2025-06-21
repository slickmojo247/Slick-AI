# Merges: think.py
import glob

class Think:
    @staticmethod
    def load_knowledge():
        return "\n".join(
            open(f).read() 
            for f in glob.glob("think/**/*.md", recursive=True)
        )
    
    def enhance(self, prompt):
        return f"Context:\n{self.load_knowledge()}\n\nQuery:{prompt}"