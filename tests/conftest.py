import os

# Ensure Qt uses an offscreen platform so tests can run in headless environments
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
