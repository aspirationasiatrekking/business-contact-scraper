from ddgs import DDGS

with DDGS(timeout=30) as ddgs:
    results = ddgs.text(
        "clinics in Bhaktapur Nepal",
        max_results=10,
        region="us-en",
        backend="mojeek"
    )

    print(f"Found {len(results)} results")

    for result in results:
        print(result["title"])
        print(result["href"])
        print()