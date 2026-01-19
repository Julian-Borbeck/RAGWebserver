import json
import os
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from filelock import FileLock

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

def log_event(event, logfile = "events.jsonl"):

    logfile = Path(logfile)
    logfile.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        **event,
    }

    line = json.dumps(record, ensure_ascii=False)

    lock = FileLock(str(logfile) + ".lock")

    with lock:
        with logfile.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
