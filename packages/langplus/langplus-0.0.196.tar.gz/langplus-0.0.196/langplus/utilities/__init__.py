"""General utilities."""
from langplus.requests import TextRequestsWrapper
from langplus.utilities.apify import ApifyWrapper
from langplus.utilities.arxiv import ArxivAPIWrapper
from langplus.utilities.awslambda import LambdaWrapper
from langplus.utilities.bash import BashProcess
from langplus.utilities.bing_search import BingSearchAPIWrapper
from langplus.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langplus.utilities.google_places_api import GooglePlacesAPIWrapper
from langplus.utilities.google_search import GoogleSearchAPIWrapper
from langplus.utilities.google_serper import GoogleSerperAPIWrapper
from langplus.utilities.graphql import GraphQLAPIWrapper
from langplus.utilities.metaphor_search import MetaphorSearchAPIWrapper
from langplus.utilities.openweathermap import OpenWeatherMapAPIWrapper
from langplus.utilities.powerbi import PowerBIDataset
from langplus.utilities.pupmed import PubMedAPIWrapper
from langplus.utilities.python import PythonREPL
from langplus.utilities.searx_search import SearxSearchWrapper
from langplus.utilities.serpapi import SerpAPIWrapper
from langplus.utilities.spark_sql import SparkSQL
from langplus.utilities.twilio import TwilioAPIWrapper
from langplus.utilities.wikipedia import WikipediaAPIWrapper
from langplus.utilities.wolfram_alpha import WolframAlphaAPIWrapper

__all__ = [
    "ApifyWrapper",
    "ArxivAPIWrapper",
    "PubMedAPIWrapper",
    "BashProcess",
    "BingSearchAPIWrapper",
    "DuckDuckGoSearchAPIWrapper",
    "GooglePlacesAPIWrapper",
    "GoogleSearchAPIWrapper",
    "GoogleSerperAPIWrapper",
    "GraphQLAPIWrapper",
    "LambdaWrapper",
    "MetaphorSearchAPIWrapper",
    "OpenWeatherMapAPIWrapper",
    "PowerBIDataset",
    "PythonREPL",
    "SearxSearchWrapper",
    "SerpAPIWrapper",
    "SparkSQL",
    "TextRequestsWrapper",
    "TwilioAPIWrapper",
    "WikipediaAPIWrapper",
    "WolframAlphaAPIWrapper",
]
