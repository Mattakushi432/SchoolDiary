#!/usr/bin/env python
"""
Simple test runner script for the journal app tests.
Run this after activating your virtual environment and installing Django.
"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SchoolDiary.settings')
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["journal.tests"])
    if failures:
        sys.exit(1)