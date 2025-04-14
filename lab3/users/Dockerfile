FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["uvicorn", "users.users_service:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]