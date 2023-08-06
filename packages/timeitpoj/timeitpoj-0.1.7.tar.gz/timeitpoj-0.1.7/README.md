# Timeitpoj

yet another random library for measuring python performance

## Usage in production

if you do not need to measure performance of your code in a production environment, simply set the environment
variable `TIME_IT` to`false`

#### Example

```python
from timeitpoj.timeit import TimeIt
from time import sleep

BASE_TIME = 0.1

with TimeIt("my timer") as timer:
    print("Executing my timer....")
    sleep(BASE_TIME)

    with timer("my subtimer"):
        print("Executing my subtimer....")
        sleep(BASE_TIME)

        with timer("my nested subtimer"):
            print("Executing my nested subtimer....")
            sleep(BASE_TIME)

            for _ in range(2):
                with timer("my super nested subtimer 2"):
                    sleep(BASE_TIME)

        for _ in range(5):
            with timer("my nested subtimer 2"):
                sleep(BASE_TIME)

    with timer("my subtimer 992"):
        print("Executing my subtimer 2....")
        sleep(BASE_TIME)

    with timer("my subtimer 4"):
        print("Executing my subtimer 4....")
        sleep(BASE_TIME)

    # Something that is not covered by the timer
    sleep(BASE_TIME * 2)
```

#### Output

```
================= [my timer] TIMEIT REPORT =================
[TIMEIT] my timer took 1.403 seconds
└── [81.80%] my subtimer ; 0.902 seconds
    ├── [37.49%] my nested subtimer ; 0.300 seconds
        └── my super nested subtimer 2 ; 0.200 seconds ; 2 times ; avg 0.100 seconds
    └── [62.51%] my nested subtimer 2 ; 0.501 seconds ; 5 times ; avg 0.100 seconds
├── [ 9.12%] my subtimer 992 ; 0.101 seconds
└── [ 9.08%] my subtimer 4   ; 0.100 seconds
└── [ 0.01%] internal time: 0.112 milliseconds
[78.56%% COVERAGE] time accounted for: 1.102 seconds, time unaccounted for: 0.301 seconds
[TIMEIT] report generation took 0.190 milliseconds
================= [my timer] TIMEIT REPORT =================
```