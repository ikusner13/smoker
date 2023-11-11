# Usage Guide

This guide will help you set up and run the Python servers.

## Prerequisites

Ensure you have the following installed on your machine:

- Python 3.x
- pip

## Installation

1. Clone the repository

```bash
git clone https://github.com/ikusner13/smoker.git
```

1. Navigate to the server directory and install a virtual environment.

```bash
cd server
python3 -m venv venv

pip install -r requirements.txt
```

## Running the UDP and websocket server

To run the server, execute the following command in the terminal:

```bash
python3 main.py
```

## Running websocket client

```bash
  cd client
  python3 -m http.server
```
