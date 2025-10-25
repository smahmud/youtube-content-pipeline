install:
    pip install -r requirements.txt

dev:
    pip install -r requirements.txt -r requirements-dev.txt

lock:
    pip freeze > requirements.lock.txt

test:
    pytest tests/

clean:
    find . -type f -name "*.py[co]" -delete
    rm -rf __pycache__ .pytest_cache
