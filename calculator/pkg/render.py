import json


def format_json_output(expression: str, result: float, indent: int = 2) -> str:
    # convert whole-number floats to int so JSON shows 5 instead of 5.0
    if isinstance(result, float) and result.is_integer():
        result_to_dump = int(result)
    else:
        result_to_dump = result

    output_data = {
        "expression": expression,
        "result": result_to_dump,
    }
    return json.dumps(output_data, indent=indent)
