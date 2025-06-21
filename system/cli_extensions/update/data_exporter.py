import pandas as pd

class SystemDataExporter:
    def generate_report(self, scope="all"):
        data = {
            'memory': self._get_memory_data(),
            'knowledge': self._get_knowledge_data()
        }
        return pd.DataFrame(data[scope]).to_csv(index=False)
    
    def _get_memory_data(self):
        return [mem for mem in controller.memory_bank.long_term.values()]