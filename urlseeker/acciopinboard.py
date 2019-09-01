    with open ("reddit.json", mode='w', encoding='utf-8' ) as jf:
        json.dump(stories_json, jf, ensure_ascii=False, indent=4)
