from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


def _validate_document_exists(doc_id: str) -> None:
    """Validate that a document ID exists in the docs dictionary.
    
    Args:
        doc_id: The document ID to validate
        
    Raises:
        ValueError: If the document ID is not found
    """
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

@mcp.tool(
    name="read_document",
    description="Read the contents of a document and return it as a string."
)
def read_document(
    doc_id: str = Field(description="Id of the document to read")
):
    _validate_document_exists(doc_id)
    return docs[doc_id]

@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the documents content with a new string."
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace."),
    new_str: str = Field(description="The new text to insert in place of the old text.")
):
    _validate_document_exists(doc_id)
    if docs[doc_id].find(old_str) < 0:
        raise ValueError(f"The string \"{old_str}\" is not found in the {doc_id} document")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)

@mcp.resource(
        name="list_documents",
        description="A resource to return all doc id's",
        uri="docs://documents",
        mime_type="application/json"

)
def list_documents() -> list[str]:
    return list(docs.keys())

@mcp.resource(
        name="fetch_document",
        description="A resource to return the contents of a particular doc",
        uri="docs://documents/{doc_id}",
        mime_type="text/plain"

)
def fetch_document(doc_id: str) -> str:
    return read_document(doc_id)

# TODO: Write a prompt to rewrite a doc in markdown format
@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in Markdown format."
)
def format(
    doc_id: str=Field(description="Id of the document to format")
)-> list[base.Message]:
    prompt = f"""
Your goal is to reformat a document to be written with markdown syntax.

The id of the document you need to reformat is:
<document_id>
{doc_id}
</document_id>

Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
Use the 'edit_document' tool to edit the document. After the document has been reformatted...
"""
    return[base.UserMessage(prompt)]

# TODO: Write a prompt to summarize a doc

if __name__ == "__main__":
    mcp.run(transport="stdio")
