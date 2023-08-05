from typing import TypeVar, Union, Generic, Optional

from nanoid import generate
from ebbe import format_repr
from functools import partial
from ural import get_domain_name

from minet.web import Response
from minet.serialization import serialize_error_as_slug

CrawlJobDataType = TypeVar("CrawlJobDataType")
CrawlResultDataType = TypeVar("CrawlResultDataType")


class CrawlTarget(Generic[CrawlJobDataType]):
    """
    This class represent a crawl target, i.e. at least a URL, and should be
    used by end-users when they need to specify what they want to crawl more
    precisely (i.e. if they need to switch spiders, have a custom depth or
    rely on some necessary data that will be passed along).
    """

    __slots__ = ("url", "depth", "spider", "data")

    url: str
    depth: Optional[int]
    spider: Optional[str]
    data: Optional[CrawlJobDataType]

    def __init__(
        self,
        url: str,
        depth: Optional[int] = None,
        spider: Optional[str] = None,
        data: Optional[CrawlJobDataType] = None,
    ) -> None:
        if not isinstance(url, str):
            raise TypeError("url should be a string")

        self.url = url

        if depth is not None and not isinstance(depth, int):
            raise TypeError("depth should be an int")

        self.depth = depth

        if spider is not None and not isinstance(spider, str):
            raise TypeError("spider should be a string")

        self.spider = spider
        self.data = data

    def __eq__(self, other):
        return (
            self.url == other.url
            and self.depth == other.depth
            and self.spider == other.spider
            and self.data == other.data
        )

    def __repr__(self):
        return format_repr(self, conditionals=("spider", "data", "depth"))


UrlOrCrawlTarget = Union[str, CrawlTarget[CrawlJobDataType]]


generate_crawl_job_id = partial(
    generate,
    alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
    size=12,
)


class CrawlJob(Generic[CrawlJobDataType]):
    """
    This class represents an actual job that will be queued by the crawler. It
    should not be created by users themselves as they are inferred from
    a CrawlTarget instead.

    This class should be pickle-safe as it will be serialized by persistent
    queues.
    """

    __slots__ = (
        "id",
        "url",
        "depth",
        "spider",
        "data",
        "attempts",
        "parent",
        "__has_cached_domain",
        "__domain",
    )

    id: str
    url: str
    depth: int
    spider: Optional[str]
    data: Optional[CrawlJobDataType]
    attempts: int
    parent: Optional[str]

    # TODO: we should add headers, cookies and such here in the future

    __has_cached_domain: bool
    __domain: Optional[str]

    def __init__(
        self,
        url: str,
        depth: Optional[int] = None,
        spider: Optional[str] = None,
        data: Optional[CrawlJobDataType] = None,
        parent: Optional[str] = None,
    ):
        self.id = generate_crawl_job_id()
        self.url = url
        self.depth = depth if depth is not None else 0
        self.spider = spider
        self.data = data
        self.attempts = 0
        self.parent = parent

        self.__has_cached_domain = False
        self.__domain = None

    def __hash__(self) -> int:
        return hash(self.id)

    def __getstate__(self):
        return (
            self.id,
            self.url,
            self.depth,
            self.spider,
            self.data,
            self.attempts,
            self.parent,
        )

    def __setstate__(self, state):
        (
            self.id,
            self.url,
            self.depth,
            self.spider,
            self.data,
            self.attempts,
            self.parent,
        ) = state

        self.__has_cached_domain = False
        self.__domain = None

    @property
    def domain(self) -> Optional[str]:
        if self.__has_cached_domain:
            return self.__domain

        if self.url is not None:
            self.__domain = get_domain_name(self.url)

        self.__has_cached_domain = True

        return self.__domain

    def __repr__(self):
        return format_repr(self, conditionals=("data", "spider", "parent"))


class CrawlResult(Generic[CrawlJobDataType, CrawlResultDataType]):
    __slots__ = ("job", "data", "error", "response", "degree")

    FIELDNAMES = [
        "id",
        "parent",
        "spider",
        "depth",
        "url",
        "resolved_url",
        "error",
        "status",
        "degree",
        "body_size",
    ]

    job: CrawlJob[CrawlJobDataType]
    data: Optional[CrawlResultDataType]
    error: Optional[Exception]
    response: Optional[Response]
    degree: int

    def __init__(self, job: CrawlJob[CrawlJobDataType]):
        self.job = job
        self.data = None
        self.error = None
        self.response = None
        self.degree = 0

    @property
    def url(self) -> str:
        return self.job.url

    @property
    def depth(self) -> int:
        return self.job.depth

    @property
    def spider(self) -> Optional[str]:
        return self.job.spider

    @property
    def error_code(self) -> Optional[str]:
        return serialize_error_as_slug(self.error) if self.error else None

    def as_csv_row(self):
        job = self.job

        return [
            job.id,
            job.parent,
            job.spider,
            job.depth,
            job.url,
            self.response.end_url if self.response else None,
            self.error_code,
            self.response.status if self.response else None,
            self.degree,
            len(self.response) if self.response else None,
        ]

    def __repr__(self) -> str:
        return format_repr(
            self,
            attributes=(
                (
                    "url",
                    "depth",
                    "spider",
                    ("error", self.error_code),
                    ("status", self.response.status if self.response else None),
                    "degree",
                    (
                        "dtype",
                        type(self.data).__name__ if self.data is not None else None,
                    ),
                    ("size", self.response.human_size if self.response else None),
                )
            ),
            conditionals=("spider", "error", "status", "degree", "dtype"),
        )


class ErroredCrawlResult(CrawlResult[CrawlJobDataType, None]):
    job: CrawlJob[CrawlJobDataType]
    data: None
    error: Exception
    response: Optional[Response]
    degree: int

    def __init__(
        self,
        job: CrawlJob[CrawlJobDataType],
        error: Exception,
        response: Optional[Response] = None,
    ):
        self.job = job
        self.data = None
        self.error = error
        self.response = response
        self.degree = 0

    @property
    def error_code(self) -> str:
        return serialize_error_as_slug(self.error)


class SuccessfulCrawlResult(CrawlResult[CrawlJobDataType, CrawlResultDataType]):
    job: CrawlJob[CrawlJobDataType]
    data: CrawlResultDataType
    error: None
    response: Response
    degree: int

    def __init__(
        self,
        job: CrawlJob[CrawlJobDataType],
        response: Response,
        data: CrawlResultDataType,
        degree: int,
    ):
        self.job = job
        self.data = data
        self.error = None
        self.response = response
        self.degree = degree

    @property
    def error_code(self) -> None:
        return None


AnyCrawlResult = Union[
    ErroredCrawlResult[CrawlJobDataType],
    SuccessfulCrawlResult[CrawlJobDataType, CrawlResultDataType],
]
