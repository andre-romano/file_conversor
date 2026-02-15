# src\file_conversor\tests\conftest.py
import sys

from pathlib import Path


src_dir = str(Path(__file__).resolve().parents[1] / "src")
sys.path.insert(0, src_dir)

print(f"Added to sys.path:\n'{src_dir}'")
