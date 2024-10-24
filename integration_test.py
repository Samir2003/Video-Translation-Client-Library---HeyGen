import subprocess
import time
import pytest
import requests
from client import TranslationClient

# Fixture to spin up the server
@pytest.fixture(scope="module")
def start_server():
    # Start the server as a subprocess
    server_process = subprocess.Popen(['python3', 'server.py'])
    
    # Give the server time to start
    time.sleep(2)
    
    # Yield control back to the test, and once done, the following teardown code will run
    yield
    
    # Teardown: Kill the server subprocess after tests are done
    server_process.terminate()

# The integration test using the client library
def test_client_poll_status(start_server):
    # Initialize the client and poll for status
    client = TranslationClient("http://127.0.0.1:5000")
    
    # Poll the status and check that the result is either 'completed' or 'error'
    final_status = client.poll_status()
    
    assert final_status in ['completed', 'error'], f"Unexpected final status: {final_status}"
    
    print(f"Integration Test: Final status of the job is '{final_status}'")
