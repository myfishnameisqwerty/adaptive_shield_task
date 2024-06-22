import json
from typing import Any, DefaultDict, List, Dict

from animal import Animal


def ger_html_template(json_data: Dict[str, Any]) -> str:
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Adaptive shield task</title>
</head>
<body>
    <h1>Output</h1>
    <pre>{json_data}</pre>
</body>
</html>
"""


def create_html(data: DefaultDict[str, List[Animal]], output_file_path: str):
    regular_dict = {k: [animal.__dict__() for animal in v] for k, v in data.items()}
    json_data = json.dumps(regular_dict, indent=4)
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(ger_html_template(json_data))

