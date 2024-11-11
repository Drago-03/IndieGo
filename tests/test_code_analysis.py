import pytest
from src.models.code_analysis import CodeAnalyzer

def test_complexity_calculation():
    analyzer = CodeAnalyzer()
    code = """
def complex_function(x):
    if x > 0:
        while x > 10:
            if x % 2 == 0:
                x -= 1
            else:
                x += 1
    return x
    """
    
    result = analyzer.analyze_code(code)
    assert result.complexity > 1

def test_security_check():
    analyzer = CodeAnalyzer()
    code = """
def unsafe_function():
    user_input = input()
    eval(user_input)
    """
    
    result = analyzer.analyze_code(code)
    assert len(result.security_issues) > 0
    assert any("eval()" in issue for issue in result.security_issues)

def test_best_practices():
    analyzer = CodeAnalyzer()
    code = """
def function_without_docstring(x):
    return x * 2
    """
    
    result = analyzer.analyze_code(code)
    assert len(result.best_practices) > 0
    assert any("docstring" in practice for practice in result.best_practices)

def test_performance_analysis():
    analyzer = CodeAnalyzer()
    code = """
def slow_function():
    result = ""
    for i in range(1000):
        result += str(i)
    return result
    """
    
    result = analyzer.analyze_code(code)
    assert len(result.performance_tips) > 0
    assert any("join()" in tip for tip in result.performance_tips)