FROM python:3.12-slim
WORKDIR /project
COPY src ./src
COPY data ./data
CMD ["python", "-m", "src.app", "--input", "data/synthetic_sessions.csv", "--output", "output/dashboard.html"]
