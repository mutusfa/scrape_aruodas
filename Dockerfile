FROM python:3.9
ARG JOB_NUM=1

COPY . app
WORKDIR /app
RUN pip install .

VOLUME crawls
VOLUME scraped_data
VOLUME .scrapy

ENTRYPOINT ["scrapy"]
CMD ["crawl", "rent", "-s", "JOBDIR=crawls/rent-$JOB_NUM", "-o", "scraped_data/rent.csv"]