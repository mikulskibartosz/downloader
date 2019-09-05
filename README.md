# Development environment setup

1. Install conda

2. Run the following commands:

```
conda create --name fandom python=3.7.4
conda activate fandom
conda install --file requirements.txt
```

# Running tests

Run the `pytest scrapers/*` command in the root directory of the project.

# How to download hot topics

Run: `python download_hot_topics.py` in the command line

The downloaded data will be stored in the `hot_topics.csv` file.

# Scheduling the script

I have prepared an Airflow configuration file (file: airflow_dag/download_hot_topics_dag.py) which runs the download_hot_topics.py script on a daily basis. The changes required to make it production-ready are described in the "How to make it production-ready" section of this README file.

# Running with Airflow in Docker

1. Build the docker image using the following command (in the project's root directory): `docker build -t fandom:latest .`

2. Run the docker image: `docker run --rm -p 8080:8080 fandom:latest`

3. Open `localhost:8080` in the browser.

4. Enable the `download_hot_topics` DAG.

5. Wait until the DAG finishes.

6. Copy the output file from the docker container: `docker cp $(docker ps -aqf "ancestor=fandom:latest"):/script_output/hot_topics.csv hot_topics.csv`

7. Stop the container.

# How to make it production-ready

##  Change the output destination to an external storage

Instead of writing to a local file located on one of the Airflow workers, we should store the output in a location which can be accessed by subsequent Airflow tasks. It can be done by, for example, writing to an S3 bucket/a database or sending the file content to a message queue.

## Use Airflow cluster instead of a dockerized Airflow

Running Airflow as a cluster allows to benefit from making the change described in the next paragraph.

##  Download topics from multiple websites at the same time

Instead of running all Scrapy spiders in the same file, we can split them into multiple scripts (one spider per script) and run every one of them as a separate Airflow task.

Additionally, the spider configuration (page addresses) can be split (so every Airflow task downloads a subset of addresses) to parallelize scraping a single source.

Obviously, in this case, we have to use external shared storage instead of a CSV file because every task will run on a different Airflow worker.

## Monitoring

Assuming that the script runs in Airflow, we can use the built-in monitoring mechanism. It not only sends emails when a task fails but can also trigger a restart of the task in case of a failure. 

Airflow deals with the errors that cause the script to fail, but the monitoring in Airflow will not catch a "business error".
Such errors occur when the HTML structure of the source changes, and we end up with an empty or invalid file.

Such situations can be detected by implementing a `StatsCollector` in Scrapy (https://docs.scrapy.org/en/latest/topics/stats.html) which sends the number of downloaded items to InfluxDB (or any other storage) + setting up a dashboard in Grafana. We can configure alerts in Grafana to send a notification (as an email or a message in a Slack channel) when the number of collected items differs from the expected value.

To make the notifications even more useful, the Scrapy Spiders can be extended by an "Item pipeline" (https://docs.scrapy.org/en/latest/topics/item-pipeline.html#price-validation-and-dropping-items-with-no-prices) which can validate the extracted content and drop invalid values. Such discarded elements will raise an alert in Grafana because there are not enough items in the output.

## Adding more sources

If more sources (or more URLs from an existing source) are needed, the configuration can be loaded from a database at runtime instead of hardcoding the values in the script.

## Decide what to do with duplicates

For example, `CAPCOM GO! Apollo VR Planetarium` game is both simulation and free to play, so it is listed twice with two different categories. Similarly, `Zombieland: Double Tap` movie is both a comedy and an action movie.

In my opinion, merging categories is not the responsibility of the scraper and should be done later in the data pipeline.