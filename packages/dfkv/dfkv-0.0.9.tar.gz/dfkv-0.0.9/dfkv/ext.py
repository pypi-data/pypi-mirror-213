# this is ext utils
from . import dt

now = dt.now
ts = dt.timestamp

if __name__ == "__main__":
    print(now())
    print(now(5))
    print(now(6))
    print(now(99))
    print(ts())