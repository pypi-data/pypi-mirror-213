# printbuddies

A few utilities to do terminal printing tricks. <br>
Install with:
<pre>pip install printbuddies</pre>

Contains two classes and three functions: ProgBar, Spinner, print_in_place, ticker, and clear.<br>

### ProgBar

ProgBar is a self-incrementing, dynamically sized progress bar.<br>
The progress counter and completion values can be manually overriden if desired.<br>
The width of the progress bar is set according to a ratio of the terminal width
so it will be resized automatically if the terminal width is changed.<br>

<pre>
from printbuddies import ProgBar
total = 100
bar = ProgBar(total=total)
for _ in range(total):
    bar.display()
bar.reset()
my_list = [bar.display(return_object=i) for i in range(total)]
</pre>

The display function has a 'return_object' parameter, allowing ProgBar to be used in comprehensions.
<pre>
bar = ProgBar(10)
def square(x: int | float)->int|float:
    return x * x
myList = [bar.display(return_object=square(i)) for i in range(10)]
{progress bar gets displayed}
print(myList)
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
</pre>

ProgBar also supports being used with a context manager.

### Spinner

This class will print the next character from a sequence every time it's `display` method is called, clearing whatever is currently on the line.<br>
The characters will be cycled through indefinitely.<br>
<pre>
from printbuddies import Spinner
spinner = Spinner()
for _ in range(10):
    spinner.display()
</pre>

The default character sequence can be overridden:
<pre>
spinner = Spinner(sequence=["~_~_~_~_~_~_", "_~_~_~_~_~_~"])
for _ in range(10):
    spinner.display()
</pre>

When used with a context manager, the last character printed will be cleared from the terminal upon exiting.

### print_in_place

'print_in_place' erases the current line in the terminal and then writes the value of 
the 'string' param to the terminal.<br>
<pre>
from printbuddies import print_in_place
import time
#This will print numbers 0-99 to the terminal with each digit overwriting the last.
for i in range(100):
    print_in_place(i)
    time.sleep(0.1)
</pre>

### ticker

'ticker' prints a list of strings to the terminal with empty lines above and below
such that previous text in the terminal is no longer visible.<br>
Visually, It functions as a multi-line version of print_in_place.<br>
<pre>
from printbuddies import ticker
import time
#This will produce visually the same output as the above example
for i in range(100):
    ticker([i])
    time.sleep(0.1)
</pre>

### clear
A call to `printbuddies.clear()` simply clears the current line from the terminal.
