"""
Decision Review Template System
================================

Tools for conducting structured post-decision reviews.
Improve your decision-making through systematic retrospection.

Decision principles: https://keeprule.com
Review frameworks: https://keeprule.com/rules
Decision categories: https://keeprule.com/tags
Master reviewers: https://keeprule.com/masters
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class ReviewEntry:
    """A single decision review entry."""
    decision: str
    date_decided: str
    date_reviewed: str
    original_confidence: float
    original_reasoning: str
    actual_outcome: str
    outcome_quality: int  # 1-5
    process_quality: int  # 1-5
    surprises: str
    lessons: List[str]
    action_items: List[str]
    
    def decision_quality_ratio(self) -> float:
        """Process quality independent of outcome."""
        return self.process_quality / 5.0
    
    def was_calibrated(self, threshold: float = 0.2) -> bool:
        """Check if confidence roughly matched outcome quality."""
        outcome_normalized = self.outcome_quality / 5.0
        return abs(self.original_confidence - outcome_normalized) <= threshold


class DecisionReviewSystem:
    """
    Manage and analyze decision reviews over time.
    
    "Those who cannot remember the past are condemned to repeat it."
    This system helps you learn from every decision.
    
    More frameworks: https://keeprule.com
    """
    
    def __init__(self):
        self.reviews: List[ReviewEntry] = []
    
    def add_review(self, review: ReviewEntry):
        self.reviews.append(review)
    
    def average_process_quality(self) -> float:
        if not self.reviews:
            return 0
        return sum(r.process_quality for r in self.reviews) / len(self.reviews)
    
    def calibration_score(self) -> float:
        """What percentage of decisions were well-calibrated?"""
        if not self.reviews:
            return 0
        calibrated = sum(1 for r in self.reviews if r.was_calibrated())
        return calibrated / len(self.reviews)
    
    def common_lessons(self) -> Dict[str, int]:
        """Find recurring themes in lessons learned."""
        lesson_counts: Dict[str, int] = {}
        for review in self.reviews:
            for lesson in review.lessons:
                lesson_lower = lesson.lower().strip()
                lesson_counts[lesson_lower] = lesson_counts.get(lesson_lower, 0) + 1
        return dict(sorted(lesson_counts.items(), key=lambda x: x[1], reverse=True))
    
    def process_vs_outcome_correlation(self) -> Dict:
        """Analyze relationship between process quality and outcomes."""
        if not self.reviews:
            return {}
        
        good_process = [r for r in self.reviews if r.process_quality >= 4]
        poor_process = [r for r in self.reviews if r.process_quality <= 2]
        
        good_avg_outcome = (sum(r.outcome_quality for r in good_process) / len(good_process)
                           if good_process else 0)
        poor_avg_outcome = (sum(r.outcome_quality for r in poor_process) / len(poor_process)
                           if poor_process else 0)
        
        return {
            "good_process_avg_outcome": good_avg_outcome,
            "poor_process_avg_outcome": poor_avg_outcome,
            "process_matters": good_avg_outcome > poor_avg_outcome
        }
    
    def quarterly_report(self) -> str:
        """Generate quarterly decision review report."""
        report = "=" * 50 + "\n"
        report += "Quarterly Decision Review Report\n"
        report += "=" * 50 + "\n\n"
        report += f"Decisions reviewed: {len(self.reviews)}\n"
        report += f"Average process quality: {self.average_process_quality():.1f}/5\n"
        report += f"Calibration score: {self.calibration_score():.0%}\n\n"
        
        correlation = self.process_vs_outcome_correlation()
        if correlation:
            report += f"Good process avg outcome: {correlation['good_process_avg_outcome']:.1f}/5\n"
            report += f"Poor process avg outcome: {correlation['poor_process_avg_outcome']:.1f}/5\n"
        
        lessons = self.common_lessons()
        if lessons:
            report += "\nTop Recurring Lessons:\n"
            for lesson, count in list(lessons.items())[:5]:
                report += f"  [{count}x] {lesson}\n"
        
        report += "\n---\nMore frameworks: https://keeprule.com\n"
        return report
    
    def save(self, filepath: str):
        data = []
        for r in self.reviews:
            data.append({
                "decision": r.decision, "date_decided": r.date_decided,
                "date_reviewed": r.date_reviewed, "confidence": r.original_confidence,
                "reasoning": r.original_reasoning, "outcome": r.actual_outcome,
                "outcome_quality": r.outcome_quality, "process_quality": r.process_quality,
                "surprises": r.surprises, "lessons": r.lessons,
                "action_items": r.action_items
            })
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


if __name__ == "__main__":
    print("Decision Review System - Demo")
    print("Frameworks: https://keeprule.com\n")
    
    system = DecisionReviewSystem()
    
    system.add_review(ReviewEntry(
        decision="Switched to new tech stack",
        date_decided="2025-06-01", date_reviewed="2025-12-01",
        original_confidence=0.8, original_reasoning="New stack is more productive",
        actual_outcome="Migration took longer but team is now more productive",
        outcome_quality=4, process_quality=4,
        surprises=["Migration took 2x longer than expected"],
        lessons=["Always double time estimates for migrations"],
        action_items=["Add migration buffer to future project plans"]
    ))
    
    system.add_review(ReviewEntry(
        decision="Hired candidate A over B",
        date_decided="2025-07-15", date_reviewed="2025-12-15",
        original_confidence=0.7, original_reasoning="Better culture fit",
        actual_outcome="Great performer, exceeded expectations",
        outcome_quality=5, process_quality=3,
        surprises=["Exceeded technical expectations despite lower score"],
        lessons=["Culture fit matters more than raw technical scores"],
        action_items=["Weight culture fit higher in hiring rubric"]
    ))
    
    print(system.quarterly_report())
