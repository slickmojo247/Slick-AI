import csv
from pathlib import Path
from blueprint import ColorTagger, FileStatus
from typing import List, Dict

class DirectoryScanner:
    """Handles scanning of individual directories with reporting"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.tagger = ColorTagger()
        self.scan_results = []
    
    def scan_all_directories(self) -> List[Dict]:
        """Scan all directories in base path"""
        self.scan_results = []
        for directory in sorted(self.base_path.iterdir()):
            if directory.is_dir():
                result = self._scan_directory(directory)
                self.scan_results.append(result)
        return self.scan_results
    
    def _scan_directory(self, directory: Path) -> Dict:
        """Scan a single directory and return analysis"""
        scan_data = self.tagger.scan_directory(directory)
        return {
            'directory': str(directory),
            'file_count': len(scan_data),
            'status_distribution': self._get_status_counts(scan_data),
            'files': scan_data
        }
    
    def _get_status_counts(self, scan_data: Dict) -> Dict:
        """Count occurrences of each status type"""
        counts = {status.name: 0 for status in FileStatus}
        for file_data in scan_data.values():
            counts[file_data['status']] += 1
        return counts
    
    def generate_reports(self):
        """Generate CSV reports for each directory"""
        reports_dir = self.base_path / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        for result in self.scan_results:
            dir_name = Path(result['directory']).name
            report_path = reports_dir / f"{dir_name}_report.csv"
            
            with open(report_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['File', 'Status', 'Color', 'Size', 'Last Modified'])
                
                for file_path, data in result['files'].items():
                    writer.writerow([
                        Path(file_path).name,
                        data['status'],
                        data['color'],
                        data['size'],
                        data['modified']
                    ])

if __name__ == "__main__":
    scanner = DirectoryScanner("/mnt/c/Users/slick/OneDrive/Desktop/slick_ai_system")
    results = scanner.scan_all_directories()
    scanner.generate_reports()
    
    print(f"Scanned {len(results)} directories")
    print("Reports generated in 'reports' subdirectory")