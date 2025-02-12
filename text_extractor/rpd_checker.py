import time
import datetime

def rpd_checker(RATE_LIMIT_RPD, MINIMUM_WAIT_SECONDS):
    """
    Checks if a new call can be made, prioritizing immediate calls (respecting min wait)
    until the daily rate limit (RPD) is reached, then enforces waiting until next day.

    Args:
        RATE_LIMIT_RPD: The rate limit in rounds per day (RPD).
        MINIMUM_WAIT_SECONDS: The minimum time in seconds that must elapse between consecutive calls.

    Returns:
        float: 0 if a new call can be made immediately, otherwise the number of seconds to wait.
    """
    if not hasattr(rpd_checker, 'last_call_time'):
        rpd_checker.last_call_time = None
    if not hasattr(rpd_checker, 'call_timestamps_day'):
        rpd_checker.call_timestamps_day = []

    current_time = time.time()
    last_call_time = rpd_checker.last_call_time

    min_time = 0
    rpd_time = 0


    # 1. Enforce Minimum Wait
    if last_call_time is not None:
        elapsed_since_last_call = current_time - last_call_time
        if elapsed_since_last_call < MINIMUM_WAIT_SECONDS:
            wait_time_min = MINIMUM_WAIT_SECONDS - elapsed_since_last_call
            min_time = wait_time_min

    # 2. Daily Rate Limit Check: Count calls in the current day (UTC)
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    start_of_day_utc = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_day_timestamp_utc = start_of_day_utc.timestamp()

    rpd_checker.call_timestamps_day = [
        ts for ts in rpd_checker.call_timestamps_day if ts >= start_of_day_timestamp_utc
    ]

    if RATE_LIMIT_RPD == 0 or len(rpd_checker.call_timestamps_day) < RATE_LIMIT_RPD:
        # Call is allowed, update timestamps
        rpd_checker.last_call_time = current_time
        rpd_checker.call_timestamps_day.append(current_time)
        rpd_time = 0.0
    else:
        # Daily rate limit reached, calculate wait time until the start of the next day (UTC)
        next_day_utc = start_of_day_utc + datetime.timedelta(days=1)
        wait_time_daily = (next_day_utc.timestamp()) - current_time
        if wait_time_daily < 0:
            wait_time_daily = 0.0 # Ensure wait time is not negative
        rpd_time = wait_time_daily

    return max(min_time, rpd_time)

def test_rpd():
    """
    Tests the rpd_checker function by simulating multiple calls with various rates and times.
    """
    
    # Example Usage (Daily Rate Limit with Minimum Wait)
    RATE_LIMIT_RPD = 5  # Example: 50 calls per day
    MINIMUM_WAIT_SECONDS = 0.5 # Example: 0.5 seconds minimum wait

    print("--- Daily Rate Limit Test - Within Rate Limit ---")
    for i in range(40): # Calls well within daily rate limit
        wait_seconds = rpd_checker(RATE_LIMIT_RPD, MINIMUM_WAIT_SECONDS)
        if wait_seconds > 0:
            print(f"Call {i+1} - No call wait: {wait_seconds}")
            time.sleep(wait_seconds)
        else:
            print(f"Call {i+1} - Call allowed, no wait required: {wait_seconds}")

    print("\n--- Daily Rate Limit Test - Exceeding Rate Limit ---")
    for i in range(20): # Calls exceeding daily rate limit, should start waiting until next day
        wait_seconds = rpd_checker(RATE_LIMIT_RPD, MINIMUM_WAIT_SECONDS)
        if wait_seconds > 0:
            print(f"Call {40+i+1} - No call wait: {wait_seconds} seconds (wait until next day)")
            time.sleep(wait_seconds)
        else:
            print(f"Call {40+i+1} - Call allowed, no wait required: {wait_seconds}")

    print("\n--- Daily Rate Limit Minimum Wait Test (faster than min wait) ---")
    for i in range(5): # Calls faster than minimum wait, minimum wait should be enforced
        wait_seconds = rpd_checker(RATE_LIMIT_RPD, MINIMUM_WAIT_SECONDS)
        if wait_seconds > 0:
            print(f"Call {60+i+1} - No call wait: {wait_seconds}")
            time.sleep(wait_seconds)
        else:
            print(f"Call {60+i+1} - Call allowed, no wait required: {wait_seconds}")

# test_rpd()