# Development environment setup

1. Install conda

2. Run the following commands:

```
conda create --name fandom python=3.7.4
conda activate fandom
conda install --file requirements.txt
```

# Running tests

Run the `pytest scrappers/*` command in the root directory of the project.

# How to run the crowler

Run: `python download_hot_topics.py` in the command line

The downloaded data will be stored in the `hot_topics.csv` file.


# How to make it production ready

TODO

# Scale up - add more sources