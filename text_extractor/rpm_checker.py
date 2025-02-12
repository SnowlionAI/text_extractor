import time

def rpm_checker(RATE_LIMIT_RPM, MINIMUM_WAIT_SECONDS):
    """
    Checks if a new call can be made, prioritizing immediate calls (respecting min wait)
    until the rate limit (RPM) is reached, then enforces waiting.

    Args:
        RATE_LIMIT_RPM: The rate limit in rounds per minute (RPM).
        MINIMUM_WAIT_SECONDS: The minimum time in seconds that must elapse between consecutive calls.

    Returns:
        float: 0 if a new call can be made immediately, otherwise the number of seconds to wait.
    """
    if not hasattr(rpm_checker, 'last_call_time'):
        rpm_checker.last_call_time = None
    if not hasattr(rpm_checker, 'call_timestamps_minute'):
        rpm_checker.call_timestamps_minute = []

    current_time = time.time()
    last_call_time = rpm_checker.last_call_time

    min_time = 0
    rpm_time = 0

    # 1. Enforce Minimum Wait
    if last_call_time is not None:
        elapsed_since_last_call = current_time - last_call_time
        if elapsed_since_last_call < MINIMUM_WAIT_SECONDS:
            wait_time_min = MINIMUM_WAIT_SECONDS - elapsed_since_last_call
            min_time = wait_time_min

    # 2. RPM Check: Count calls in the last minute
    one_minute_ago = current_time - 60.0
    rpm_checker.call_timestamps_minute = [
        ts for ts in rpm_checker.call_timestamps_minute if ts >= one_minute_ago
    ]

    if RATE_LIMIT_RPM == 0 or len(rpm_checker.call_timestamps_minute) < RATE_LIMIT_RPM:
        # Call is allowed, update timestamps
        rpm_checker.last_call_time = current_time
        rpm_checker.call_timestamps_minute.append(current_time)
        rpm_time = 0.0
    else:
        # Rate limit reached, calculate wait time based on the oldest call in the minute window
        oldest_call_time = rpm_checker.call_timestamps_minute[0]
        wait_time_rpm = (oldest_call_time + 60.0) - current_time
        if wait_time_rpm < 0:
            wait_time_rpm = 0.0 # Ensure wait time is not negative
        rpm_time = wait_time_rpm

    return max(min_time, rpm_time)


def test_rpm():
    """
    Tests the rpm_checker function by simulating multiple calls with various rates and times.
    """
    
    # Example Usage (Corrected Eager RPM with Minimum Wait)
    RATE_LIMIT_RPM = 15
    MINIMUM_WAIT_SECONDS = 0.5

    print("--- Corrected Eager RPM Test - Within Rate Limit ---")
    for i in range(10): # Calls well within rate limit, should be near immediate
        wait_seconds = rpm_checker(RATE_LIMIT_RPM, MINIMUM_WAIT_SECONDS)
        if wait_seconds > 0:
            print(f"Call {i+1} - No call wait: {wait_seconds}")
            time.sleep(wait_seconds)
        else:
            print(f"Call {i+1} - Call allowed, no wait required: {wait_seconds}")

    print("\n--- Corrected Eager RPM Test - Exceeding Rate Limit ---")
    for i in range(20): # Calls exceeding rate limit, should start waiting after ~15 calls in a minute
        wait_seconds = rpm_checker(RATE_LIMIT_RPM, MINIMUM_WAIT_SECONDS)
        if wait_seconds > 0:
            print(f"Call {10+i+1} - No call wait: {wait_seconds}")
            time.sleep(wait_seconds)
        else:
            print(f"Call {10+i+1} - Call allowed, no wait required: {wait_seconds}")

    print("\n--- Corrected Eager RPM Minimum Wait Test (faster than min wait) ---")
    for i in range(5): # Calls faster than minimum wait, minimum wait should be enforced
        wait_seconds = rpm_checker(RATE_LIMIT_RPM, MINIMUM_WAIT_SECONDS)
        if wait_seconds > 0:
            print(f"Call {30+i+1} - No call wait: {wait_seconds}")
            time.sleep(wait_seconds)
        else:
            print(f"Call {30+i+1} - Call allowed, no wait required: {wait_seconds}")

