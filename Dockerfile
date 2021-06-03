FROM scrapinghub/scrapinghub-stack-scrapy:2.5
ENV TERM xterm
ENV SCRAPY_SETTINGS_MODULE gencrawl.settings
RUN mkdir -p /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get install -y google-chrome-stable -y
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -y
RUN apt install ./google-chrome-stable_current_amd64.deb -y
COPY . /app
RUN python setup.py install
