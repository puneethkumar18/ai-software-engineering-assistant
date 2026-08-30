import ast

from tree_sitter import Language, Parser
import tree_sitter_cpp

from app.chunking.chunk import Chunk
from app.ingestion.document import Document




def chunk_python_document(document: Document) -> list[Chunk]:

    tree = ast.parse(document.content)

    chunks = []
    lines = document.content.splitlines()

    nodes = [
        node
        for node in ast.walk(tree)
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
                ast.ClassDef,
            ),
        )
    ]

    for index, node in enumerate(nodes):

        start_line = node.lineno
        end_line = getattr(
            node,
            "end_lineno",
            start_line,
        )

        content = "\n".join(
            lines[start_line - 1:end_line]
        )

        chunks.append(
            Chunk(
                content=content,
                source=document.source,
                document_type=document.document_type,
                language=document.language,
                chunk_index=index,
                start_line=start_line,
                end_line=end_line,
            )
        )

    

    if not chunks and document.content.strip():

        chunks.append(
            Chunk(
                content=document.content,
                source=document.source,
                document_type=document.document_type,
                language=document.language,
                chunk_index=0,
                start_line=1,
                end_line=len(lines),
            )
        )

    return chunks


# ---------------------------------------------------------
# C++
# ---------------------------------------------------------

def chunk_cpp_document(document: Document) -> list[Chunk]:


    source = document.content
    source_bytes = source.encode("utf-8")

    language = Language(
        tree_sitter_cpp.language()
    )

    parser = Parser(language)

    tree = parser.parse(source_bytes)

    root_node = tree.root_node

    chunks = []

    lines = source.splitlines()

    supported_node_types = {
        "function_definition",
        "class_specifier",
        "struct_specifier",
        "enum_specifier",
        "namespace_definition",
    }

    for index, node in enumerate(root_node.children):

        if node.type not in supported_node_types:
            continue

        start_line = node.start_point.row + 1
        end_line = node.end_point.row + 1

        content = "\n".join(
            lines[start_line - 1:end_line]
        )

        chunks.append(
            Chunk(
                content=content,
                source=document.source,
                document_type=document.document_type,
                language=document.language,
                chunk_index=index,
                start_line=start_line,
                end_line=end_line,
            )
        )


    if not chunks and document.content.strip():

        chunks.append(
            Chunk(
                content=document.content,
                source=document.source,
                document_type=document.document_type,
                language=document.language,
                chunk_index=0,
                start_line=1,
                end_line=len(lines),
            )
        )

    return chunks