from typing import List, Optional, Union, Dict, Tuple
import requests
import urllib.parse
import os

class SDKException(Exception):
    pass

class InvalidMovieNameException(SDKException):
    pass

class InvalidCharacterNameException(SDKException):
    pass

class APIException(SDKException):
    pass

class Movie:
    def __init__(self, id: str, name: str, runtime: int, budget: int, box_office: int, academy_award_nominations: int, academy_award_wins: int, rotten_tomatoes_score: float):
        self.id = id
        self.name = name
        self.runtime = runtime
        self.budget = budget
        self.box_office = box_office
        self.academy_award_nominations = academy_award_nominations
        self.academy_award_wins = academy_award_wins
        self.rotten_tomatoes_score = rotten_tomatoes_score
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Movie':
        return cls(
            id=data["_id"],
            name=data["name"],
            runtime=data["runtimeInMinutes"],
            budget=data["budgetInMillions"],
            box_office=data["boxOfficeRevenueInMillions"],
            academy_award_nominations=data["academyAwardNominations"],
            academy_award_wins=data["academyAwardWins"],
            rotten_tomatoes_score=data["rottenTomatoesScore"]
        )

class Quote:
    def __init__(self, id: str, dialog: str, movie: str, character: str):
        self.id = id
        self.dialog = dialog
        self.movie = movie
        self.character = character
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Quote':
        return cls(
            id=data["_id"],
            dialog=data["dialog"],
            movie=data["movie"],
            character=data["character"]
        )

    # Redefine equality for Quote objects
    def __eq__(self, other):
        if isinstance(other, Quote):
            return (self.id == other.id) and (self.dialog == other.dialog) and (self.movie == other.movie) and (self.character == other.character)
        return False

class LotrSDK:
    def __init__(self, token: str):
        self.base_url = 'https://the-one-api.dev/v2'
        self.token = token
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.movie_name_to_id_map = self._get_movie_id_map()
        self.character_name_to_id_map = self._get_character_id_map()

    def _operator_to_api_format(self, operator: str) -> str:
        return {
            "eq": "=",  # Equals
            "neq": "!=",  # Not equals
            "in": "=", # in 
            # "nin": "!",  # Not in (currently not supported)
            # "exists": "",  # Exists (currently not supported)
            # "nexists": "!",  # Not exists (currently not supported)
            # "regex": "=",  # Regular expression (currently not supported)
            # "lt": "<",  # Less than (currently not supported)
            # "gt": ">",  # Greater than (currently not supported)
            # "lte": "<=",  # Less than or equal to (currently not supported)
            # "gte": ">="  # Greater than or equal to (currently not supported)
        }.get(operator, "")

    # General Request Methods
    def _send_request(self, url: str, expected_data: str) -> Union[List[Dict], Dict, Tuple[Union[List[Dict], Dict], bool]]:
        """Send a request to the API and handle common response scenarios."""
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json().get(expected_data)
            if data == None:
                raise APIException("The API returned an unexpected response.")
            return data, response.json()['pages'] > response.json()['page']
        else:
            raise APIException(f"Unable to connect to the API endpoint. Received status code: {response.status_code}")

    def _fetch_paginated_data(self, base_url: str, expected_data: str) -> List[Dict]:
        """Fetches paginated data from the given URL until no more data is available."""
        data = []
        page = 1
        while True:
            response_data, has_more_data = self._send_request(f"{base_url}?page={page}", expected_data)
            data.extend(response_data)
            if not has_more_data:
                break
            page += 1
        return data

    def _create_sorting_query(self, sort: Dict[str, str]) -> str:
        """Helper function to convert a dict of sorting params into a sorting query string."""
        if not sort:
            return ""
        return f"sort={','.join(f'{k}:{v}' for k, v in sort.items())}"

    def _create_filtering_query(self, filter: Optional[Dict[str, Dict[str, str]]] = None) -> str:
        """Helper function to convert a dict of filtering params into a filtering query string."""
        if not filter:
            return ""

        query_parts = []
        for key, condition in filter.items():
            operator = self._operator_to_api_format(condition.get("operator"))
            value = urllib.parse.quote_plus(condition.get("value"))  # URL encoding the value

            query_parts.append(f"{key}{operator}{value}")
        
        return '&'.join(query_parts)

    def _sanitize_name(self, name: str) -> str:
        """Helper function to sanitize movie names for comparison: lowercase and no spaces."""
        return name.lower().replace(' ', '')
    
    # Validate Methods
    def _validate_movie_name(self, name: str):
        """Check if the movie name is valid."""
        sanitized_name = self._sanitize_name(name)
        if sanitized_name not in self.movie_name_to_id_map:
            raise InvalidMovieNameException(f"No movie found with the name {name}")
    
    def _validate_character_name(self, name: str):
            """Check if the character name is valid."""
            sanitized_name = self._sanitize_name(name)
            if sanitized_name not in self.character_name_to_id_map:
                raise InvalidCharacterNameException(f"No character found with the name {name}")
            
    def _validate_filter(self, filter: Dict[str, Dict[str, str]]):
        """Check if the filter operator is currently supported."""
        for key in filter:
            operator = filter[key].get('operator')
            if operator not in ["eq", "neq"]:
                raise SDKException(f"The operator {operator} is not currently supported.")


    # Movie Methods
    def _get_movie_id_map(self):
        """Builds a map of movie names to IDs, ignoring case and spaces."""
        data = self._fetch_paginated_data(f"{self.base_url}/movie?page=1", 'docs')
        return {self._sanitize_name(movie["name"]): movie["_id"] for movie in data}
        
    def _get_movie_id(self, name: str):
        """Returns the movie ID for a given name, ignoring case and spaces."""
        self._validate_movie_name(name)
        return self.movie_name_to_id_map[self._sanitize_name(name)]

    def _get_movie_by_id(self, movie_id: str) -> Movie:
        """Get specific movie by its ID."""
        data = self._send_request(f"{self.base_url}/movie/{movie_id}", 'docs')[0]
        return Movie.from_dict(data)

    def get_movie(self, name: str) -> Movie:
        """Gets a movie by its name, ignoring case and spaces."""
        movie_id = self._get_movie_id(name)
        return self._get_movie_by_id(movie_id)
    

    # Quote Methods
    def _get_quotes_by_movie_id(self, movie_id: str) -> List[Quote]:
        """Gets quotes by movie ID."""
        data = self._send_request(f"{self.base_url}/movie/{movie_id}/quote", 'docs')
        return [Quote.from_dict(quote) for quote in data]

    def get_quote_by_id(self, quote_id: str) -> Quote:
        """Get specific quote by its ID."""
        data = self._send_request(f"{self.base_url}/quote/{quote_id}", 'docs')[0]
        return Quote.from_dict(data)

    def get_quotes(self, movies: Optional[List[str]] = None, characters: Optional[List[str]] = None, 
                sort: Optional[Dict[str, str]] = None, filter: Optional[Dict[str, str]] = None, 
                limit: Optional[int] = 10) -> List[Quote]:

        sort_query = self._create_sorting_query(sort)
        if sort_query is None:
            sort_query = ''
        else:
            sort_query = '&' + sort_query

        combined_filter = {}

        if movies:
            movie_ids = [self._get_movie_id(movie) for movie in movies]
            combined_filter["movie"] = {"operator": "in", "value": ",".join(movie_ids)}
        
        if characters:
            character_ids = [self._get_character_id(character) for character in characters]
            combined_filter["character"] = {"operator": "in", "value": ",".join(character_ids)}

        # If there is a filter argument provided, include it in the combined filter
        if filter:
            self._validate_filter(filter)
            combined_filter.update(filter)

        combined_filter_query = self._create_filtering_query(combined_filter)

        print(f"{self.base_url}/quote?{combined_filter_query}&limit={limit}{sort_query}")
        data = self._fetch_paginated_data(f"{self.base_url}/quote?{combined_filter_query}&limit={limit}{sort_query}", 'docs')
        return [Quote.from_dict(quote) for quote in data]


    # Character Methods
    def _get_character_id_map(self):
        """Builds a map of character names to IDs, ignoring case and spaces."""
        data = self._fetch_paginated_data(f"{self.base_url}/character?page=1", 'docs')
        return {self._sanitize_name(character["name"]): character["_id"] for character in data}

    def _get_character_id(self, name: str):
        """Returns the character ID for a given name, ignoring case and spaces."""
        self._validate_character_name(name)
        return self.character_name_to_id_map[self._sanitize_name(name)]

    def _get_quotes_by_character_id(self, character_id: str) -> List[Quote]:
        """Gets quotes by character ID."""
        response = requests.get(f"{self.base_url}/character/{character_id}/quote", headers=self.headers)
        data = response.json()['docs']
        return [Quote.from_dict(quote) for quote in data]
