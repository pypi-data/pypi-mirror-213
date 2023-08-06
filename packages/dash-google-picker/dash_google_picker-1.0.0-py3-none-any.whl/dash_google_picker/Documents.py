from typing import List, Dict, Union
from dataclasses import dataclass

@dataclass
class GoogleDocument:
    """
    A dataclass representing a Google Document. 

    The class takes a dictionary as an argument and sets the key-value pairs as attributes
    on the object. The dictionary should represent the properties of a Google Document
    as per the Google Picker API (https://developers.google.com/drive/picker/reference#document).

    Attributes are dynamically set based on the key-value pairs in the dictionary provided.
    """

    def __init__(self, dict_data: Dict[str, Union[str, int, bool]]):
        """
        Initialize a GoogleDocument object with a dictionary.

        :param dict_data: A dictionary where the keys represent attribute names and the values
                          represent attribute values. Should represent a Google Document as 
                          per the Google Picker API.
        """
        for key, value in dict_data.items():
            setattr(self, key, value)

class GoogleDocuments:
    """
    A class to represent a list of GoogleDocument objects.

    The class takes a list of dictionaries as an argument and creates a GoogleDocument object
    for each dictionary in the list.

    Usage:
    documents = GoogleDocuments([{'id': '1', 'title': 'Title', 'url': 'http://...'}, {...}, ...])
    """

    def __new__(cls, documents_data: List[Dict[str, Union[str, int, bool]]]) -> List[GoogleDocument]:
        """
        Create a list of GoogleDocument objects from a list of dictionaries.

        :param documents_data: A list of dictionaries where each dictionary should represent
                               the properties of a Google Document as per the Google Picker API.
        :return: A list of GoogleDocument objects.
        """
        if documents_data is None:
            return []
        else:
            return [GoogleDocument(doc) for doc in documents_data]