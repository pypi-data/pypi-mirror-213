from datetime import datetime


def meter(func, *args, **kwargs):
    print()
    startTime = datetime.now()

    # insert data into schema
    print(f"{func.__name__} Starts at {startTime}")

    print(f"{func.__name__} Returns {str(func(*args))[0:10]}...")

    endTime = datetime.now()

    duration = endTime - startTime

    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    seconds = duration.seconds % 60
    milliseconds = duration.microseconds // 1000

    print(f"{func.__name__} Takes: {hours}h {minutes}m {seconds}s {milliseconds}ms")


