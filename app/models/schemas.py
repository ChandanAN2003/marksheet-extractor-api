from typing import List, Optional
from pydantic import BaseModel, Field

class FieldWithConfidence(BaseModel):
    value: Optional[str] = None
    confidence: float = Field(..., ge=0, le=1)

class CandidateDetails(BaseModel):
    name: Optional[FieldWithConfidence] = None
    fathers_name: Optional[FieldWithConfidence] = None
    roll_no: Optional[FieldWithConfidence] = None
    registration_no: Optional[FieldWithConfidence] = None
    dob: Optional[FieldWithConfidence] = None
    exam_year: Optional[FieldWithConfidence] = None
    board_university: Optional[FieldWithConfidence] = None
    institution: Optional[FieldWithConfidence] = None

class SubjectMarks(BaseModel):
    subject: Optional[FieldWithConfidence] = None
    max_marks: Optional[FieldWithConfidence] = None
    obtained_marks: Optional[FieldWithConfidence] = None
    grade: Optional[FieldWithConfidence] = None

class MarksheetResult(BaseModel):
    candidate_details: CandidateDetails
    subject_marks: List[SubjectMarks]
    overall_result: Optional[FieldWithConfidence] = None
    issue_date: Optional[FieldWithConfidence] = None
    issue_place: Optional[FieldWithConfidence] = None