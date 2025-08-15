from pydantic import Field
from mcp.server.fastmcp import FastMCP

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
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)

@mcp.resource(
        name="list_documents",
        description="A resource to return all doc id's",
        uri="docs://documents",
        mime_type="appplication/json"

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
    _validate_document_exists(doc_id)
    return docs[doc_id]

# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc

if __name__ == "__main__":
    mcp.run(transport="stdio")
