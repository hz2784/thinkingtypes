from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os

from engine.detector import (
    profile_student, profile_all_students, get_type_distribution,
    get_drift_alerts, get_grouping_suggestions,
    TYPE_LABELS, TYPE_COLORS, TYPE_DESCRIPTIONS, TYPE_STRENGTHS, TYPE_GROWTH,
    TYPE_TEACHER_TIPS,
)
from database import get_db

app = FastAPI(title="Thinking Types Dashboard")

BASE_DIR = os.path.dirname(__file__)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/api/class-overview")
async def class_overview(unit_id: str = None):
    profiles = profile_all_students(unit_id)
    distribution = {}
    for p in profiles:
        t = p["primary_type"]
        if t not in distribution:
            distribution[t] = {
                "type": t,
                "label": TYPE_LABELS[t],
                "color": TYPE_COLORS[t],
                "students": [],
            }
        distribution[t]["students"].append({
            "id": p["student_id"],
            "name": f"{p['first_name']} {p['last_name']}",
            "depth": p["depth_score"],
            "structure": p["structure_score"],
            "evidence": p["evidence_score"],
            "confidence": p["confidence"],
            "secondary_type": TYPE_LABELS.get(p.get("secondary_type")),
        })

    return {
        "total_students": len(profiles),
        "distribution": distribution,
        "type_meta": {
            t: {
                "label": TYPE_LABELS[t],
                "color": TYPE_COLORS[t],
                "description": TYPE_DESCRIPTIONS[t],
                "strengths": TYPE_STRENGTHS[t],
                "growth": TYPE_GROWTH[t],
                "teacher_tip": TYPE_TEACHER_TIPS[t],
            }
            for t in TYPE_LABELS
        },
    }


@app.get("/api/student/{student_id}")
async def student_profile(student_id: str):
    conn = get_db()
    student = conn.execute(
        "SELECT * FROM students WHERE student_id=?", (student_id,)
    ).fetchone()
    if not student:
        return JSONResponse(status_code=404, content={"error": "Student not found"})

    units = conn.execute("SELECT unit_id FROM units ORDER BY sequence").fetchall()
    conn.close()

    unit_ids = [u["unit_id"] for u in units]

    overall = profile_student(student_id)
    per_unit = []
    for uid in unit_ids:
        p = profile_student(student_id, uid)
        if p:
            p["unit_id"] = uid
            per_unit.append(p)

    t = overall["primary_type"] if overall else None

    return {
        "student_id": student_id,
        "first_name": student["first_name"],
        "last_name": student["last_name"],
        "overall": overall,
        "per_unit": per_unit,
        "type_info": {
            "label": TYPE_LABELS.get(t, ""),
            "color": TYPE_COLORS.get(t, "#666"),
            "description": TYPE_DESCRIPTIONS.get(t, ""),
            "strengths": TYPE_STRENGTHS.get(t, ""),
            "growth": TYPE_GROWTH.get(t, ""),
        } if t else None,
    }


@app.get("/api/grouping")
async def grouping(unit_id: str = None):
    pairs = get_grouping_suggestions(unit_id)
    for pair in pairs:
        pair["student_a"]["label"] = TYPE_LABELS.get(pair["student_a"]["type"], "")
        pair["student_a"]["color"] = TYPE_COLORS.get(pair["student_a"]["type"], "#666")
        pair["student_b"]["label"] = TYPE_LABELS.get(pair["student_b"]["type"], "")
        pair["student_b"]["color"] = TYPE_COLORS.get(pair["student_b"]["type"], "#666")
    return {"pairs": pairs}


@app.get("/api/alerts")
async def alerts():
    drift_alerts = get_drift_alerts()
    for alert in drift_alerts:
        for ts in alert["type_sequence"]:
            ts["label"] = TYPE_LABELS.get(ts["type"], "")
            ts["color"] = TYPE_COLORS.get(ts["type"], "#666")
    return {"alerts": drift_alerts}


@app.get("/api/students")
async def all_students():
    conn = get_db()
    students = conn.execute("SELECT * FROM students ORDER BY last_name").fetchall()
    units = conn.execute("SELECT unit_id FROM units ORDER BY sequence").fetchall()
    conn.close()

    unit_ids = [u["unit_id"] for u in units]
    result = []

    for s in students:
        overall = profile_student(s["student_id"])
        if not overall:
            continue

        per_unit = []
        for uid in unit_ids:
            p = profile_student(s["student_id"], uid)
            if p:
                per_unit.append({
                    "unit_id": uid,
                    "type": p["primary_type"],
                    "label": TYPE_LABELS.get(p["primary_type"], ""),
                    "color": TYPE_COLORS.get(p["primary_type"], "#666"),
                })

        t = overall["primary_type"]
        result.append({
            "student_id": s["student_id"],
            "first_name": s["first_name"],
            "last_name": s["last_name"],
            "type": t,
            "label": TYPE_LABELS.get(t, ""),
            "color": TYPE_COLORS.get(t, "#666"),
            "depth": overall["depth_score"],
            "structure": overall["structure_score"],
            "evidence": overall["evidence_score"],
            "confidence": overall["confidence"],
            "secondary_type": TYPE_LABELS.get(overall.get("secondary_type")),
            "per_unit": per_unit,
        })

    return {"students": result}


@app.get("/api/units")
async def list_units():
    conn = get_db()
    units = conn.execute("SELECT * FROM units ORDER BY sequence").fetchall()
    conn.close()
    return {"units": [dict(u) for u in units]}
