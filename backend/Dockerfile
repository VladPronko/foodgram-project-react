FROM python:3.7-slim

WORKDIR /app
# COPY requirements.txt ./
# RUN pip3 install -r ./requirements.txt --no-cache-dir
COPY . .
RUN pip install -r requirements.txt
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000

# CMD ["python", "-m", "gunicorn", "--bind", ":8000", "--workers", "1", "foodproject.wsgi"]
# CMD ["gunicorn", "foodproject.wsgi:application", "--bind", "0:8000" ]

