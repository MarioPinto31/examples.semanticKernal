# Integrating LangSmith with Semantic Kernel for Debugging

This guide demonstrates how to integrate **LangSmith** into a **Semantic Kernel** project for powerful tracing and debugging.

A common misconception is that you need to use the **LangChain** framework to use LangSmith. However, LangSmith is a standalone observability platform that can be integrated with any LLM application — including one built purely with Semantic Kernel.

The integration is achieved by using the `langsmith` Python package, which provides decorators and context managers to capture the execution flow of your kernel and send it to your LangSmith project for visualization.

---

## Step 1: Prerequisites

First, ensure you have the necessary Python packages installed in your environment:

```bash
pip install semantic-kernel python-dotenv langsmith

```

## Step 2: Set Up Your Environment

It is a best practice to manage secrets and configuration using environment variables.
Create a .env file in your project’s root directory.

⚠️ Never hardcode secrets directly in your code.
```bash
# .env file

# For Semantic Kernel (using Azure OpenAI as an example)
AZURE_OPENAI_API_KEY="YOUR_AZURE_OPENAI_KEY"
AZURE_OPENAI_ENDPOINT="YOUR_AZURE_OPENAI_ENDPOINT"
AZURE_OPENAI_DEPLOYMENT_NAME="YOUR_DEPLOYMENT_NAME"

# For LangSmith Tracing
LANGSMITH_API_KEY="YOUR_LANGSMITH_API_KEY"
```

## Step 3: Example Code

The following script sets up a simple Semantic Kernel with a math plugin (tool).
We wrap the main execution logic in a LangSmith @traceable decorator, which automatically captures the entire process.


```python
import os
import asyncio
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import kernel_function
from langsmith import traceable  # Key import for LangSmith integration
from dotenv import load_dotenv

# --- 1. Initial Setup ---

# Load environment variables from your .env file
load_dotenv()

# Configure LangSmith by setting environment variables
# The `langsmith` package will automatically detect these.
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "My Semantic Kernel Project"  # Optional: Name your project

# Initialize the Semantic Kernel
kernel = sk.Kernel()

# Add your LLM service (e.g., Azure OpenAI)
service_id = "default"
kernel.add_service(
    AzureChatCompletion(
        service_id=service_id,
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    )
)


# --- 2. Create a Plugin (a "Tool" to be traced) ---

class MathPlugin:
    """A simple plugin that the LLM can use."""
    @kernel_function(name="add", description="Adds two numbers.")
    def add(self, number1: int, number2: int) -> int:
        """A native function that adds two integers."""
        print(f"Tool Call: Running add({number1}, {number2})")
        return number1 + number2

# Register the plugin with the kernel so the LLM can find it
kernel.add_plugin(MathPlugin(), plugin_name="math")


# --- 3. Define the Main Logic to be Traced ---

# The @traceable decorator tells LangSmith to record this function's execution.
# We give it a name to easily identify it in the LangSmith UI.
@traceable(run_type="chain", name="SK Solver with Tool Call")
async def run_kernel_with_tool(problem: str):
    """
    Invokes the kernel to solve a problem, potentially using tools.
    This entire operation will be traced as a single run in LangSmith.
    """
    # Create settings to enable the LLM to use our "add" tool
    execution_settings = sk.connectors.ai.open_ai.OpenAIPromptExecutionSettings(
        service_id=service_id,
        tool_choice="auto",
    )

    # Define a prompt that encourages using the tool
    prompt = f"""
    Solve the following math problem: {problem}
    If you need to add numbers, use the `math.add` tool.
    Explain your steps.
    """

    # Invoke the kernel
    result = await kernel.invoke_prompt(
        prompt,
        arguments=sk.KernelArguments(settings=execution_settings)
    )
    return result

# --- 4. Run the Code ---

async def main():
    problem = "What is the result of 512 + 1024?"
    print(f"Solving: '{problem}'")

    # When we call this function, the trace will be sent to LangSmith
    final_answer = await run_kernel_with_tool(problem)

    print("\n--- Final LLM Answer ---")
    print(final_answer)
    print("\n✅ Execution complete. Go to your LangSmith project to see the trace!")


if __name__ == "__main__":
    asyncio.run(main())

```

## Step 4: Check the Trace in LangSmith

After running the Python script, navigate to your project in the LangSmith dashboard.
You will find a new trace named “SK Solver with Tool Call”.

- Clicking on it will reveal a detailed, hierarchical view of the entire execution, allowing you to inspect every step:

- Parent Run (SK Solver with Tool Call): The top-level run corresponding to the function decorated with @traceable.

- LLM Call: The initial request sent to the Azure OpenAI model, including the exact prompt.

- Tool Call (math.add): Shows that the LLM correctly decided to use your tool, along with the arguments it passed (number1: 512, number2: 1024).

- Tool Output: The value returned by your add function (1536).

Final LLM Call: The subsequent call to the model, where it incorporates the tool’s output to construct the final, human-readable answer.