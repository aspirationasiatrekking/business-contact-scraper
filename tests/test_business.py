from models.business import Business
from dataclasses import asdict


business = Business(
    name = "Nepal Hiking Team",
    website = "https://www.nepalhikingteam.com",
    category = "Trekking company",
    emails = ["abc@gmail.com","def@gmail.com"],

)

print(business.name)
print(business.website)
print(business.category)
print(business.emails)
business_data = asdict(business)

print("\nConverted dictionary:")
print(business_data)