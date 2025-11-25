import json
import re

def parse_publications(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    data = {
        "journal": [],
        "proceedings": [],
        "internationalconf": [],
        "nationalconf": [],
        "lecture": [],
        "patent": [],
        "media": []
    }

    section_map = {
        "学術論文（全文査読付ジャーナル誌）": "journal",
        "学術論文（全文査読付Proceedings）": "proceedings",
        "国際会議口頭発表": "internationalconf",
        "国内口頭発表": "nationalconf",
        "講演・総説・解説・資料等": "lecture",
        "特許": "patent",
        "メディア報道": "media"
    }

    current_section = None
    current_entry = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if line is a section header
        if line in section_map:
            # Save previous entry if exists
            if current_section and current_entry:
                data[current_section].append(current_entry)
                current_entry = ""
            current_section = section_map[line]
            continue

        if current_section:
            # Check if line starts with a number (e.g., "1.", "10.")
            match = re.match(r'^\d+\.\s*(.*)', line)
            if match:
                # Save previous entry if exists
                if current_entry:
                    data[current_section].append(current_entry)
                
                # Start new entry
                content = match.group(1)
                # Remove presenter marker '〇'
                content = content.replace('〇', '')
                current_entry = content
            else:
                # Continuation of previous entry
                if current_entry:
                    current_entry += " " + line

    # Append the last entry
    if current_section and current_entry:
        data[current_section].append(current_entry)

    return data

def update_json(data, json_path):
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    txt_path = "publication_20251125.txt"
    json_path = "publications.json"
    
    print(f"Reading from {txt_path}...")
    parsed_data = parse_publications(txt_path)
    
    print(f"Writing to {json_path}...")
    update_json(parsed_data, json_path)
    print("Done.")
