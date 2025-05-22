# Import the json module to parse the Lambda response body (which is a JSON string)
import json

# Import pytest to structure and run tests using the pytest framework
import pytest

# Import MagicMock to mock objects and methods, allowing us to simulate DynamoDB
from unittest.mock import MagicMock

# Import the actual Lambda function handler from your application code
from src.handlers.hello import handler


# Define a pytest fixture to create and return a mock DynamoDB table
# This fixture will be injected into tests that require it
@pytest.fixture
def mock_table():
    return MagicMock()  # Create a mock object that simulates a table


# Test case for successful DynamoDB insertion
def test_handler_success(mock_table):
    # Simulate a successful put_item call by returning an empty dict (what boto3 does on success)
    mock_table.put_item.return_value = {}

    # Call the Lambda handler with an empty event and context, injecting the mock_table
    response = handler(event={}, context={}, table=mock_table)

    # Parse the JSON response body into a Python dictionary
    body = json.loads(response['body'])

    # Assert that the Lambda returned HTTP 200 OK
    assert response['statusCode'] == 200

    # Assert that the expected message is in the response body
    assert 'Hello, world!' in body['message']

    # Check that put_item was called exactly once
    mock_table.put_item.assert_called_once()

    # Confirm that the `Item` parameter was used in the put_item call
    assert 'Item' in mock_table.put_item.call_args.kwargs


# Test case for simulating a DynamoDB failure (e.g., AWS service error)
def test_handler_dynamodb_failure(mock_table):
    # Import ClientError to simulate a boto3 exception
    from botocore.exceptions import ClientError

    # Simulate put_item throwing a ClientError, mimicking a real failure from DynamoDB
    mock_table.put_item.side_effect = ClientError(
        error_response={'Error': {'Code': '500', 'Message': 'Internal Server Error'}},
        operation_name='PutItem'
    )

    # Call the handler with mock event/context and the mocked table
    response = handler(event={}, context={}, table=mock_table)

    # Expect the function to return HTTP 500 due to the simulated error
    assert response['statusCode'] == 500

    # Ensure put_item was called once, even though it failed
    mock_table.put_item.assert_called_once()
