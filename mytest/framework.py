TICK = "\u2713"
CROSS = "\u2717"
WARNING = "\u26A0"
BULLET = "\u2022"

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
GREY = "\033[90m"
RESET = "\033[0m"

total_test_count = 0
passed_count = 0
failed_count = 0

def print_test_result(test_name: str, passed: bool) -> None:
    global passed_count, failed_count, total_test_count
    total_test_count += 1

    if passed:
        print(f"{GREEN}{TICK} PASS{RESET} {test_name}{RESET}")
        passed_count += 1
    else:
        print(f"{RED}{CROSS} FAIL{RESET} {test_name}{RESET}")
        failed_count += 1

def print_test_group_header(group_name: str) -> None:
    print(f"\n{BULLET} Testing {group_name}")

def print_test_group_subheader(subgroup_name: str) -> None:
    print(f"\n{GREY}{BULLET} TEST {subgroup_name}{RESET}")

def print_header() -> None:
    print("Running tests...\n")

def print_footer() -> None:
    if failed_count == 0:
        print(f"\n{GREEN}{TICK} {passed_count} / {total_test_count} tests passed.{RESET}")
    elif passed_count != 0:
        print(f"\n{YELLOW}{WARNING} {passed_count} / {total_test_count} tests passed.{RESET}")
    else:
        print(f"\n{RED}{CROSS} {passed_count} / {total_test_count} tests passed.{RESET}")
