FROM puckel/docker-airflow

ARG AIRFLOW_USER_HOME=/usr/local/airflow
ARG SCRIPTS=/scripts
ARG OUTPUT=/script_output
COPY requirements.txt /requirements.txt

USER root
RUN pip install -r /requirements.txt

RUN mkdir ${SCRIPTS} && mkdir ${OUTPUT} && chmod a+w ${OUTPUT}
COPY download_hot_topics.py ${SCRIPTS}
COPY scrapers ${SCRIPTS}/scrapers
COPY airflow_dag/* ${AIRFLOW_USER_HOME}/dags

EXPOSE 8080 5555 8793

USER airflow
WORKDIR ${AIRFLOW_USER_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]