def format_context(chunks, metadata):

    lines = []
    for i, chunk in enumerate(chunks):
        md = metadata[i] if i < len(metadata) else {}
        info = (
            f"doc={md.get('source_document','?')}, "
            f"section={md.get('source_section','?')}, "
            f"section_idx={md.get('section_idx','?')}, "
            f"chunk_idx={md.get('chunk_idx','?')}"
        )
        lines.append(f"[{i}] ({info})\n{chunk}".strip())
    return "\n---\n".join(lines)

def validate_response_schema(obj):

    message = obj.get("message", "")
    command = obj.get("command", "")

    if not isinstance(message, str):
        message = str(message)

    if not isinstance(command, str):
        command = str(command)
        
    return {"message": message, "command": command}