import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

import sys
import os

# Point to task4 where app.py lives
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "task4"))

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

from app import app

def test_header_is_present(dash_duo):
    dash_duo.start_server(app)
    header = dash_duo.find_element("h1")
    assert header is not None
    assert "Pink Morsel" in header.text

def test_chart_is_present(dash_duo):
    dash_duo.start_server(app)
    chart = dash_duo.find_element("#sales-chart")
    assert chart is not None

def test_region_picker_is_present(dash_duo):
    dash_duo.start_server(app)
    region_filter = dash_duo.find_element("#region-filter")
    assert region_filter is not None