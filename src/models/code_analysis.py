from typing import Dict, List
import ast
import re
from dataclasses import dataclass

@dataclass
class CodeAnalysisResult:
    """
    Stores the results of code analysis
    """
    complexity: int
    suggestions: List[str]
    security_issues: List[str]
    best_practices: List[str]
    performance_tips: List[str]

class CodeAnalyzer:
    """
    Analyzes code for various metrics and provides suggestions
    """
    def __init__(self):
        self.complexity_threshold = 10
        self.max_line_length = 80
        self.security_patterns = {
            r"eval\(": "Avoid using eval() as it can be dangerous",
            r"exec\(": "Avoid using exec() for security reasons",
            r"(?<![\w])input\(": "Ensure input validation is implemented",
            r"os\.system\(": "Use subprocess module instead of os.system",
        }

    def analyze_code(self, code: str) -> CodeAnalysisResult:
        """
        Perform comprehensive code analysis
        
        Args:
            code (str): Source code to analyze
            
        Returns:
            CodeAnalysisResult: Analysis results
        """
        try:
            tree = ast.parse(code)
            
            complexity = self._calculate_complexity(tree)
            suggestions = self._generate_suggestions(code, tree)
            security_issues = self._check_security(code)
            best_practices = self._check_best_practices(code, tree)
            performance_tips = self._analyze_performance(tree)
            
            return CodeAnalysisResult(
                complexity=complexity,
                suggestions=suggestions,
                security_issues=security_issues,
                best_practices=best_practices,
                performance_tips=performance_tips
            )
        except SyntaxError:
            return CodeAnalysisResult(
                complexity=0,
                suggestions=["Invalid Python syntax"],
                security_issues=[],
                best_practices=[],
                performance_tips=[]
            )

    def _calculate_complexity(self, tree: ast.AST) -> int:
        """
        Calculate cyclomatic complexity
        
        Args:
            tree (ast.AST): AST of the code
            
        Returns:
            int: Complexity score
        """
        complexity = 1
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        return complexity

    def _generate_suggestions(self, code: str, tree: ast.AST) -> List[str]:
        """
        Generate code improvement suggestions
        
        Args:
            code (str): Source code
            tree (ast.AST): AST of the code
            
        Returns:
            List[str]: List of suggestions
        """
        suggestions = []
        
        # Check line length
        lines = code.splitlines()
        for i, line in enumerate(lines, 1):
            if len(line) > self.max_line_length:
                suggestions.append(
                    f"Line {i} exceeds {self.max_line_length} characters"
                )

        # Check function length
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if len(node.body) > 15:
                    suggestions.append(
                        f"Function '{node.name}' is too long. Consider breaking it down."
                    )

        return suggestions

    def _check_security(self, code: str) -> List[str]:
        """
        Check for security issues
        
        Args:
            code (str): Source code
            
        Returns:
            List[str]: List of security issues
        """
        issues = []
        for pattern, message in self.security_patterns.items():
            if re.search(pattern, code):
                issues.append(message)
        return issues

    def _check_best_practices(self, code: str, tree: ast.AST) -> List[str]:
        """
        Check for Python best practices
        
        Args:
            code (str): Source code
            tree (ast.AST): AST of the code
            
        Returns:
            List[str]: List of best practice suggestions
        """
        practices = []
        
        # Check for docstrings
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    practices.append(
                        f"Add docstring to {node.__class__.__name__.lower()} '{node.name}'"
                    )

        # Check for type hints
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not node.returns and not any(
                    isinstance(a, ast.AnnAssign) for a in node.args.args
                ):
                    practices.append(
                        f"Consider adding type hints to function '{node.name}'"
                    )

        return practices

    def _analyze_performance(self, tree: ast.AST) -> List[str]:
        """
        Analyze code for performance improvements
        
        Args:
            tree (ast.AST): AST of the code
            
        Returns:
            List[str]: List of performance suggestions
        """
        tips = []
        
        for node in ast.walk(tree):
            # Check for list comprehension opportunities
            if isinstance(node, ast.For):
                if isinstance(node.body[0], ast.Append):
                    tips.append(
                        "Consider using list comprehension instead of for loop with append"
                    )
            
            # Check for multiple string concatenations
            elif isinstance(node, ast.BinOp):
                if isinstance(node.op, ast.Add):
                    if isinstance(node.left, ast.Str) or isinstance(node.right, ast.Str):
                        tips.append(
                            "Use join() instead of multiple string concatenations"
                        )

        return tips