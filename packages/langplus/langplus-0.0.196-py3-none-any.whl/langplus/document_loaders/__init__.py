"""All different types of document loaders."""

from langplus.document_loaders.airbyte_json import AirbyteJSONLoader
from langplus.document_loaders.airtable import AirtableLoader
from langplus.document_loaders.apify_dataset import ApifyDatasetLoader
from langplus.document_loaders.arxiv import ArxivLoader
from langplus.document_loaders.azlyrics import AZLyricsLoader
from langplus.document_loaders.azure_blob_storage_container import (
    AzureBlobStorageContainerLoader,
)
from langplus.document_loaders.azure_blob_storage_file import (
    AzureBlobStorageFileLoader,
)
from langplus.document_loaders.bibtex import BibtexLoader
from langplus.document_loaders.bigquery import BigQueryLoader
from langplus.document_loaders.bilibili import BiliBiliLoader
from langplus.document_loaders.blackboard import BlackboardLoader
from langplus.document_loaders.blockchain import BlockchainDocumentLoader
from langplus.document_loaders.chatgpt import ChatGPTLoader
from langplus.document_loaders.college_confidential import CollegeConfidentialLoader
from langplus.document_loaders.confluence import ConfluenceLoader
from langplus.document_loaders.conllu import CoNLLULoader
from langplus.document_loaders.csv_loader import CSVLoader, UnstructuredCSVLoader
from langplus.document_loaders.dataframe import DataFrameLoader
from langplus.document_loaders.diffbot import DiffbotLoader
from langplus.document_loaders.directory import DirectoryLoader
from langplus.document_loaders.discord import DiscordChatLoader
from langplus.document_loaders.docugami import DocugamiLoader
from langplus.document_loaders.duckdb_loader import DuckDBLoader
from langplus.document_loaders.email import (
    OutlookMessageLoader,
    UnstructuredEmailLoader,
)
from langplus.document_loaders.epub import UnstructuredEPubLoader
from langplus.document_loaders.evernote import EverNoteLoader
from langplus.document_loaders.excel import UnstructuredExcelLoader
from langplus.document_loaders.facebook_chat import FacebookChatLoader
from langplus.document_loaders.fauna import FaunaLoader
from langplus.document_loaders.figma import FigmaFileLoader
from langplus.document_loaders.gcs_directory import GCSDirectoryLoader
from langplus.document_loaders.gcs_file import GCSFileLoader
from langplus.document_loaders.git import GitLoader
from langplus.document_loaders.gitbook import GitbookLoader
from langplus.document_loaders.github import GitHubIssuesLoader
from langplus.document_loaders.googledrive import GoogleDriveLoader
from langplus.document_loaders.gutenberg import GutenbergLoader
from langplus.document_loaders.hn import HNLoader
from langplus.document_loaders.html import UnstructuredHTMLLoader
from langplus.document_loaders.html_bs import BSHTMLLoader
from langplus.document_loaders.hugging_face_dataset import HuggingFaceDatasetLoader
from langplus.document_loaders.ifixit import IFixitLoader
from langplus.document_loaders.image import UnstructuredImageLoader
from langplus.document_loaders.image_captions import ImageCaptionLoader
from langplus.document_loaders.imsdb import IMSDbLoader
from langplus.document_loaders.iugu import IuguLoader
from langplus.document_loaders.joplin import JoplinLoader
from langplus.document_loaders.json_loader import JSONLoader
from langplus.document_loaders.markdown import UnstructuredMarkdownLoader
from langplus.document_loaders.mastodon import MastodonTootsLoader
from langplus.document_loaders.max_compute import MaxComputeLoader
from langplus.document_loaders.mediawikidump import MWDumpLoader
from langplus.document_loaders.modern_treasury import ModernTreasuryLoader
from langplus.document_loaders.notebook import NotebookLoader
from langplus.document_loaders.notion import NotionDirectoryLoader
from langplus.document_loaders.notiondb import NotionDBLoader
from langplus.document_loaders.obsidian import ObsidianLoader
from langplus.document_loaders.odt import UnstructuredODTLoader
from langplus.document_loaders.onedrive import OneDriveLoader
from langplus.document_loaders.onedrive_file import OneDriveFileLoader
from langplus.document_loaders.pdf import (
    MathpixPDFLoader,
    OnlinePDFLoader,
    PDFMinerLoader,
    PDFMinerPDFasHTMLLoader,
    PDFPlumberLoader,
    PyMuPDFLoader,
    PyPDFDirectoryLoader,
    PyPDFium2Loader,
    PyPDFLoader,
    UnstructuredPDFLoader,
)
from langplus.document_loaders.powerpoint import UnstructuredPowerPointLoader
from langplus.document_loaders.psychic import PsychicLoader
from langplus.document_loaders.pyspark_dataframe import PySparkDataFrameLoader
from langplus.document_loaders.python import PythonLoader
from langplus.document_loaders.readthedocs import ReadTheDocsLoader
from langplus.document_loaders.reddit import RedditPostsLoader
from langplus.document_loaders.roam import RoamLoader
from langplus.document_loaders.rtf import UnstructuredRTFLoader
from langplus.document_loaders.s3_directory import S3DirectoryLoader
from langplus.document_loaders.s3_file import S3FileLoader
from langplus.document_loaders.sitemap import SitemapLoader
from langplus.document_loaders.slack_directory import SlackDirectoryLoader
from langplus.document_loaders.snowflake_loader import SnowflakeLoader
from langplus.document_loaders.spreedly import SpreedlyLoader
from langplus.document_loaders.srt import SRTLoader
from langplus.document_loaders.stripe import StripeLoader
from langplus.document_loaders.telegram import (
    TelegramChatApiLoader,
    TelegramChatFileLoader,
)
from langplus.document_loaders.text import TextLoader
from langplus.document_loaders.tomarkdown import ToMarkdownLoader
from langplus.document_loaders.toml import TomlLoader
from langplus.document_loaders.trello import TrelloLoader
from langplus.document_loaders.twitter import TwitterTweetLoader
from langplus.document_loaders.unstructured import (
    UnstructuredAPIFileIOLoader,
    UnstructuredAPIFileLoader,
    UnstructuredFileIOLoader,
    UnstructuredFileLoader,
)
from langplus.document_loaders.url import UnstructuredURLLoader
from langplus.document_loaders.url_playwright import PlaywrightURLLoader
from langplus.document_loaders.url_selenium import SeleniumURLLoader
from langplus.document_loaders.weather import WeatherDataLoader
from langplus.document_loaders.web_base import WebBaseLoader
from langplus.document_loaders.whatsapp_chat import WhatsAppChatLoader
from langplus.document_loaders.wikipedia import WikipediaLoader
from langplus.document_loaders.word_document import (
    Docx2txtLoader,
    UnstructuredWordDocumentLoader,
)
from langplus.document_loaders.xml import UnstructuredXMLLoader
from langplus.document_loaders.youtube import (
    GoogleApiClient,
    GoogleApiYoutubeLoader,
    YoutubeLoader,
)

# Legacy: only for backwards compat. Use PyPDFLoader instead
PagedPDFSplitter = PyPDFLoader

# For backwards compatability
TelegramChatLoader = TelegramChatFileLoader

__all__ = [
    "AZLyricsLoader",
    "AirbyteJSONLoader",
    "AirtableLoader",
    "ApifyDatasetLoader",
    "ArxivLoader",
    "AzureBlobStorageContainerLoader",
    "AzureBlobStorageFileLoader",
    "BSHTMLLoader",
    "BibtexLoader",
    "BigQueryLoader",
    "BiliBiliLoader",
    "BlackboardLoader",
    "BlockchainDocumentLoader",
    "CSVLoader",
    "ChatGPTLoader",
    "CoNLLULoader",
    "CollegeConfidentialLoader",
    "ConfluenceLoader",
    "DataFrameLoader",
    "DiffbotLoader",
    "DirectoryLoader",
    "DiscordChatLoader",
    "DocugamiLoader",
    "Docx2txtLoader",
    "DuckDBLoader",
    "FaunaLoader",
    "EverNoteLoader",
    "FacebookChatLoader",
    "FigmaFileLoader",
    "GCSDirectoryLoader",
    "GCSFileLoader",
    "GitHubIssuesLoader",
    "GitLoader",
    "GitbookLoader",
    "GoogleApiClient",
    "GoogleApiYoutubeLoader",
    "GoogleDriveLoader",
    "GutenbergLoader",
    "HNLoader",
    "HuggingFaceDatasetLoader",
    "HuggingFaceDatasetLoader",
    "IFixitLoader",
    "IMSDbLoader",
    "ImageCaptionLoader",
    "IuguLoader",
    "JSONLoader",
    "JoplinLoader",
    "MWDumpLoader",
    "MastodonTootsLoader",
    "MathpixPDFLoader",
    "MaxComputeLoader",
    "ModernTreasuryLoader",
    "NotebookLoader",
    "NotionDBLoader",
    "NotionDirectoryLoader",
    "ObsidianLoader",
    "OneDriveLoader",
    "OneDriveFileLoader",
    "OnlinePDFLoader",
    "OutlookMessageLoader",
    "PDFMinerLoader",
    "PDFMinerPDFasHTMLLoader",
    "PDFPlumberLoader",
    "PagedPDFSplitter",
    "PlaywrightURLLoader",
    "PsychicLoader",
    "PyMuPDFLoader",
    "PyPDFDirectoryLoader",
    "PyPDFLoader",
    "PyPDFium2Loader",
    "PySparkDataFrameLoader",
    "PythonLoader",
    "ReadTheDocsLoader",
    "RedditPostsLoader",
    "RoamLoader",
    "S3DirectoryLoader",
    "S3FileLoader",
    "SRTLoader",
    "SeleniumURLLoader",
    "SitemapLoader",
    "SlackDirectoryLoader",
    "SpreedlyLoader",
    "StripeLoader",
    "TelegramChatApiLoader",
    "TelegramChatFileLoader",
    "TelegramChatLoader",
    "TextLoader",
    "ToMarkdownLoader",
    "TomlLoader",
    "TrelloLoader",
    "TwitterTweetLoader",
    "UnstructuredAPIFileIOLoader",
    "UnstructuredAPIFileLoader",
    "UnstructuredCSVLoader",
    "UnstructuredEPubLoader",
    "UnstructuredEmailLoader",
    "UnstructuredExcelLoader",
    "UnstructuredFileIOLoader",
    "UnstructuredFileLoader",
    "UnstructuredHTMLLoader",
    "UnstructuredImageLoader",
    "UnstructuredMarkdownLoader",
    "UnstructuredODTLoader",
    "UnstructuredPDFLoader",
    "UnstructuredPowerPointLoader",
    "UnstructuredRTFLoader",
    "UnstructuredURLLoader",
    "UnstructuredWordDocumentLoader",
    "UnstructuredXMLLoader",
    "WeatherDataLoader",
    "WebBaseLoader",
    "WhatsAppChatLoader",
    "WikipediaLoader",
    "YoutubeLoader",
    "SnowflakeLoader",
]
