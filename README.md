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

## What to personalize before submitting

1. Actually complete 5–10 hours of study and record the time spent.
2. Understand the scripts and change the dataset, metrics, charting, tests, or failure rules so the final submission demonstrates **your** decisions and unique work.
3. Push to a GitHub repository you own and verify the workflow finishes successfully. Capture a real screenshot of the Actions run.
4. Replace any bracketed text in your assignment write-up with your real experience and verified repo URL. Do not claim Docker/GitHub Actions were run if you only ran the local Python tests.

### Suggested learning resources
- Instructor's video: https://www.youtube.com/watch?v=ioTsICXbI0Y
- GitHub Actions Python tutorial: https://docs.github.com/en/actions/tutorials/build-and-test-code/python
- Docker Python guide: https://docs.docker.com/guides/python/
