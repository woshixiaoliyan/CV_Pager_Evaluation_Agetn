from __future__ import annotations

import json

from ..llm import ChatJSON
from ..models import Comparison, DimensionScore, Summary

SYSTEM_PROMPT = (
    "You are an expert reviewer of computer vision papers. Score each dimension 0-5 "
    "using the provided rubric and the evidence. Return JSON: "
    '{"dimension_scores": [{"cluster_id", "score", "confidence", "evidence": [str]}]}. '
    "Never invent evidence; only reuse provided comparisons and qualitative evidence."
)


def score_dimensions(chat: ChatJSON, comparisons: list[Comparison], qualitative: dict, kb: dict) -> list[DimensionScore]:
    dims = [d for d in kb.get("dimensions", []) if d.get("status") == "evaluated"]
    user = json.dumps(
        {
            "comparisons": [c.model_dump() for c in comparisons],
            "qualitative": qualitative,
            "dimensions": dims,
        },
        ensure_ascii=False,
    )
    payload = chat.chat_json(SYSTEM_PROMPT, user)
    raw_scores = payload.get("dimension_scores", [])
    by_id = {d["cluster_id"]: d for d in dims}
    scores: list[DimensionScore] = []
    for raw in raw_scores:
        cid = raw.get("cluster_id")
        if cid not in by_id:
            continue
        scores.append(
            DimensionScore(
                cluster_id=cid,
                dimension=by_id[cid]["name"],
                score=float(raw.get("score", 0)),
                confidence=raw.get("confidence", "medium"),
                evidence=[str(e) for e in raw.get("evidence", [])],
            )
        )
    return scores


def build_summary(scores: list[DimensionScore], weights: dict[str, float] | None = None) -> Summary:
    evaluated = [s for s in scores if s.score is not None]
    if not evaluated:
        return Summary(conclusion="no evaluable dimensions")
    if weights:
        total = sum(weights.get(s.cluster_id, 1.0) for s in evaluated)
        weighted = sum(s.score * weights.get(s.cluster_id, 1.0) for s in evaluated) / total
    else:
        weighted = sum(s.score for s in evaluated) / len(evaluated)
        weights = {s.cluster_id: 1.0 for s in evaluated}
    ranked = sorted(evaluated, key=lambda s: s.score, reverse=True)
    strengths = [f"{s.dimension} ({s.score})" for s in ranked[:3] if s.score >= 3]
    weaknesses = [f"{s.dimension} ({s.score})" for s in ranked[-3:] if s.score < 3]
    conclusion = (
        f"整体评分 {weighted:.2f}/5；主要优势：{('、'.join(strengths)) if strengths else '无明显优势'}；"
        f"主要不足：{('、'.join(weaknesses)) if weaknesses else '无明显不足'}。"
    )
    return Summary(weighted_score=round(weighted, 2), weights=weights, strengths=strengths, weaknesses=weaknesses, conclusion=conclusion)
