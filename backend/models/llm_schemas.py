from datetime import date
from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


# Define Pydantic models for structured data
class Party(BaseModel):
    name: str
    role: str


class DateEntry(BaseModel):
    # Using Literal to restrict the type to specific choices
    type: Literal["notice_date", "response_deadline"]
    # Pydantic will automatically validate strings like "2024-12-31" into date objects
    value: date


class ActionItem(BaseModel):
    priority: Literal["high", "medium", "low"]
    action: str = Field(description="What to do next")
    why: str = Field(description="Reason for the action")
    timeline: str = Field(description="When to do it")


class DocumentAnalysis(BaseModel):
    document_type: str = Field(
        description="Type of document (e.g., FIR, Notice, Contract, etc.)"
    )
    parties: List[Party]
    dates: List[DateEntry]
    sections: List[str] = Field(
        description="Extract explicit legal sections/laws from Document, or apply from Relevant Laws"
    )
    clauses: List[str] = Field(
        description="Extract key clauses/obligations from Document"
    )
    summary: str = Field(
        description="A clear 2-3 sentence explanation of the document."
    )
    risk_level: Literal["Low", "Medium", "High"]
    urgency: Literal["Immediate", "Soon", "Normal"]
    consequences: List[str] = Field(description="List of potential outcomes")
    recommended_timeline: str = Field(description="e.g., Respond within X days")
    actions: List[ActionItem]


class SeverityLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class ClauseMatchStatus(str, Enum):
    unchanged = "unchanged"
    modified = "modified"
    added = "added"
    removed = "removed"


class MatchedClause(BaseModel):
    clause_text_a: str = Field(description="Clause text from document A (empty if added)")
    clause_text_b: str = Field(description="Clause text from document B (empty if removed)")
    clause_title: str = Field(description="Title or section number of the clause")
    status: ClauseMatchStatus = Field(description="Whether this clause was added, removed, modified, or unchanged")
    significance: SeverityLevel = Field(description="How significant this change is")


class ClauseComparisonResult(BaseModel):
    total_clauses_a: int = Field(description="Total clauses extracted from document A")
    total_clauses_b: int = Field(description="Total clauses extracted from document B")
    matched_clauses: List[MatchedClause] = Field(description="List of matched clauses with their status")
    added_count: int = Field(description="Number of clauses added")
    removed_count: int = Field(description="Number of clauses removed")
    modified_count: int = Field(description="Number of clauses modified")
    unchanged_count: int = Field(description="Number of clauses unchanged")


class ClauseComparisonResponse(BaseModel):
    comparison: ClauseComparisonResult
    summary: str = Field(description="AI-generated summary of key differences")
