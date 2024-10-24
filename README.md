# Video Translation Client Library & Server Simulation

This repository contains a simulated **video translation server** and a **client library** that interacts with the server to get the status of a video translation job. The client implements an optimized polling mechanism with **exponential backoff** to reduce unnecessary calls.

## Table of Contents

- [Overview](#overview)
- [Setup Instructions](#setup-instructions)
- [How to Run the Application](#how-to-run-the-application)
  - [Running the Server](#running-the-server)
  - [Using the Client](#using-the-client)
  - [Running the Integration Test](#running-the-integration-test)
- [How the Server Works](#how-the-server-works)
- [How the Client Works](#how-the-client-works)
- [How We Improved Beyond a Trivial Approach](#how-we-improved-beyond-a-trivial-approach)
- [Bells and Whistles](#bells-and-whistles)

---

## Overview

The app consists of:
1. A **Server** (`server.py`) that simulates the video translation backend and returns the status of a job (`pending`, `completed`, or `error`).
2. A **Client Library** (`client.py`) that polls the server to check the status of the job. It uses an **exponential backoff** strategy to reduce frequent requests while ensuring timely results.
3. An **Integration Test** (`integration_test.py`) using **pytest** that demonstrates how to use the client to interact with the server and checks if the status is fetched correctly.

---

## Setup Instructions

### Dependencies:
You will need to install the dependencies required by the code:

   ```bash
   pip install -r ./requirements.txt 
   ```
   
### Files:
- **server.py**: The Flask-based server simulates the backend.
- **client.py**: The client library that communicates with the server.
- **integration_test.py**: Test case demonstrating the interaction between the client and the server.
- **README.md**: This file explaining how to use the app.

---

## How to Run the Application

### Running the Server
1. To start the server that simulates video translation, simply run:

   ```bash
   python server.py
   ```
   This will start the server at `http://127.0.0.1:5000`. You can verify the status by visiting `http://127.0.0.1:5000/status`.

   The server will initially return `{"result": "pending"}` and after a configurable delay (10 seconds by default), it will return either `completed` or `error`.

### Using the Client

1. To use the client to poll the server, modify and run the following code in `client.py`:

   ```python
   from client import TranslationClient

   client = TranslationClient("http://127.0.0.1:5000")
   final_status = client.poll_status()

   print(f"The final status of the job is: {final_status}")
    ```

This client will keep polling the server until it receives a result of `completed` or `error`, using exponential backoff to reduce unnecessary requests.

### Running the Integration Test

1. You can run the integration test that starts the server, uses the client to check the status, and terminates the server after the test.

   ```bash
   pytest -s integration_test.py
    ```
This will display the result of the test along with logs. The `-s` flag ensures that print statements are shown in the output.

---

## How the Server Works

The server is a Flask application that simulates a video translation process:
- The server tracks the time elapsed since it was started.
- It returns a status of `pending` until a configurable delay has passed (set to 10 seconds by default).
- After the delay, it randomly returns `completed` or `error` based on a configurable error probability (10% by default).

---

## How the Client Works

The client library polls the server to check the status of the job:
- The `get_status()` method makes an HTTP GET request to `http://127.0.0.1:5000/status`.
- The `poll_status()` method implements **exponential backoff**, which starts with a 1-second delay between polls and doubles the delay after each attempt. This minimizes the number of requests made to the server while still ensuring timely retrieval of the status.
- The polling stops when the status is either `completed` or `error`, or when the maximum number of retries (configurable) is reached.

## How We Improved Beyond a Trivial Approach

### The Trivial Approach:
A trivial approach would involve polling the server with a fixed delay between each request, regardless of the response. This would result in either:
- **Too frequent polling**: This would increase the load on the server, causing unnecessary requests that could slow down performance.
- **Too infrequent polling**: This would lead to unnecessary delays in retrieving the status, causing a bad user experience.

### Our Optimized Approach:
We implemented **exponential backoff** in the client library:
- **Exponential backoff** increases the delay between consecutive requests, starting from a short delay and gradually increasing it. This optimizes the polling by reducing the number of requests when the result is likely still `pending`, while ensuring responsiveness when the result is close to being ready.
- This approach balances the cost of polling with the urgency of getting the result in a timely manner.

## Bells and Whistles

Here are some extra features implemented in the app:

1. **Exponential Backoff**: Instead of using fixed polling intervals, the client uses exponential backoff to optimize requests and avoid unnecessary load on the server.
   
2. **Configurable Server Delay**: The server simulates a realistic video translation process with configurable delays and error chances, providing a more accurate test environment.
   
3. **pytest Integration**: The test script is structured using `pytest` for easy setup, teardown, and execution. This ensures that the server starts and stops automatically as part of the testing process.

4. **Graceful Error Handling**: The client library gracefully handles any HTTP errors or connection issues with appropriate logging, ensuring robustness in real-world scenarios.
