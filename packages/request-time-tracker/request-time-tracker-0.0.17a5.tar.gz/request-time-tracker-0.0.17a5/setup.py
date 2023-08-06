from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "readme.md").read_text()

setuptools.setup(
    name="request-time-tracker",
    version="0.0.17-a5",
    author="Roman Karpovich",
    author_email="roman@razortheory.com",
    description="Requests time tracker from being captured by proxy (e.g. nginx) till being executed by wsgi handler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/razortheory/request-time-tracker",
    project_urls={
        "Home": "https://github.com/razortheory/request-time-tracker",
        "Bug Tracker": "https://github.com/razortheory/request-time-tracker/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={
        "request_time_tracker": "src/request_time_tracker",
        "request_pressure_tracker": "src/request_pressure_tracker",
    },
    packages=[
        "request_time_tracker",
        "request_time_tracker.notifiers",
        "request_time_tracker.trackers",
        "request_time_tracker.trackers.cache",
        "request_time_tracker.wsgi_django",
        "request_pressure_tracker",
        "request_pressure_tracker.notifiers",
        "request_pressure_tracker.trackers",
        "request_pressure_tracker.wsgi_django",
    ],
    python_requires=">=3.6",
    install_requires=[],
    extras_require={
        'redis': ['redis'],
        'aws': ['boto3'],
        'azure': ['requests'],
    }
)
