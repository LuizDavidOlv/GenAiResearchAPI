import json
from types import SimpleNamespace


class Temp:
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