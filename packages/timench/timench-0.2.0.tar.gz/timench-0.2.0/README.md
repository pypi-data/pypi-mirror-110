# Timench
**Timench** is a small framework for measure execution time of one function, multiple functions and some code with context 

## Internal variables
Timench has three internal dicts:
- Timench.funcs = {case_name: func} - for storage funcs for measurement by case name
- Timench.times = {case_name: [time1, time2, ]} - for storage measurement time (as list) by case name
- Timench.reports = {case_name: 'report'} for storage for measurement reports (as string) by case name

## Usage
### 1. Time measurement of single function run
For example let's try to measure run time of time.sleep() function
```python
tmnch = Timench()
case_name = 'sleep_1sec'
tmnch.add_func(case_name, time.sleep)  # Add function with case name to benchmark list
```
Now we can set args for time.sleep(*args) and run benchmark
```python
repeats = 10  # Count of repeats
sleep_time = 1.0  # args of time.sleep(sleep_time)
tmnch.run(case_name, repeats, sleep_time)  # Run benchmark
print(tmnch.get_report(case_name))  # Print benchmark report
```
and write report to txt-file
```python
tmnch.write_reports('example_1_report.txt')
```

### 2. Time measurement of multiple functions run. 

My favorite way of Timench usage is compare execution time of different code with same features. Here is basic setup of example:
```python
import time

from timench import Timench

tmnch = Timench()
repeats = 10
env_args = {  # dict structure: {case_name: [args, kwargs] of function func(*args, **kwargs), }
    'sleep_1s': [[1.0, ], None],
    'sleep_2s': [[2.0, ], None],
    'sleep_3s': [[3.0, ], None]
}

for case_name in env_args:  # # Add functions to benchmark list
    tmnch.add_func(case_name, time.sleep)
```
Run all benchmarks:
```python
tmnch.multiple_run(repeats, env_args)   # Run multiple benchmarks
```
Output reports to terminal and txt-file:
```python
for case_name in env_args:
    print(tmnch.get_report(case_name))  # Print to terminal all reports

tmnch.write_reports('example_2_report.txt')  # Write all reports to txt-file
```

### 3. Context usage
Sometimes we need to know execution times of code without function creation and benchmark setup.

Let's look to simple example:
```python
import time

from timench import Timench

with Timench():  # Just wrap your code with Timench
    time.sleep(1.0)
```

## Full examples

### Example 1. Time measurement of function single run
```python
import time

from timench import Timench

tmnch = Timench()
case_name = 'sleep_1sec'  # Set run case name
repeats = 10  # Count of repeats
sleep_time = 1.0  # args of time.sleep(sleep_time)

tmnch.add_func(case_name, time.sleep)  # Add function to benchmark list

tmnch.run(case_name, repeats, sleep_time)  # Run benchmark
print(tmnch.get_report(case_name))  # Print benchmark report

tmnch.write_reports('example_1_report.txt')  # Write all reports to txt-file
```
Output example:
```
Case: sleep_1sec
---
Function: sleep
Total time = 10.0128 sec
Best loop time = 1.00024 sec
Average loop time = 1.00128 sec
Repeats = 10
```

### Example 2. Time measurement of multiple functions run
```python
import time

from timench import Timench

tmnch = Timench()
repeats = 10
env_args = {  # dict structure: {case_name: [args, kwargs] of function func(*args, **kwargs), }
    'sleep_1s': [[1.0, ], None],
    'sleep_2s': [[2.0, ], None],
    'sleep_3s': [[3.0, ], None]
}

for case_name in env_args:  # # Add functions to benchmark list
    tmnch.add_func(case_name, time.sleep)

tmnch.multiple_run(repeats, env_args)  # Run multiple benchmarks

for case_name in env_args:
    print(tmnch.get_report(case_name))  # Print to terminal all reports

tmnch.write_reports('example_2_report.txt')  # Write all reports to txt-file
```
Output example:
```
Case: sleep_1s
---
Function: sleep
Total time = 10.1691 sec
Best loop time = 1.00017 sec
Average loop time = 1.01691 sec
Repeats = 10

Case: sleep_2s
---
Function: sleep
Total time = 20.0776 sec
Best loop time = 2.00185 sec
Average loop time = 2.00776 sec
Repeats = 10

Case: sleep_3s
---
Function: sleep
Total time = 30.0205 sec
Best loop time = 3.00012 sec
Average loop time = 3.00205 sec
Repeats = 10
```
### Example 3. Time measurement with context execution
```python
import time

from timench import Timench

with Timench():  # Run time measurement for some code
    time.sleep(1.0)
    time.sleep(2.0)
    time.sleep(3.0)
```
Output example:
```
Run time = 6.00682 sec
```