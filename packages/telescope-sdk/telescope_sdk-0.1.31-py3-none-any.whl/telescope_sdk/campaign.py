from enum import Enum
from typing import List, Optional
from telescope_sdk.common import UserFacingDataType
from pydantic import BaseModel
from telescope_sdk.company import CompanySizeRange


class CampaignStatus(str, Enum):
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    ERROR = 'ERROR'


class ExampleCompany(BaseModel):
    id: str
    name: str


class IdealCustomerProfile(BaseModel):
    example_companies: List[ExampleCompany]
    job_titles: List[str]
    keywords: List[str] = None
    negative_keywords: List[str] = None
    country_codes: List[List[str]] = None
    employee_country_codes: List[List[str]] = None
    industries: List[str] = None
    company_size_range: CompanySizeRange = None
    company_types: List[str] = None


class Campaign(UserFacingDataType):
    name: str
    status: CampaignStatus
    sequence_id: Optional[str] = None
    outreach_enabled: Optional[bool] = None
    replenish: bool
    icp: IdealCustomerProfile
