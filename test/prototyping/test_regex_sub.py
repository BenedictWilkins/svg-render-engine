# import re


# def replace_dot_in_blocks(s, replacement_char):
#     # This pattern matches text within {{...}} blocks
#     pattern = r"(\{\{[^\{\}]*?\}\})"

#     # Function to be called for each match
#     def replace_dots(match):
#         # Replace all dots in each match
#         return match.group(0).replace(".", replacement_char)

#     # Use re.sub to apply the replacement
#     return re.sub(pattern, replace_dots, s)


# def replace_dots_outermost(s, replacement_char):
#     # Pattern to match the outermost {{...}}
#     pattern = r"\{\{(.*?)\}\}"

#     def replace_dots(match):
#         # Replace dots only in the matched outermost text
#         return "{{" + match.group(1).replace(".", replacement_char) + "}}"

#     # Apply the replacement
#     return re.sub(pattern, replace_dots, s)


# # Example usage
# original_string = (
#     "This is a test. .{{.{{..This should.replace dots.}}.}}. This should not."
# )
# modified_string = replace_dot_in_blocks(original_string, "*")
# print(modified_string)


# modified_string = replace_dots_outermost(original_string, "*")
# print(modified_string)

import re


def replace_dots_outermost(s, replacement_char):
    # Pattern to match the outermost {{...}}
    # Using a non-greedy match, but ensuring that nested {{...}} are also included
    pattern = r"\{\{.*?\}\}"

    def replace_dots(match):
        # Replace dots in the entire matched segment, including nested blocks
        return match.group(0).replace(".", replacement_char)

    # Apply the replacement
    return re.sub(pattern, replace_dots, s)


# Example usage
original_string = (
    "This is a test. .{{.{{..This should.replace dots.}}.}}. This should not."
)
modified_string = replace_dots_outermost(original_string, "*")
print(modified_string)
