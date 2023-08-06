import unittest
from unittest.mock import patch, MagicMock
from unittest import TestCase, mock, main
from lotr_sdk.sdk import LotrSDK, Movie, Quote, SDKException, InvalidMovieNameException, InvalidCharacterNameException, APIException

class TestLotrSDK(TestCase):
    @patch('lotr_sdk.sdk.requests.get')
    @patch.object(LotrSDK, '_get_movie_id_map', return_value={"thefellowshipofthering": "1"})
    @patch.object(LotrSDK, '_get_character_id_map', return_value={"character1": "id1", "character2": "id2"})
    def setUp(self, mock_get, mock_movie_map, mock_character_map):
        self.sdk = LotrSDK('test_token')

    def test_sanitize_name(self):
        # Use self.sdk, which was set in setUp
        self.assertEqual(self.sdk._sanitize_name("The Fellowship of the Ring"), "thefellowshipofthering")

    def test_validate_movie_name(self):
        # Use self.sdk, which was set in setUp
        # Should not raise
        self.sdk._validate_movie_name("The Fellowship of the Ring")

    def test_validate_movie_name_invalid(self):
        # Use self.sdk, which was set in setUp
        # Should raise InvalidMovieNameException
        with self.assertRaises(InvalidMovieNameException):
            self.sdk._validate_movie_name("Unknown Movie")

    def test_get_movie_id(self):
        # Use self.sdk, which was set in setUp
        self.assertEqual(self.sdk._get_movie_id("The Fellowship of the Ring"), "1")

    def test_get_movie_id_invalid(self):
        # Use self.sdk, which was set in setUp
        # Should raise InvalidMovieNameException
        with self.assertRaises(InvalidMovieNameException):
            self.sdk._get_movie_id("Unknown Movie")

    def test_get_movie_by_id(self):
        # Mocking the _send_request method to return a sample movie data
        movie_data = {
            "_id": "1",
            "name": "The Fellowship of the Ring",
            "runtimeInMinutes": 178,
            "budgetInMillions": 93,
            "boxOfficeRevenueInMillions": 871,
            "academyAwardNominations": 13,
            "academyAwardWins": 4,
            "rottenTomatoesScore": 91
        }
        with mock.patch.object(self.sdk, '_send_request', return_value=(movie_data, False)):
            movie = self.sdk._get_movie_by_id("1")
            self.assertEqual(movie.id, movie_data["_id"])
            self.assertEqual(movie.name, movie_data["name"])

    def test_get_movie(self):
        # Mocking the _send_request method to return a sample movie data
        movie_data = {
            "_id": "1",
            "name": "The Fellowship of the Ring",
            "runtimeInMinutes": 178,
            "budgetInMillions": 93,
            "boxOfficeRevenueInMillions": 871,
            "academyAwardNominations": 13,
            "academyAwardWins": 4,
            "rottenTomatoesScore": 91
        }
        with mock.patch.object(self.sdk, '_send_request', return_value=(movie_data, False)):
            movie = self.sdk.get_movie("The Fellowship of the Ring")
            self.assertEqual(movie.id, movie_data["_id"])
            self.assertEqual(movie.name, movie_data["name"])

    def test_validate_character_name(self):
        # Should not raise
        self.sdk._validate_character_name("character1")

    def test_validate_character_name_invalid(self):
        # Should raise InvalidCharacterNameException
        with self.assertRaises(InvalidCharacterNameException):
            self.sdk._validate_character_name("Unknown Character")

    def test_get_character_id(self):
        self.assertEqual(self.sdk._get_character_id("character1"), "id1")

    def test_get_character_id_invalid(self):
        # Should raise InvalidCharacterNameException
        with self.assertRaises(InvalidCharacterNameException):
            self.sdk._get_character_id("Unknown Character")

    def test_get_quote_by_id(self):
        # Mocking the _send_request method to return a sample quote data
        quote_data = {
            "_id": "quote1",
            "dialog": "Some interesting dialog",
            "movie": "The Fellowship of the Ring",
            "character": "Gandalf"
        }
        with mock.patch.object(self.sdk, '_send_request', return_value=(quote_data, False)):
            quote = self.sdk.get_quote_by_id("quote1")
            self.assertEqual(quote.id, quote_data["_id"])
            self.assertEqual(quote.dialog, quote_data["dialog"])

    def test_get_quotes(self):
        # Mocking the _send_request method to return a sample quote data
        quote_data_list = [
            {
                "_id": "quote1",
                "dialog": "Some interesting dialog 1",
                "movie": "The Fellowship of the Ring",
                "character": "character1"
            },
            {
                "_id": "quote2",
                "dialog": "Some interesting dialog 2",
                "movie": "The Fellowship of the Ring",
                "character": "character2"
            },
        ]
        with mock.patch.object(self.sdk, '_fetch_paginated_data', return_value=quote_data_list):
            quotes = self.sdk.get_quotes(movies=["The Fellowship of the Ring"], characters=["character1", "character2"])
            self.assertEqual(len(quotes), 2)
            for quote, expected_quote_data in zip(quotes, quote_data_list):
                self.assertEqual(quote.id, expected_quote_data["_id"])
                self.assertEqual(quote.dialog, expected_quote_data["dialog"])



if __name__ == "__main__":
    unittest.main()
