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

# How to download hot topics

Run: `python download_hot_topics.py` in the command line

The downloaded data will be stored in the `hot_topics.csv` file.

# Scheduling the script

I have prepeared an Airflow script (file: airflow_dag/download_hot_topics_dag.py) which runs the download_hot_topics.py script on a daily basis. The changes required to make it production-ready are described in the "How to make it production ready" section.

# Running with Airflow in Docker

1. Build the docker image using the following command (in the project's root director): `docker build -t fandom:latest .`

2. Run the docker image: `docker run --rm -p 8080:8080 fandom:latest`

3. Open `localhost:8080` in the browser.

4. Enable the `download_hot_topics` DAG.

5. Wait unitl the DAG finishes.

6. Copy the output file from the docker container: `docker cp $(docker ps -aqf "ancestor=fandom:latest"):/script_output/hot_topics.csv hot_topics.csv`

7. Stop the container.

# How to make it production ready

##  Change the output destination to an external storage

Instead of writing to a local file located on one of the Airflow workers, we should store the output in a location which can be accessed by subsequent Airflow tasks, for example a S3 bucket or a database, or send the file content to a message queue.

## Use Airflow cluster instead of a dockerized Airflow

This allows to benefit from making the change described in the next paragraph.

##  Download topics from multiple websites at the same time

Instead of running all Scrapy spiders in the same file, we can split them into multiple scripts (one spider per script) and run every one of them as a separate Airflow task. Additionally, the spider configuration (page addresses) can be splitted (so every Airflow task downloads a subset of addresses) to pararelize scraping a single source.

Obviously, in this case, we have to use an external shared storage instead of a csv file because every task will run on a different Airflow worker.
