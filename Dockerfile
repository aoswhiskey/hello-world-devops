FROM python:3.13-alpine

WORKDIR /app

RUN addgroup -S app && adduser -S -G app app

COPY --chown=app:app app.py /app/app.py

USER app
EXPOSE 32777

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:32777/healthz', timeout=2)"

CMD ["python", "app.py"]
