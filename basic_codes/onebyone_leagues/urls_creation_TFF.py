def generate_urls_from_file(input_file, output_file, range_start, range_end):
    generated_urls = []

    # Read base URLs from the input file
    with open(input_file, "r", encoding="utf-8-sig") as file:
        base_urls = file.readlines()

    # Generate URLs
    for url in base_urls:
        url = url.strip()  # Remove any trailing whitespace or newline
        for i in range(range_start, range_end + 1):
            generated_urls.append(url.replace("{i}", str(i)))

    # Write generated URLs to the output file
    with open(output_file, "w", encoding="utf-8") as file:
        for url in generated_urls:
            file.write(url + "\n")

    print(f"Generated URLs have been saved to {output_file}")


# Generate URLs for "SÜPER LIG"
generate_urls_from_file(
    input_file="../basic_codes/URLS/urls_TRENDYOL_SÜPER_LIG.txt",
    output_file="generated_urls_TRENDYOL_SÜPER_LIG.txt",
    range_start=1,
    range_end=34
)

# Generate URLs for "1. LIG"
generate_urls_from_file(
    input_file="../basic_codes/URLS/urls_TRENDYOL_1._LIG.txt",
    output_file="generated_urls_TRENDYOL_1._LIG.txt",
    range_start=1,
    range_end=34
)
