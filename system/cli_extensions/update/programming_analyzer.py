# programming_analyzer.py
import ast
import complexity

class CodeAnalyzer:
    def __init__(self):
        self.metrics = {
            'cyclomatic': complexity.CyclomaticComplexity(),
            'maintainability': complexity.MaintainabilityIndex()
        }
    
    def analyze(self, code):
        try:
            tree = ast.parse(code)
            results = {
                'quality_score': 0,
                'quality_feedback': '',
                'improvements': [],
                'performance_analysis': '',
                'complexity': {}
            }
            
            # Calculate metrics
            for name, metric in self.metrics.items():
                results['complexity'][name] = metric.calculate(tree)
            
            # Generate feedback
            results['quality_score'] = self._calculate_score(results['complexity'])
            results['quality_feedback'] = self._generate_feedback(results)
            results['improvements'] = self._suggest_improvements(tree)
            results['performance_analysis'] = self._analyze_performance(tree)
            
            return results
            
        except Exception as e:
            return {
                'error': f"Analysis failed: {str(e)}",
                'quality_score': 0,
                'improvements': ["Fix syntax errors first"]
            }
    
    def _calculate_score(self, metrics):
        # Simplified scoring logic
        base_score = 8
        if metrics['cyclomatic'] > 10:
            base_score -= 2
        if metrics['maintainability'] < 70:
            base_score -= 1
        return max(1, min(10, base_score))
    
    def _generate_feedback(self, results):
        feedback = []
        if results['complexity']['cyclomatic'] > 10:
            feedback.append("Code is too complex - consider refactoring")
        if results['complexity']['maintainability'] < 70:
            feedback.append("Maintainability could be improved")
        return ". ".join(feedback) if feedback else "Code looks good!"
    
    def _suggest_improvements(self, tree):
        # Simplified improvement suggestions
        suggestions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and len(node.body) > 30:
                suggestions.append(f"Function '{node.name}' is too long - split into smaller functions")
        return suggestions or ["No major improvements needed"]
    
    def _analyze_performance(self, tree):
        # Simplified performance analysis
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                return "Found loops - consider vectorization if possible"
        return "No obvious performance issues detected"