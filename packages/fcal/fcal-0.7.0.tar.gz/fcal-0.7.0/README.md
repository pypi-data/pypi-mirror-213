## Installation

```
pip install fcal
```

## Usage

```sh
# Print the last 10 days in the default format
fcal -b 10

# Print the last 10 days in MM-DD format 
fcal -b 10 -f '%m-%d'

# Print the last 10 days and next 10 days in local datetime format %c  
fcal -b 10 -a 10 -f '%c'
```
