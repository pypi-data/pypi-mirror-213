import re
import yaml

def find_error_in_regex(yaml_file):
    with open(yaml_file, 'r') as f:
        rules = yaml.safe_load(f)

    for r in rules:
        try:
            pattern = re.compile(r)
        except re.error as e:
            print(f"Error in regular expression: {r}")
            print(f"Error message: {str(e)}")

find_error_in_regex('elapse_secrets/db/rules-elapse-stable.yml')
