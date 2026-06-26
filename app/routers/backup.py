import json
import io
from datetime import datetime, date
from decimal import Decimal
from typing import Any
from enum import Enum

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User

router = APIRouter(tags=["backup"])

# ── Custom JSON encoder ───────────────────────────────────────────

class BackupEncoder(json.JSONEncoder):
    """Handles every type that standard json.dumps can't serialize."""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, bytes):
            return obj.decode("utf-8", errors="replace")
        # Last resort — converts uuid, custom types, etc. to string
        try:
            return str(obj)
        except Exception:
            return None


def _dump_all_tables(db: Session) -> dict[str, list[dict]]:
    """Query every table and return {table_name: [row_dicts]}."""
    inspector = inspect(db.bind)
    table_names = inspector.get_table_names()

    data: dict[str, list[dict]] = {}
    for table in table_names:
        rows = db.execute(text(f'SELECT * FROM "{table}"')).mappings().all()
        # Keep raw values — BackupEncoder handles serialization
        data[table] = [dict(row) for row in rows]
    return data


# ── JSON endpoint ─────────────────────────────────────────────────

@router.get(
    "/json",
    summary="Download full database backup as JSON",
    response_class=StreamingResponse,
)
def backup_json(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = _dump_all_tables(db)
    payload = {
        "exported_at": datetime.utcnow().isoformat(),
        "tables": data,
    }
    content = json.dumps(payload, indent=2, ensure_ascii=False, cls=BackupEncoder)
    filename = f"kkabbas_backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"

    return StreamingResponse(
        io.BytesIO(content.encode("utf-8")),
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ── SQL endpoint ──────────────────────────────────────────────────

def _to_sql_value(val: Any) -> str:
    """Format a Python value as a SQL literal."""
    if val is None:
        return "NULL"
    if isinstance(val, bool):
        return "TRUE" if val else "FALSE"
    if isinstance(val, Enum):
        val = val.value
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, Decimal):
        return str(val)
    if isinstance(val, (datetime, date)):
        return f"'{val.isoformat()}'"
    if isinstance(val, bytes):
        escaped = val.decode("utf-8", errors="replace").replace("'", "''")
        return f"'{escaped}'"
    # String and everything else — escape single quotes
    escaped = str(val).replace("'", "''")
    return f"'{escaped}'"


@router.get(
    "/sql",
    summary="Download full database backup as SQL INSERT statements",
    response_class=StreamingResponse,
)
def backup_sql(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = _dump_all_tables(db)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    lines: list[str] = [
        f"-- KKA Portal database backup",
        f"-- Exported at: {datetime.utcnow().isoformat()}",
        f"-- Tables: {len(data)}",
        "",
    ]

    for table, rows in data.items():
        lines.append(f"-- ── {table} ({len(rows)} rows) ──")
        if not rows:
            lines.append("")
            continue
        columns = list(rows[0].keys())
        cols_str = ", ".join(f'"{c}"' for c in columns)
        for row in rows:
            vals_str = ", ".join(_to_sql_value(row[c]) for c in columns)
            lines.append(
                f'INSERT INTO "{table}" ({cols_str}) VALUES ({vals_str});'
            )
        lines.append("")

    content = "\n".join(lines)
    filename = f"kkabbas_backup_{ts}.sql"

    return StreamingResponse(
        io.BytesIO(content.encode("utf-8")),
        media_type="text/plain",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )