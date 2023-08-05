import pytest
import responses
from pyrchive import ArchiveSesh

# Sample HTML content for mocking the response
sample_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <input type="hidden" name="submitid" value="test_submit_id" />
</body>
</html>
"""


@responses.activate
def test_fetch_submit_id():
    responses.add(
        responses.GET,
        "https://archive.is",
        body=sample_html,
        status=200,
        content_type="text/html",
    )

    archive_sesh = ArchiveSesh()
    assert archive_sesh.submit_id == "test_submit_id"


@responses.activate
def test_archive_url():
    responses.add(
        responses.GET,
        "https://archive.is",
        body=sample_html,
        status=200,
        content_type="text/html",
    )

    responses.add(
        responses.GET,
        "https://archive.is/submit/?submitid=test_submit_id&url=https%3A%2F%2Fwww.example.com",
        status=200,
        content_type="text/html",
    )

    archive_sesh = ArchiveSesh()
    archive_url = archive_sesh.archive_url("https://www.example.com")
    assert archive_url == "https://archive.is/submit/?submitid=test_submit_id&url=https%3A//www.example.com"
