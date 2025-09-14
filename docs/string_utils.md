
### docs/string_utils.md
```markdown
# String Utilities

Functions for common string operations.

## Functions

### `title_case_with_exceptions(text, exceptions=None)`

Convert text to title case with exceptions for specific words.

**Parameters:**
- `text` (str): The text to convert to title case.
- `exceptions` (list): List of words to keep in lowercase.

**Returns:**
- str: Text in title case with exceptions applied.

**Example:**
```python
from priyam.string_utils import title_case_with_exceptions

result = title_case_with_exceptions("the lord of the rings", ["the", "of"])
print(result)  # "The Lord of the Rings"

---

`reverse_words(text)`
Reverse the order of words in a string.

Parameters:
text (str): The text to reverse.

Returns:
str: Text with words reversed.

Example:
`from priyam.string_utils import reverse_words

result = reverse_words("Hello World")
print(result)  # "World Hello"`

`slugify(text, separator="-")`
Convert text to a slug for use in URLs.

Parameters:
text (str): The text to convert to a slug.
separator (str): The separator to use between words.

Returns:
str: A slugified version of the text.

Example:
`from priyam.string_utils import slugify

result = slugify("Hello World!")
print(result)  # "hello-world"`