# Capstone Analytics Validation Pipeline

A small, original *starter* project for learning GitHub Actions, Docker, and automated quality checks. The **input is entirely synthetic**; no real users or financial records are included.

## What makes it different from a tutorial?

The implementation validates gameplay-session records *before* calculating six custom dashboard KPIs, including player repeat rate and completion rate by mode. It deliberately blocks duplicate session IDs, blank player IDs, malformed status values, negative figures, and empty datasets. This is a use-case-specific analytics pipeline, not a copied GitHub Actions example.

## Run locally (Python 3.10+)

```bash
python -m unittest discover -s tests -v
python -m src.app --input data/synthetic_sessions.csv --output output/dashboard.html
```

Open `output/dashboard.html` in a browser to view the standalone dashboard.

## Try a deliberate failure

Make a copy of `data/synthetic_sessions.csv`, repeat a `session_id`, and run `python -m src.app --input path/to/changed.csv`. The command should stop with `DATA QUALITY FAILURE`. Restore the valid file afterward.

## Run with Docker (requires local Docker installation)

```bash
docker build -t capstone-analytics-demo .
docker run --rm -v "$(pwd)/output:/project/output" capstone-analytics-demo
```

In GitHub Actions, the workflow runs tests, produces an HTML report, builds the Docker image, runs the container, then uploads the HTML dashboard as a downloadable workflow artifact.

