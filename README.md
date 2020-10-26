# SDS Project

Data Science project for UE19CS203: Statistics for Data Science.

## Index

-   [Getting Started](#getting-started)
-   [Prerequisites](#prerequisites)
-   [Installing](#installing)
-   [Disclaimer](#disclaimer)

## Getting Started

Clone the repository into your system, by typing the following in your terminal:

```
git clone https://github.com/LaRuim/SDS-Project.git
```

## Prerequisites

-   Python 3.x

## Installing

To install all Python dependencies, run the following command in your terminal:

```
pip3 install -r requirements.txt
```

The given dataset is raw and is unsegregated. To obtain the appropriate datasets and clean them, navigate to [scripts/cleaning](https://github.com/LaRuim/SDS-Project/tree/master/scripts/cleaning) and run the following commands in your terminal:

```
python3 split.py
python3 clean.py
```

## Disclaimer

Note: Attributes beginning with 'power' or 'mentality' are rated of of 20, whereas the rest are rated out of 100.\
Note: clean.py takes a long time to run.