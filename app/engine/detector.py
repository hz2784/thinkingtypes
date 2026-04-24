import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "thinking_types.db")

TYPE_MAP = {
    (False, False, False): "architect",
    (False, False, True): "detective",
    (False, True, False): "advocate",
    (False, True, True): "explorer",
    (True, False, False): "reporter",
    (True, False, True): "collector",
    (True, True, False): "improviser",
    (True, True, True): "wanderer",
}

TYPE_LABELS = {
    "architect": "Architect",
    "detective": "Detective",
    "advocate": "Advocate",
    "explorer": "Explorer",
    "reporter": "Reporter",
    "collector": "Collector",
    "improviser": "Improviser",
    "wanderer": "Wanderer",
}

TYPE_COLORS = {
    "architect": "#1e3a5f",
    "detective": "#0d7c4a",
    "advocate": "#d94f4f",
    "explorer": "#1a8a8a",
    "reporter": "#5ba3d9",
    "collector": "#d4a017",
    "improviser": "#e87d2f",
    "wanderer": "#9b7cc4",
}

TYPE_DESCRIPTIONS = {
    "architect": "Builds carefully reasoned arguments with precision and structure.",
    "detective": "Methodically examines all angles before drawing a conclusion.",
    "advocate": "Passionate about a position and argues with creative energy.",
    "explorer": "Pursues ideas across boundaries and makes unexpected connections.",
    "reporter": "Accurately captures and organizes information — a reliable fact-finder.",
    "collector": "Gathers information from many sources with strong research instincts.",
    "improviser": "Quick, confident responses based on instinct — jumps in first.",
    "wanderer": "Touches many ideas with genuine curiosity and openness.",
}

TYPE_STRENGTHS = {
    "architect": "Rigor, clarity, persuasion",
    "detective": "Thoroughness, fairness, analytical depth",
    "advocate": "Persuasion, voice, creative argumentation",
    "explorer": "Originality, cross-domain thinking, creativity",
    "reporter": "Reliability, organization, factual accuracy",
    "collector": "Breadth, research instinct, finding information",
    "improviser": "Speed, confidence, voice, willingness to start",
    "wanderer": "Curiosity, openness, range of interests",
}

TYPE_GROWTH = {
    "architect": "Taking creative risks, flexibility",
    "detective": "Efficiency — committing to a position",
    "advocate": "Considering opposing views, acknowledging complexity",
    "explorer": "Organization, follow-through",
    "reporter": "Moving beyond reporting to analysis",
    "collector": "Synthesis — connecting what they've gathered",
    "improviser": "Slowing down to add evidence and reasoning",
    "wanderer": "Focus — picking one idea and going deep",
}

TYPE_TEACHER_TIPS = {
    "architect": "Challenge them with open-ended prompts that have no single right answer.",
    "detective": "Give them a deadline to decide — help them practice making calls with incomplete information.",
    "advocate": "Pair with Detectives for peer review — natural fit for perspective-taking practice.",
    "explorer": "Give them a structural scaffold (graphic organizer) but let them fill it their way.",
    "reporter": 'Ask them "So what?" after their summary — push them to add one sentence of analysis.',
    "collector": '"You found 5 great sources. Now pick the 2 most important and explain how they connect."',
    "improviser": '"Your idea is strong. Now find 2 pieces of evidence that prove you\'re right."',
    "wanderer": '"You have 4 interesting ideas here. Circle your favorite one, and let\'s build on that."',
}

BOUNDARY_LOW = 4.0
BOUNDARY_HIGH = 6.0


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def compute_depth_score(orf_sessions, maze_sessions, essay_signals, awe_scores):
    signals = []
    weights = []

    if maze_sessions:
        inf_accs = []
        for m in maze_sessions:
            if m["inferential_total"] > 0:
                inf_accs.append(m["inferential_correct"] / m["inferential_total"])
        if inf_accs:
            signals.append(sum(inf_accs) / len(inf_accs))
            weights.append(0.15)

    if awe_scores:
        avg_evidence = sum(a["evidence_score"] for a in awe_scores) / len(awe_scores)
        signals.append(avg_evidence / 4.0)
        weights.append(0.20)

    if essay_signals:
        reasoning_ratios = []
        for es in essay_signals:
            if es["total_sentence_count"] > 0:
                reasoning_ratios.append(es["reasoning_sentence_count"] / es["total_sentence_count"])
        if reasoning_ratios:
            signals.append(sum(reasoning_ratios) / len(reasoning_ratios))
            weights.append(0.25)

        avg_cross_ref = sum(es["cross_text_references"] for es in essay_signals) / len(essay_signals)
        signals.append(min(1.0, avg_cross_ref / 3.0))
        weights.append(0.20)

        if len(essay_signals) >= 2:
            changes = 0
            for i in range(1, len(essay_signals)):
                r1 = essay_signals[i-1]["reasoning_sentence_count"]
                r2 = essay_signals[i]["reasoning_sentence_count"]
                if r2 > r1:
                    changes += 1
            evolution = changes / (len(essay_signals) - 1)
            signals.append(evolution)
            weights.append(0.20)

    if not weights:
        return 5.0

    total_weight = sum(weights)
    score = sum(s * w for s, w in zip(signals, weights)) / total_weight
    return round(score * 10, 2)


def compute_structure_score(orf_sessions, essay_signals):
    signals = []
    weights = []

    if essay_signals and len(essay_signals) >= 2:
        para_counts = [es["topic_sentences_count"] for es in essay_signals]
        mean_p = sum(para_counts) / len(para_counts)
        variance = sum((p - mean_p) ** 2 for p in para_counts) / len(para_counts)
        consistency = 1.0 - min(1.0, variance / 4.0)
        signals.append(1.0 - consistency)
        weights.append(0.25)

    if essay_signals:
        diversities = []
        for es in essay_signals:
            if es["connective_words_total"] > 0:
                diversities.append(min(1.0, es["connective_words_unique"] / 8.0))
        if diversities:
            signals.append(sum(diversities) / len(diversities))
            weights.append(0.20)

    if essay_signals:
        revision_ratios = []
        for es in essay_signals:
            total_revisions = (es["revision_surface_edits"] +
                             es["revision_structural_edits"] +
                             es["revision_argument_edits"])
            if total_revisions > 0:
                deep_ratio = (es["revision_structural_edits"] + es["revision_argument_edits"]) / total_revisions
                revision_ratios.append(deep_ratio)
        if revision_ratios:
            signals.append(sum(revision_ratios) / len(revision_ratios))
            weights.append(0.25)

    if essay_signals:
        org_scores = []
        for es in essay_signals:
            total_paras = max(1, es["topic_sentences_count"] + 1)
            org_scores.append(es["topic_sentences_count"] / total_paras)
        avg_org = sum(org_scores) / len(org_scores)
        signals.append(1.0 - avg_org)
        weights.append(0.15)

    if orf_sessions:
        self_corr_rates = []
        for o in orf_sessions:
            if o["errors"] > 0:
                self_corr_rates.append(min(1.0, o["self_corrections"] / o["errors"]))
        pace_var = 0.5 if not self_corr_rates else sum(self_corr_rates) / len(self_corr_rates)
        signals.append(pace_var)
        weights.append(0.15)

    if not weights:
        return 5.0

    total_weight = sum(weights)
    score = sum(s * w for s, w in zip(signals, weights)) / total_weight
    return round(score * 10, 2)


def compute_evidence_score(maze_sessions, essay_signals):
    signals = []
    weights = []

    if essay_signals:
        avg_sources = sum(es["num_evidence_sources"] for es in essay_signals) / len(essay_signals)
        signals.append(min(1.0, avg_sources / 5.0))
        weights.append(0.25)

    if essay_signals:
        counter_rate = sum(es["counterargument_present"] for es in essay_signals) / len(essay_signals)
        signals.append(counter_rate)
        weights.append(0.25)

    if essay_signals and len(essay_signals) >= 2:
        sources_list = [es["num_evidence_sources"] for es in essay_signals]
        mean_s = sum(sources_list) / len(sources_list)
        variance = sum((s - mean_s) ** 2 for s in sources_list) / len(sources_list)
        consistency = 1.0 - min(1.0, variance / 4.0)
        signals.append(1.0 - consistency)
        weights.append(0.20)

    if maze_sessions:
        avg_changes = sum(m["answer_changes"] for m in maze_sessions) / len(maze_sessions)
        signals.append(min(1.0, avg_changes / 5.0))
        weights.append(0.15)

    if essay_signals:
        depth_per_ev = []
        for es in essay_signals:
            if es["num_evidence_sources"] > 0:
                ratio = es["evidence_explanation_sentences"] / es["num_evidence_sources"]
                depth_per_ev.append(min(1.0, ratio / 3.0))
        if depth_per_ev:
            avg_depth = sum(depth_per_ev) / len(depth_per_ev)
            signals.append(1.0 - avg_depth)
            weights.append(0.15)

    if not weights:
        return 5.0

    total_weight = sum(weights)
    score = sum(s * w for s, w in zip(signals, weights)) / total_weight
    return round(score * 10, 2)


def classify_type(depth, structure, evidence):
    boundaries = []
    if BOUNDARY_LOW <= depth <= BOUNDARY_HIGH:
        boundaries.append("depth")
    if BOUNDARY_LOW <= structure <= BOUNDARY_HIGH:
        boundaries.append("structure")
    if BOUNDARY_LOW <= evidence <= BOUNDARY_HIGH:
        boundaries.append("evidence")

    is_surface = depth < 5.0
    is_exploratory = structure >= 5.0
    is_divergent = evidence >= 5.0

    primary = TYPE_MAP[(is_surface, is_exploratory, is_divergent)]

    secondary = None
    if len(boundaries) == 1:
        dim = boundaries[0]
        if dim == "depth":
            alt_surface = not is_surface
            secondary = TYPE_MAP[(alt_surface, is_exploratory, is_divergent)]
        elif dim == "structure":
            alt_expl = not is_exploratory
            secondary = TYPE_MAP[(is_surface, alt_expl, is_divergent)]
        elif dim == "evidence":
            alt_div = not is_divergent
            secondary = TYPE_MAP[(is_surface, is_exploratory, alt_div)]

    dist_from_boundary = []
    for score in [depth, structure, evidence]:
        if score < BOUNDARY_LOW:
            dist_from_boundary.append(BOUNDARY_LOW - score)
        elif score > BOUNDARY_HIGH:
            dist_from_boundary.append(score - BOUNDARY_HIGH)
        else:
            dist_from_boundary.append(0)
    avg_dist = sum(dist_from_boundary) / 3
    confidence = min(1.0, avg_dist / 1.5)

    return {
        "primary_type": primary,
        "secondary_type": secondary,
        "boundary_dimensions": boundaries,
        "confidence": round(confidence, 2),
    }


def profile_student(student_id, unit_id=None):
    conn = get_db()

    if unit_id:
        orf_rows = conn.execute(
            "SELECT * FROM orf_sessions WHERE student_id=? AND unit_id=?",
            (student_id, unit_id)
        ).fetchall()
        maze_rows = conn.execute(
            "SELECT * FROM maze_sessions WHERE student_id=? AND unit_id=?",
            (student_id, unit_id)
        ).fetchall()
        essay_ids = conn.execute(
            "SELECT essay_id FROM essays WHERE student_id=? AND unit_id=?",
            (student_id, unit_id)
        ).fetchall()
    else:
        orf_rows = conn.execute(
            "SELECT * FROM orf_sessions WHERE student_id=?", (student_id,)
        ).fetchall()
        maze_rows = conn.execute(
            "SELECT * FROM maze_sessions WHERE student_id=?", (student_id,)
        ).fetchall()
        essay_ids = conn.execute(
            "SELECT essay_id FROM essays WHERE student_id=?", (student_id,)
        ).fetchall()

    eids = [e["essay_id"] for e in essay_ids]

    if not eids:
        conn.close()
        return None

    placeholders = ",".join(["?"] * len(eids))
    awe_rows = conn.execute(
        f"SELECT * FROM awe_scores WHERE essay_id IN ({placeholders})", eids
    ).fetchall()
    signal_rows = conn.execute(
        f"SELECT * FROM essay_signals WHERE essay_id IN ({placeholders})", eids
    ).fetchall()

    conn.close()

    orf_list = [dict(r) for r in orf_rows]
    maze_list = [dict(r) for r in maze_rows]
    awe_list = [dict(r) for r in awe_rows]
    signal_list = [dict(r) for r in signal_rows]

    depth = compute_depth_score(orf_list, maze_list, signal_list, awe_list)
    structure = compute_structure_score(orf_list, signal_list)
    evidence = compute_evidence_score(maze_list, signal_list)

    classification = classify_type(depth, structure, evidence)
    signal_count = len(orf_list) + len(maze_list) + len(signal_list)

    return {
        "student_id": student_id,
        "unit_id": unit_id,
        "depth_score": depth,
        "structure_score": structure,
        "evidence_score": evidence,
        "signal_count": signal_count,
        **classification,
    }


def profile_all_students(unit_id=None):
    conn = get_db()
    students = conn.execute("SELECT * FROM students ORDER BY last_name").fetchall()
    conn.close()

    profiles = []
    for s in students:
        p = profile_student(s["student_id"], unit_id)
        if p:
            p["first_name"] = s["first_name"]
            p["last_name"] = s["last_name"]
            profiles.append(p)
    return profiles


def get_type_distribution(unit_id=None):
    profiles = profile_all_students(unit_id)
    dist = {}
    for p in profiles:
        t = p["primary_type"]
        if t not in dist:
            dist[t] = []
        dist[t].append(f"{p['first_name']} {p['last_name']}")
    return dist


def get_drift_alerts(school_year="2025-2026"):
    conn = get_db()
    students = conn.execute("SELECT * FROM students ORDER BY last_name").fetchall()
    units = conn.execute("SELECT unit_id FROM units ORDER BY sequence").fetchall()
    conn.close()

    unit_ids = [u["unit_id"] for u in units]
    alerts = []

    for s in students:
        type_sequence = []
        for uid in unit_ids:
            p = profile_student(s["student_id"], uid)
            if p:
                type_sequence.append({
                    "unit_id": uid,
                    "type": p["primary_type"],
                    "depth": p["depth_score"],
                    "structure": p["structure_score"],
                    "evidence": p["evidence_score"],
                })

        if len(type_sequence) < 2:
            continue

        types = [t["type"] for t in type_sequence]
        alert = {
            "student_id": s["student_id"],
            "first_name": s["first_name"],
            "last_name": s["last_name"],
            "type_sequence": type_sequence,
            "alert_type": None,
            "message": None,
        }

        depth_first = type_sequence[0]["depth"]
        depth_last = type_sequence[-1]["depth"]
        depth_grew = depth_last - depth_first >= 2.5

        type_changes = sum(
            1 for i in range(1, len(type_sequence))
            if type_sequence[i]["type"] != type_sequence[i-1]["type"]
        )

        if type_sequence[-2]["depth"] >= 5.0 and type_sequence[-1]["depth"] < 5.0:
            alert["alert_type"] = "warning"
            alert["message"] = (
                f"Shifted from {TYPE_LABELS[types[-2]]} to {TYPE_LABELS[types[-1]]} — "
                f"depth decreased significantly. May need support engaging analytically."
            )
            alerts.append(alert)
        elif len(set(types)) == 1 and len(types) >= 3:
            alert["alert_type"] = "stable"
            alert["message"] = (
                f"Stable as {TYPE_LABELS[types[0]]} for {len(types)} units. "
                f"Consider a stretch activity to expand range."
            )
            alerts.append(alert)
        elif type_changes >= 1 and depth_grew:
            alert["alert_type"] = "positive"
            alert["message"] = (
                f"Growing deeper — moved from {TYPE_LABELS[types[0]]} to {TYPE_LABELS[types[-1]]} "
                f"with depth increasing from {depth_first:.1f} to {depth_last:.1f}."
            )
            alerts.append(alert)
        elif type_changes >= 2 and len(set(types)) >= 3:
            alert["alert_type"] = "positive"
            alert["message"] = (
                f"Showing range — moved through {len(set(types))} different types. "
                f"Developing flexibility across thinking styles."
            )
            alerts.append(alert)
        elif type_changes >= 1 and types[0] != types[-1]:
            alert["alert_type"] = "positive"
            alert["message"] = (
                f"Shifted from {TYPE_LABELS[types[0]]} to {TYPE_LABELS[types[-1]]} — "
                f"developing new thinking patterns."
            )
            alerts.append(alert)

    alerts.sort(key=lambda a: {"warning": 0, "stable": 1, "positive": 2}.get(a["alert_type"], 3))
    return alerts


def get_grouping_suggestions(unit_id=None):
    profiles = profile_all_students(unit_id)

    OPPOSITES = {
        "architect": "wanderer", "wanderer": "architect",
        "detective": "improviser", "improviser": "detective",
        "advocate": "collector", "collector": "advocate",
        "explorer": "reporter", "reporter": "explorer",
    }

    by_type = {}
    for p in profiles:
        t = p["primary_type"]
        if t not in by_type:
            by_type[t] = []
        by_type[t].append(p)

    pairs = []
    used = set()

    for p in profiles:
        if p["student_id"] in used:
            continue
        opposite_type = OPPOSITES.get(p["primary_type"])
        if opposite_type and opposite_type in by_type:
            partner = None
            for candidate in by_type[opposite_type]:
                if candidate["student_id"] not in used:
                    partner = candidate
                    break
            if partner:
                used.add(p["student_id"])
                used.add(partner["student_id"])
                pairs.append({
                    "student_a": {
                        "id": p["student_id"],
                        "name": f"{p['first_name']} {p['last_name']}",
                        "type": p["primary_type"],
                    },
                    "student_b": {
                        "id": partner["student_id"],
                        "name": f"{partner['first_name']} {partner['last_name']}",
                        "type": partner["primary_type"],
                    },
                    "pairing_reason": _pairing_reason(p["primary_type"], partner["primary_type"]),
                })

    unpaired = [p for p in profiles if p["student_id"] not in used]
    for i in range(0, len(unpaired) - 1, 2):
        a, b = unpaired[i], unpaired[i+1]
        pairs.append({
            "student_a": {
                "id": a["student_id"],
                "name": f"{a['first_name']} {a['last_name']}",
                "type": a["primary_type"],
            },
            "student_b": {
                "id": b["student_id"],
                "name": f"{b['first_name']} {b['last_name']}",
                "type": b["primary_type"],
            },
            "pairing_reason": _pairing_reason(a["primary_type"], b["primary_type"]),
        })

    return pairs


def _pairing_reason(type_a, type_b):
    reasons = {
        ("architect", "wanderer"): "James brings structure and focus; partner brings creative breadth.",
        ("wanderer", "architect"): "Wanderer brings creative breadth; Architect brings structure and focus.",
        ("detective", "improviser"): "Detective brings thorough analysis; Improviser brings quick instincts and energy.",
        ("improviser", "detective"): "Improviser brings quick instincts; Detective brings thorough analysis.",
        ("advocate", "collector"): "Advocate brings deep conviction; Collector brings broad evidence base.",
        ("collector", "advocate"): "Collector brings broad evidence; Advocate brings focused argumentation.",
        ("explorer", "reporter"): "Explorer brings creative connections; Reporter brings factual precision.",
        ("reporter", "explorer"): "Reporter brings factual precision; Explorer brings creative connections.",
    }
    key = (type_a, type_b)
    if key in reasons:
        return reasons[key]
    return f"{TYPE_LABELS.get(type_a, type_a)} and {TYPE_LABELS.get(type_b, type_b)} bring complementary perspectives."


if __name__ == "__main__":
    print("=== All Students (Overall) ===")
    profiles = profile_all_students()
    for p in profiles:
        sec = f" / {TYPE_LABELS[p['secondary_type']]}" if p.get("secondary_type") else ""
        print(f"  {p['first_name']:8s} {p['last_name']:10s} → {TYPE_LABELS[p['primary_type']]:12s}{sec}  "
              f"(D:{p['depth_score']:.1f}  S:{p['structure_score']:.1f}  E:{p['evidence_score']:.1f}  "
              f"conf:{p['confidence']:.2f})")

    print("\n=== Type Distribution ===")
    dist = get_type_distribution()
    for t, names in sorted(dist.items()):
        print(f"  {TYPE_LABELS[t]:12s} ({len(names)}): {', '.join(names)}")
