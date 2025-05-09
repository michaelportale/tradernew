import os
from dotenv import load_dotenv

# Load .env file from project root
base_dir = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(base_dir, "..", ".env")
print(f"Looking for .env file at: {env_file}")
print(f"File exists: {os.path.exists(env_file)}")

# Try to load the .env file
load_dotenv(env_file)

# Print the environment variables
print("Environment variables:")
print(f"POSTGRES_SERVER: {os.environ.get('POSTGRES_SERVER', 'Not set')}")
print(f"POSTGRES_USER: {os.environ.get('POSTGRES_USER', 'Not set')}")
print(f"POSTGRES_PASSWORD: {os.environ.get('POSTGRES_PASSWORD', 'Not set')}")
print(f"POSTGRES_DB: {os.environ.get('POSTGRES_DB', 'Not set')}")
print(f"REDIS_HOST: {os.environ.get('REDIS_HOST', 'Not set')}")
print(f"REDIS_PORT: {os.environ.get('REDIS_PORT', 'Not set')}")

# Print the .env file contents
print("\n.env file contents:")
if os.path.exists(env_file):
    with open(env_file, 'r') as f:
        print(f.read())
