from setuptools import setup

setup(
    # Metadata
    name="bischoff_and_ratcliff_1995",
    version="0.1.0",
    description="Instance generator, as described in the paper of Bischoff and Ratcliff (1995)",
    url="https://github.com/lucasguesserts/bischoff-and-ratcliff-1995",
    author="Lucas Guesser",
    author_email="lucasguesserts@gmail.com",
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],
    keywords=[
        "container loading problem",
        "knapsack problem",
        "single large object placement problem (slopp)",
        "packing problem",
    ],
    # Options
    install_requires=["pytest"],
    python_requires=">=3.0",
    scripts=["bin/generate_all_instances"],
)
