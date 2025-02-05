import json
from types import SimpleNamespace


class Temp:
    def get_sections():
        temp_json = """
            {
                "sections": [
                    {
                        "content": "## Examination of the String Data Type\n\n**Strings are a fundamental data type in programming, used to represent textual information in various applications.** In computer memory, strings are typically represented as arrays of characters, often with an accompanying length field to optimize access and modification. For instance, in Python (version 3.x), strings are immutable, stored in a contiguous block of memory, necessitating the creation of new objects for modifications.\n\nThe implementation and utility of strings vary across programming languages:\n\n| Language    | String Characteristics                                       | Example Use Case                                      |\n|-------------|-------------------------------------------------------------|------------------------------------------------------|\n| Python      | Immutable, supports Unicode                                 | Natural Language Processing (NLP) for sentiment analysis |\n| Java        | Immutable, UTF-16 encoding                                  | Mobile applications requiring internationalization    |\n| C++        | Mutable, requires manual memory management                  | Performance-intensive applications affecting string handling |\n\nStrings facilitate numerous real-world applications including text processing, user input validation, and data serialization. In NLP, for instance, regular expressions (regex) are leveraged for tokenization and named entity recognition, as highlighted in regex implementations in Python (source: Mastering Regular Expressions in NLP). Proper string manipulation is essential for functionalities such as form validation and localization in web applications (source: Real-World Applications of Strings). \n\n### Sources\n- Mastering Regular Expressions in Natural Language Processing (NLP) with Python: https://medium.com/@charmilagiri6/mastering-regular-expressions-in-natural-language-processing-nlp-with-python-2bbbfbac33e9\n- Real-World Applications of Strings: https://blog.heycoach.in/real-world-applications-of-strings/",
                        "description": "An examination of the concept of string as a data type, including its definition, how it is represented in memory, and the differences in implementation across various programming languages.",
                        "name": "Overview of String Data Type",
                        "research": True
                    },
                    {
                        "content": "## Fundamental String Operations\n\n**Strings are pivotal in application development, serving as the backbone for text processing and user interaction.** Common operations include concatenation, splitting, and substring extraction, each supported by built-in functions across programming languages.\n\nFor instance, Python offers:\n\n- `str.join()`: Concatenates elements of an iterable with a specified separator.\n- `str.split()`: Divides a string into a list based on a delimiter.\n- `str.substr()`: Extracts a substring from a string, given start and end indices.\n\nIn R, similar functionality can be accessed through the `stringr` package:\n\n- `str_c()`: Concatenates strings with optional separators.\n- `str_split()`: Splits strings into lists at specified delimiters.\n- `str_sub()`: Retrieves substrings based on character positions.\n\nProgramming languages also employ string manipulation for practical applications such as data validation, URL encoding, and natural language processing (e.g., keyword extraction). Specifically, regular expressions (regex) are invaluable for complex text manipulations, enabling tasks like extracting patterns or validating formats with succinct commands.\n\n### Sources\n- Real-World Applications of Strings : https://blog.heycoach.in/real-world-applications-of-strings/\n- Strings in Action: Real-World Tales of Text Manipulation : https://medium.com/@mohsin.shaikh324/strings-in-action-real-world-tales-of-text-manipulation-d3147466af14\n- Exploring Natural Language Processing Applications : https://www.coursera.org/articles/natural-language-processing-applications\n- Mastering Regular Expressions in Natural Language Processing (NLP) with Python : https://medium.com/@charmilagiri6/mastering-regular-expressions-in-natural-language-processing-nlp-with-python-2bbbfbac33e9",
                        "description": "Discussion of fundamental operations that can be performed on strings, such as concatenation, splitting, and substring extraction. This section will highlight built-in functions available in different programming languages."
                        "name": "Common String Operations",
                        "research": True
                    },
                    {
                        "content": "## Real-World Applications of Strings\n\n**Strings serve a crucial role in modern software development, particularly in text processing, form validation, and localization.** For instance, in applications such as online forms, strings validate user inputs to ensure formats like email addresses or phone numbers are correct. This capability prevents input errors and enhances data integrity.\n\nLocalization and internationalization processes also depend on strings. According to official documentation from JSON (JavaScript Object Notation), strings represent data structures that are essential in APIs used for localization (JSON, v2021). This allows applications to adapt their interfaces for different languages efficiently.\n\nAnother example includes natural language processing (NLP) applications where strings become pivotal. Tasks like sentiment analysis require string manipulation to understand emotional tones within textual data. NLP frameworks can parse and analyze user-generated content, enhancing interactions in platforms such as customer support chatbots.\n\n### Sources\n- Real-World Applications of Strings : https://blog.heycoach.in/real-world-applications-of-strings/\n- Strings in Action: Real-World Tales of Text Manipulation : https://medium.com/@mohsin.shaikh324/strings-in-action-real-world-tales-of-text-manipulation-d3147466af14\n- Exploring Natural Language Processing Applications : https://www.coursera.org/articles/natural-language-processing-applications"
                        "description": "Exploration of various real-world scenarios where strings are utilized, such as text processing in applications, form input validation, and localization.",
                        "name": "Real-World Applications of Strings"
                        "research": True
                    },
                    {
                        "content": "## Insight into String Manipulation Techniques\n\n**String manipulation techniques are foundational in programming, powering applications in text processing and data validation.** Regular expressions (regex) are among the most powerful string handling tools, allowing developers to efficiently search, extract, and manipulate text patterns. For example, the regex pattern `\\b[A-Z][a-z]+\\b` can be used to identify proper nouns within a text, which is essential in tasks like named entity recognition (NER) in natural language processing (NLP).\n\nCommon string manipulation functions include:\n- `str_detect()`: Checks if a specific pattern exists in a string.\n- `str_replace()`: Modifies the first occurrence of a pattern.\n- `str_extract()`: Retrieves the first match of a designated pattern from a string.\n\nThese functions enable valuable applications such as form validation in web applications, where input strings are matched against expected formats. A reported benchmark shows that regex can perform complex pattern matching tasks in under a second on datasets exceeding 1,000 entries (test case: `regex101.com`). Mastery of these techniques significantly enhances a developer’s ability to work with data efficiently.\n\n### Sources\n- Real-World Applications of Strings : https://blog.heycoach.in/real-world-applications-of-strings/\n- Strings in Action: Real-World Tales of Text Manipulation : https://medium.com/@mohsin.shaikh324/strings-in-action-real-world-tales-of-text-manipulation-d3147466af14\n- Mastering Regular Expressions in Natural Language Processing (NLP) with Python : https://medium.com/@charmilagiri6/mastering-regular-expressions-in-natural-language-processing-nlp-with-python-2bbbfbac33e9",
                        "description": "Insight into string manipulation techniques and common algorithms used in string processing, including search and matching algorithms, and their importance in programming.",
                        "name": "String Manipulation and Algorithms",
                        "research": True
                    },
                ]
            }
        """

        sections = json.loads(temp_json, object_hook=lambda d: SimpleNamespace(**d))
        return sections
    
    def get_sections2():
        temp_json = """
            {
            "sections": [
                {
                "content": '## Examination of the String Data Type\\n\\n**Strings are a fundamental data type in programming, used to represent textual information in various applications.** In computer memory, strings are typically represented as arrays of characters, often with an accompanying length field to optimize access and modification. For instance, in Python (version 3.x), strings are immutable, stored in a contiguous block of memory, necessitating the creation of new objects for modifications.\\n\nThe implementation and utility of strings vary across programming languages:\\n\\n| Language    | String Characteristics                                       | Example Use Case                                      |\\n|-------------|-------------------------------------------------------------|------------------------------------------------------|\\n| Python      | Immutable, supports Unicode                                 | Natural Language Processing (NLP) for sentiment analysis |\\n| Java        | Immutable, UTF-16 encoding                                  | Mobile applications requiring internationalization    |\\n| C++        | Mutable, requires manual memory management                  | Performance-intensive applications affecting string handling |\\n\nStrings facilitate numerous real-world applications including text processing, user input validation, and data serialization. In NLP, for instance, regular expressions (regex) are leveraged for tokenization and named entity recognition, as highlighted in regex implementations in Python (source: Mastering Regular Expressions in NLP). Proper string manipulation is essential for functionalities such as form validation and localization in web applications (source: Real-World Applications of Strings). \\n\\n### Sources\\n- Mastering Regular Expressions in Natural Language Processing (NLP) with Python: https://medium.com/@charmilagiri6/mastering-regular-expressions-in-natural-language-processing-nlp-with-python-2bbbfbac33e9\\n- Real-World Applications of Strings: https://blog.heycoach.in/real-world-applications-of-strings/',
                "description": "An examination of the concept of string as a data type, including its definition, how it is represented in memory, and the differences in implementation across various programming languages.",
                "name": "Overview of String Data Type",
                "research": true
                },
                {
                "content": "test2",
                "description": "Discussion of fundamental operations that can be performed on strings...",
                "name": "Common String Operations",
                "research": true
                },
                {
                "content": "test3",
                "description": "Exploration of various real-world scenarios where strings are utilized...",
                "name": "Real-World Applications of Strings",
                "research": true
                },
                {
                "content": "test4",
                "description": "Insight into string manipulation techniques and common algorithms...",
                "name": "String Manipulation and Algorithms",
                "research": true
                }
            ]
            }
        """

        sections = json.loads(temp_json, object_hook=lambda d: SimpleNamespace(**d))
        return sections


    
    def get_queries():
        temp_json = """
            {
                "queries": [
                    {
                        "search_query": "applications of strings in programming 2024 case studies text processing user input validation natural language processing localization"
                    },
                    {
                        "search_query": "string manipulation techniques natural language processing vs regular expressions 2024 comparison examples"
                    }
                ]
            }
        """
        queries = json.loads(temp_json, object_hook=lambda d: SimpleNamespace(**d))

        return queries
    def get_report_sections():
        temp_json = """
                        {
                            "sections": [
                                {
                                    "name": "Introduction",
                                    "description": "This section provides a brief overview of the string data type, its significance in programming, and its usage in various applications.",
                                    "research": false,
                                    "content": ""
                                },
                                {
                                    "name": "Overview of String Data Type",
                                    "description": "An examination of the concept of string as a data type, including its definition, how it is represented in memory, and the differences in implementation across various programming languages.",
                                    "research": true,
                                    "content": ""
                                },
                                {
                                    "name": "Common String Operations",
                                    "description": "Discussion of fundamental operations that can be performed on strings, such as concatenation, splitting, and substring extraction. This section will highlight built-in functions available in different programming languages.",
                                    "research": true,
                                    "content": ""
                                },
                                {
                                    "name": "Real-World Applications of Strings",
                                    "description": "Exploration of various real-world scenarios where strings are utilized, such as text processing in applications, form input validation, and localization.",
                                    "research": true,
                                    "content": ""
                                },
                                {
                                    "name": "String Manipulation and Algorithms",
                                    "description": "Insight into string manipulation techniques and common algorithms used in string processing, including search and matching algorithms, and their importance in programming.",
                                    "research": true,
                                    "content": ""
                                },
                                {
                                    "name": "Conclusion",
                                    "description": "A summary of the key points covered in the report, highlighting the importance of string data types and their applications, along with a concise list of fundamental concepts discussed.",
                                    "research": false,
                                    "content": ""
                                }
                            ]
                        }
                    """

        # Convert the JSON string to a list of objects with dot notation
        report_sections = json.loads(temp_json, object_hook=lambda d: SimpleNamespace(**d))

        return report_sections