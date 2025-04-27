FROM python:3.10-slim

WORKDIR /workspace

RUN apt-get update && apt-get install -y \
    unzip \
    bash \
    wget \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install pandas numpy tqdm pyarrow scikit-learn matplotlib seaborn yfinance

ENV SPARK_VERSION=3.4.1
ENV HADOOP_VERSION=3

RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xvzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH
ENV PYTHONPATH=$SPARK_HOME/python/:$SPARK_HOME/python/build:$PYTHONPATH
ENV PYSPARK_PYTHON=python3

COPY . .

CMD ["bash"]

