from app.schemas.retrieval import RetrievalResult



def build_context(
    results: list[RetrievalResult],
)->str:
    if not results:
        return ""

    context_parts = []

    for index, result in enumerate(results,start=1):
        
        source =  result.source

        if result.start_line is not None and result.end_line is not None:

            source = (
                f"{source}:"
                f"{result.start_line}-"
                f"{result.end_line}"
            )

        context_parts.append(
            f"[Source {index}: {source}]\n"
            f"{result.content}"
        )

    return "\n\n".join(context_parts)


def build_rag_prompt(
        query:str,
        rag_context:str,
):
    return f"""
You are an AI software engineering assistant.

You answer questions about a GitHub repository.

Use the retrieved repository context as a starting
point, but do not assume it is complete or relevant.

When the retrieved context does not directly answer
the user's question, use the available repository
tools.

For implementation questions:

1. Search the repository for relevant keywords,
   classes, functions, or files.
2. Read the most relevant source files.
3. Base your answer on the actual source code.
4. Prefer specific source-code evidence over guesses.
5. Do not use unrelated files as evidence.
6. If the repository does not contain enough
   information, clearly say so.

Retrieved repository context:

{rag_context}

User question:

{query}

Provide a concise and technically accurate answer.
"""