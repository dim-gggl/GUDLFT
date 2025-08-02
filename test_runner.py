#!/usr/bin/env python3
"""
Script simple pour exécuter les tests unitaires
"""
import os
import sys

# Add the root directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_test_save_competitions_data():
    """Specific test for save_competitions_data"""
    try:
        from tests.unit_tests.test_data_manager import (
            test_save_competitions_data,
        )

        test_save_competitions_data()
        print("✅ test_save_competitions_data: PASSED")
        return True
    except Exception as e:
        print(f"❌ test_save_competitions_data: FAILED - {e}")
        return False


def run_test_save_clubs_data():
    """Test for save_clubs_data"""
    try:
        from tests.unit_tests.test_data_manager import test_save_clubs_data

        test_save_clubs_data()
        print("✅ test_save_clubs_data: PASSED")
        return True
    except Exception as e:
        print(f"❌ test_save_clubs_data: FAILED - {e}")
        return False


def run_test_update_existing_club_and_competition():
    """Test for update_existing_club_and_competition"""
    try:
        from tests.unit_tests.test_data_manager import (
            test_update_existing_club_and_competition,
        )

        test_update_existing_club_and_competition()
        print("✅ test_update_existing_club_and_competition: PASSED")
        return True
    except Exception as e:
        print(f"❌ test_update_existing_club_and_competition: FAILED - {e}")
        return False


def run_test_update_new_objects():
    """Test for update_new_objects"""
    try:
        from tests.unit_tests.test_data_manager import test_update_new_objects

        test_update_new_objects()
        print("✅ test_update_new_objects: PASSED")
        return True
    except Exception as e:
        print(f"❌ test_update_new_objects: FAILED - {e}")
        return False


def run_test_successful_booking():
    """Test for successful_booking"""
    try:
        from tests.unit_tests.test_data_manager import test_successful_booking

        test_successful_booking(app_context=current_app.app_context())
        print("✅ test_successful_booking: PASSED")
        return True
    except Exception as e:
        print(f"❌ test_successful_booking: FAILED - {e}")
        return False


def run_test_booking_with_validation_error():
    """Test for booking_with_validation_error"""
    try:
        from tests.unit_tests.test_data_manager import (
            test_booking_with_validation_error,
        )

        test_booking_with_validation_error()
        print("✅ test_booking_with_validation_error: PASSED")
        return True
    except Exception as e:
        print(f"❌ test_booking_with_validation_error: FAILED - {e}")
        return False


def run_all_data_manager_tests():
    """Run all data_manager tests"""
    tests = [
        ("test_save_competitions_data", run_test_save_competitions_data),
        ("test_save_clubs_data", run_test_save_clubs_data),
        (
            "test_update_existing_club_and_competition",
            run_test_update_existing_club_and_competition,
        ),
        ("test_update_new_objects", run_test_update_new_objects),
        ("test_successful_booking", run_test_successful_booking),
        (
            "test_booking_with_validation_error",
            run_test_booking_with_validation_error,
        ),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n--- Running {test_name} ---")
        if test_func():
            passed += 1

    print(f"\n--- Results ---")
    print(f"Passed: {passed}/{total}")
    return passed == total


if __name__ == "__main__":
    success = run_all_data_manager_tests()
    sys.exit(0 if success else 1)
