import sys
import os

# Get the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

# Add project root to Python path
sys.path.insert(0, project_root)

print(f"Project root added to path: {project_root}")
print(f"Python path: {sys.path}")