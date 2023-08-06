# seating

Sort the order of class functions, properties, and member variables.

## Installation

Install with:

<pre>
pip install seating
</pre>


### Sorting and Priority

* Class variables declared in class body outside of a function
* Dunder methods
* Functions decorated with `property` or corresponding `.setter` and `.deleter` methods
* Class functions

Each of these groups will be sorted alphabetically with respect to themselves.

The only exception is for dunder methods.<br>
They will be sorted alphabetically except that `__init__` will be first.

If you have class contents that are grouped a certain way and you want the groups individually sorted
so that the grouping is maintained, you can use `# Seat` to demarcate the groups.



i.e. if the source is:

<pre>
class MyClass():
    {arbitrary lines of code}
    # Seat
    {more arbitrary code}
    # Seat
    {yet more code}
</pre>

then the three sets of code in brackets will be sorted independently from one another.

## Usage

#### CLI

<pre>
>seat -h
usage: seat [-h] [--start START] [--stop STOP] [-nb] [-o OUTPUT] [-d] file

positional arguments:
  file                  The file to format.

options:
  -h, --help            show this help message and exit
  --start START         Optional line number to start formatting at.
  --stop STOP           Optional line number to stop formatting at.
  -nb, --noblack        Don't format file with Black after sorting.
  -o OUTPUT, --output OUTPUT
                        Write changes to this file, otherwise changes are written back to the original file.
  -d, --dump            Dump ast tree to file instead of doing anything else. For debugging purposes.
</pre>

#### Programmatically

<pre>
from seating import seat
from pathier import Pathier

file = Pathier("somefile.py")
source = file.read_text()
source = seat(source)
file.write_text(source)
</pre>
