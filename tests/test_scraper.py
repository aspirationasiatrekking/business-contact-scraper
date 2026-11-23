from scraper.website import scrape_website

result = scrape_website("https://nepalguidetrekking.com/")  

if result:
    print("Name:", result.name)
    print("Website:", result.website)
    print("Emails:", result.emails)
    print("Phone Numbers:", result.phone_numbers)
    print("Address:", result.address)
    print("City:", result.city)
    print("State/Province:", result.state_province)
    print("Country:", result.country)
    print("Address source:", result.address_source)
    print("City source:", result.city_source)
    print("Country source:", result.country_source)