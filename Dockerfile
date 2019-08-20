FROM fedora:25

LABEL maintainer="vlussenburg@xebialabs.com"

RUN dnf -y install procps net-tools pcre pcre-static python && \
    dnf clean all 
RUN pip install --upgrade pip==10.0.1
RUN pip install flask==1.0.2
RUN mkdir /app

ENV FLASK_APP=/app/job.py
ENV FLASK_ENV=development

COPY job.py /app/

EXPOSE 5000

CMD flask run --host=0.0.0.0