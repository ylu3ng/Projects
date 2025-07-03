import os
from sympy import symbols, integrate, sympify, Symbol, solve # Added 'solve' for sympy_solve_equation
from sympy.parsing.mathematica import parse_mathematica # Useful if inputs are Mathematica-like
import wolframalpha
import json # For handling JSON inputs for StructuredTool

# --- Configuration for APIs ---
# IMPORTANT: Replace with your actual App ID for Wolfram Alpha.
WOLFRAM_ALPHA_APP_ID = "4PL699-V7PYHX5W4K" # <<< IMPORTANT: GET YOUR OWN!

# Initialize Wolfram Alpha Client (if App ID is available)
wolfram_client = None
if WOLFRAM_ALPHA_APP_ID != "4PL699-V7PYHX5W4K":
    try:
        wolfram_client = wolframalpha.Client(WOLFRAM_ALPHA_APP_ID)
        print("Wolfram Alpha client initialized successfully.")
    except Exception as e:
        print(f"Warning: Could not initialize Wolfram Alpha client. Ensure App ID is correct. Error: {e}")
        print("Wolfram Alpha tool will not be available.")
else:
    print("Wolfram Alpha App ID not set. Wolfram Alpha tool will not be available.")

# --- Python Functions representing our Tools ---

def sympy_integrate(expression_str: str, variable_str: str, lower_limit: float = None, upper_limit: float = None) -> str:
    """
    Performs symbolic integration of a mathematical expression with respect to a given variable.
    Can perform indefinite or definite integration.
    Args:
        expression_str: The mathematical expression to integrate (e.g., "x**2", "k*x*(1-x)").
        variable_str: The variable to integrate with respect to (e.g., "x", "y").
        lower_limit (optional): The lower bound for definite integration (e.g., 0).
        upper_limit (optional): The upper bound for definite integration (e.g., 1).
    Returns:
        A string representation of the integration result.
    Example indefinite: sympy_integrate("x**2", "x") -> "x**3/3"
    Example definite: sympy_integrate("x**2", "x", 0, 1) -> "1/3"
    """
    try:
        var = Symbol(variable_str)
        expr = sympify(expression_str)

        if lower_limit is not None and upper_limit is not None:
            # Definite integral
            result = integrate(expr, (var, lower_limit, upper_limit))
        else:
            # Indefinite integral
            result = integrate(expr, var)

        return str(result)
    except Exception as e:
        return f"Error performing SymPy integration: {e}. Check expression, variable, and limits."


def sympy_solve_equation(equation_str: str, variable_str: str) -> str:
    """
    Solves a mathematical equation symbolically for a given variable.
    SymPy's solve function assumes the expression equals zero.
    Args:
        equation_str: The equation to solve (e.g., "x**2 - 4", "k*x - 3").
        variable_str: The variable to solve for (e.g., "x", "k").
    Returns:
        A string representation of the solutions.
    Example: sympy_solve_equation("x**2 - 4", "x") -> "[-2, 2]"
    """
    try:
        var = Symbol(variable_str)
        expr = sympify(equation_str)
        solutions = solve(expr, var) # Using solve from sympy
        return str(solutions)
    except Exception as e:
        return f"Error solving equation with SymPy: {e}. Check equation and variable."

def wolfram_alpha_query(query: str) -> str:
    """
    Queries Wolfram Alpha for a factual or computational answer.
    Use for complex calculations, specific data lookups (e.g., properties of distributions),
    or when precise numerical answers are needed for something SymPy can't handle directly.
    Args:
        query: A concise query string optimized for Wolfram Alpha (e.g., "Normal distribution PDF", "integrate x^2 from 0 to 1").
    Returns:
        A string containing the most relevant result from Wolfram Alpha.
        Returns an error message if the client is not initialized or query fails.
    """
    if wolfram_client is None:
        return "Wolfram Alpha tool is not available (API key not set or invalid)."
    try:
        print(f"Calling Wolfram Alpha with query: '{query}'") # For debugging
        res = wolfram_client.query(query)
        # Iterate through pods to find a "Result" or "Solution" or "Definition"
        # Wolfram Alpha output can be complex; this is a simplified parser.
        for pod in res.pods:
            if pod.title in ["Result", "Solution", "Definition", "Input interpretation", "Value"]:
                if hasattr(pod, 'text'): # Check if the pod has direct text content
                    return pod.text
                elif hasattr(pod, 'subpods'): # Some results are in subpods
                    for subpod in pod.subpods:
                        if hasattr(subpod, 'plaintext'):
                            return subpod.plaintext
        # Fallback if no specific result pod is found, return all available text
        all_text_results = []
        for pod in res.pods:
            if hasattr(pod, 'text'):
                all_text_results.append(pod.text)
            elif hasattr(pod, 'subpods'):
                for subpod in pod.subpods:
                    if hasattr(subpod, 'plaintext'):
                        all_text_results.append(subpod.plaintext)
        if all_text_results:
            return "\n".join(all_text_results)
        return "No direct textual result found from Wolfram Alpha."
    except Exception as e:
        return f"Error querying Wolfram Alpha: {e}. Please ensure the query is precise and within API limits."

# --- LangChain Tool Definitions ---
from langchain.tools import Tool, StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field # Ensure this import is used!

# Input schema for SymPyIntegrate
class SymPyIntegrateInput(BaseModel):
    expression_str: str = Field(description="The mathematical expression to integrate (e.g., 'x**2', 'k*x*(1-x)').")
    variable_str: str = Field(description="The variable to integrate with respect to (e.g., 'x', 'y').")
    lower_limit: float = Field(default=None, description="The lower bound for definite integration (e.g., 0.0). Use None for indefinite integral.")
    upper_limit: float = Field(default=None, description="The upper bound for definite integration (e.g., 1.0). Use None for indefinite integral.")

# Input schema for SymPySolveEquation
class SymPySolveEquationInput(BaseModel):
    equation_str: str = Field(description="The equation to solve, assuming it equals zero (e.g., 'x**2 - 4', 'k*(1/6) - 1').")
    variable_str: str = Field(description="The variable to solve for (e.g., 'x', 'k').")

# Define the tools list for the agent
tools = [
    StructuredTool.from_function(
        func=sympy_integrate,
        name="SymPyIntegrate",
        description="Performs symbolic definite or indefinite integration of a mathematical expression. Ideal for finding areas under curves, total probabilities from PDFs, expected values, or indefinite integrals.",
        args_schema=SymPyIntegrateInput
    ),
    StructuredTool.from_function(
        func=sympy_solve_equation,
        name="SymPySolveEquation",
        description="Solves a mathematical equation symbolically for a given variable, assuming the expression equals zero. Useful for finding roots, specific constant values, or critical points.",
        args_schema=SymPySolveEquationInput
    ),
    Tool(
        name="WolframAlpha",
        func=wolfram_alpha_query,
        description="Queries Wolfram Alpha for factual information, complex numerical computations, specific statistical tests, or when SymPy cannot handle a query directly. Input should be a concise, direct query string (e.g., 'Normal distribution PDF', 'integrate x^2 from 0 to 1'). Prioritize this for quick lookups or very complex problems that might exceed SymPy's immediate capabilities or your defined SymPy tools.",
    )
]

print("\n--- Tools Defined ---")
for tool in tools:
    print(f"Tool Name: {tool.name}")
    print(f"  Description: {tool.description}")
    # The 'schema' attribute is specifically on the args_schema object itself.
    if hasattr(tool, 'args_schema') and tool.args_schema is not None:
        print(f"  Arguments Schema: {tool.args_schema.schema()}")
    else:
        print("  Arguments Schema: N/A (or not a StructuredTool)")
    print("-" * 20)