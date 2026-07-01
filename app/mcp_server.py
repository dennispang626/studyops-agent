"""Optional MCP server for StudyOps tool functions.

Install `mcp[cli]` before running this module directly. The plain Python tool
functions are available without the MCP dependency and are used by ADK as well.
"""

from __future__ import annotations

from app.tools.studyops_tools import (
    classify_certification_source,
    create_study_plan,
    fetch_and_clean_source,
    generate_practice_quiz,
    generate_rag_context,
    get_certification_catalog,
    get_learning_memory,
    get_retry_queue,
    ingest_certification_source,
    ingest_uploaded_file,
    list_obsidian_notes,
    record_practice_attempt,
    rebuild_chroma_index,
    run_studyops_workflow_tool,
    search_certification_sources,
    search_obsidian_notes,
    seed_studyops_source_map,
    submit_practice_answers,
    write_obsidian_note,
)

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:  # pragma: no cover - optional dependency
    FastMCP = None


def build_mcp_server():
    """Build the MCP server when the optional MCP SDK is installed."""

    if FastMCP is None:
        raise RuntimeError("Install `mcp[cli]>=1,<2` to run the MCP server.")

    server = FastMCP("studyops-agent")
    server.tool()(get_certification_catalog)
    server.tool()(search_certification_sources)
    server.tool()(classify_certification_source)
    server.tool()(fetch_and_clean_source)
    server.tool()(seed_studyops_source_map)
    server.tool()(ingest_certification_source)
    server.tool()(ingest_uploaded_file)
    server.tool()(write_obsidian_note)
    server.tool()(list_obsidian_notes)
    server.tool()(search_obsidian_notes)
    server.tool()(rebuild_chroma_index)
    server.tool()(generate_rag_context)
    server.tool()(create_study_plan)
    server.tool()(generate_practice_quiz)
    server.tool()(submit_practice_answers)
    server.tool()(run_studyops_workflow_tool)
    server.tool()(record_practice_attempt)
    server.tool()(get_learning_memory)
    server.tool()(get_retry_queue)
    return server


mcp = build_mcp_server() if FastMCP is not None else None


if __name__ == "__main__":
    if mcp is None:
        raise SystemExit("Install `mcp[cli]>=1,<2` to run the StudyOps MCP server.")
    mcp.run()
