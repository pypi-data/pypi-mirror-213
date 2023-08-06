# Poplar 

This is a simple logging tool for Python. It sets up a logger with a CLI stream handler and a file handler. Output will be sent to both the console and a log file (saved in `./logs/`).

You could easily add this to your project manually, but this is for convenience sake.

## Installation

```bash
pip install -U poplar-logging`
```

## Usage

```python
import poplar

poplar.log.info("Hello, world!")
poplar.save()
```
