# The Lord of the Rings SDK

This SDK provides an easy interface to interact with the Lord of the Rings API. You can fetch movies, characters, and quotes data. The SDK handles common tasks such as pagination, sorting, and filtering.

## Installation

The SDK can be installed via pip:

```
pip install lotr-sdk
```

## Basic Usage

Start by creating an instance of the SDK with your API token:

```python
from lotr_sdk import LotrSDK

sdk = LotrSDK('your_api_token')
```

### Fetching Movie Data

Fetch a movie by its name:

```python
movie = sdk.get_movie('The Fellowship of the Ring')
print(movie.name)  # Prints: The Fellowship of the Ring
```

### Fetching Quote Data

Fetch a quote by its ID:

```python
quote = sdk.get_quote_by_id('quote_id')
print(quote.dialog)  # Prints: quote dialog
```

Fetch quotes by movie names:

```python
quotes = sdk.get_quotes(movies=['The Fellowship of the Ring', 'The Two Towers'])
for quote in quotes:
    print(quote.dialog)
```

### Fetching Character Data

Fetch quotes by character names:

```python
quotes = sdk.get_quotes(characters=['Frodo Baggins', 'Gandalf'])
for quote in quotes:
    print(quote.dialog)
```

### Pagination, Sorting, and Filtering

The `get_quotes` method supports pagination, sorting, and filtering:

```python
quotes = sdk.get_quotes(
    movies=['The Fellowship of the Ring'],
    sort={'movie': 'asc', 'character': 'desc'},
    filter={'character': 'eq:Frodo Baggins'},
    limit=10
)
```

- The `movies` and `characters` parameters take a list of movie and character names respectively.
- The `sort` parameter takes a dictionary of fields and their sorting order ('asc' or 'desc').
- The `filter` parameter takes a dictionary of fields and their filter value. The filter format is 'operator:value'. Available operators are 'eq' (equals), 'neq' (not equals), 'in' (in), 'nin' (not in), 'exists' (exists), 'nexists' (not exists), 'regex' (regular expression), 'lt' (less than), 'gt' (greater than), 'lte' (less than or equal to), and 'gte' (greater than or equal to).
- The `limit` parameter takes an integer for the maximum number of results per page. The SDK handles fetching all pages automatically.

### Error Handling

The SDK throws custom exceptions for common error scenarios:

- `SDKException`: Base exception class for the SDK.
- `InvalidMovieNameException`: Thrown when no movie is found with the provided name.
- `InvalidCharacterNameException`: Thrown when no character is found with the provided name.
- `APIException`: Thrown when an API request fails.

## Contribution

Contributions are welcome! Please submit a pull request with any enhancements, fixes, or features.
