from dataclasses import dataclass, field


@dataclass
class Business:

    name: str
    website: str

    category: str = ""
    emails: list[str] = field(default_factory=list)
    phone_numbers: list[str] = field(default_factory=list)
    nepal_phone_numbers: list[str] = field(default_factory=list)

    address: str = ""
    city: str = ""
    district: str = ""

    source_url: str = ""
    contact_page_urls: list[str] = field(default_factory=list)

    extraction_status: str = "pending"