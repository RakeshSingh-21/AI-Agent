from llama_cpp import Llama

llm = Llama(
    model_path=r"D:/Local_Models/meta-llama-3-8b-instruct.Q4_K_M.gguf",
    n_ctx=2048
)

def review_code(diff):
    prompt = f"""
You are a senior software engineer.

Review this PR diff and provide:
- Code quality issues
- Security risks
- Performance improvements
- Style suggestions

Diff:
{diff}
"""

    output = llm(prompt, max_tokens=500)

    return output["choices"][0]["text"]