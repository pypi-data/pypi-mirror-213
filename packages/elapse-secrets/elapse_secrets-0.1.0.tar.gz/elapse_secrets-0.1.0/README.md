# Elapse Secrets Filters

Elapse Secrets Filters is a Python package designed to help you search and mask sensitive information in a body of text using pre-defined regular expressions. This package includes filters for common secrets like AWS keys, Github tokens, API keys, and much more.

The package provides two main functions:

1. `filter_elapse_secrets(text: str) -> str` - Uses the predefined regex filters to search and mask (with asterisks) any matching sensitive information in the input text.

2. `find_error_in_regex(yaml_file: str) -> None` - Checks the YAML file containing regex rules for any incorrect patterns and logs the error if any are found.

## Getting Started

1. Clone this repository

   ```bash
   git clone https://github.com/username/elapse_secrets_filters.git
   ```

2. Navigate to the cloned repository

   ```bash
   cd elapse_secrets_filters
   ```

3. Install the required packages

   ```bash
   poetry install
   ```

## Usage

This is a basic usage example.

```python
from elapse_secrets_filters import filter_elapse_secrets

text_with_secrets = "My AWS Access Key is AKIAYOURACCESSKEYHERE"
filtered_text = filter_elapse_secrets(text_with_secrets)
print(filtered_text)
# Output: My AWS Access Key is ********
```

## Documentation

### `filter_elapse_secrets(text: str) -> str`

This function takes a string as input and returns the string with sensitive information replaced by asterisks.

#### Parameters

- `text (str)`: The text to filter.

#### Returns

- `str`: The filtered text.

### `find_error_in_regex(yaml_file: str) -> None`

This function checks a YAML file for incorrect regular expression patterns. If an error is found, it is logged.

#### Parameters

- `yaml_file (str)`: The YAML file to check.

#### Returns

- `None`

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the terms of the MIT license.

## Contact

Please feel free to contact the maintainers of this project if you have any questions.

## Acknowledgments

We would like to thank all the contributors who have been part of this project.
