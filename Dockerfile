FROM scrapinghub/scrapinghub-stack-scrapy:2.5
ENV TERM xterm
ENV SCRAPY_SETTINGS_MODULE gencrawl.settings
RUN mkdir -p /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
#RUN apt-get install -y google-chrome-stable -y
#RUN apt-get install wget -y
#RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN apt install ./google-chrome-stable_current_amd64.deb -y

# We need wget to set up the PPA and xvfb to have a virtual screen and unzip to install the Chromedriver
#RUN apt-get install -y wget unzip

# Set up the Chrome PPA
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Update the package list and install chrome
RUN apt-get update -y
RUN apt-get install -y google-chrome-stable

# Set up Chromedriver Environment variables
#ENV CHROMEDRIVER_VERSION 2.19
#ENV CHROMEDRIVER_DIR /chromedriver
#RUN mkdir $CHROMEDRIVER_DIR

# Download and install Chromedriver
#RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
#RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR

# Put Chromedriver into the PATH
#ENV PATH $CHROMEDRIVER_DIR:$PATH

COPY . /app
RUN python setup.py install
