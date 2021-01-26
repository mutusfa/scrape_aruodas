FROM python:3.9


COPY . app
WORKDIR /app
RUN pip install .

VOLUME crawls
VOLUME scraped_data
VOLUME .scrapy

ENTRYPOINT ["scrapy"]
CMD ["crawl", "rent"]

