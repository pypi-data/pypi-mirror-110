"""
Abstract base class for scene release databases
"""

import abc

import logging  # isort:skip
_log = logging.getLogger(__name__)


class SceneDbApiBase(abc.ABC):
    """Base class for scene release database APIs"""

    @property
    @abc.abstractmethod
    def name(self):
        """Unique name of the scene release database"""

    @property
    @abc.abstractmethod
    def label(self):
        """User-facing name of the scene release database"""

    async def search(self, query, only_existing_releases=True):
        """
        Search for scene release

        :param SceneQuery query: Search query
        :param bool only_existing_releases: See
            :meth:`~.scene.find.SceneQuery.search`

        :return: :class:`list` of release names as :class:`str`

        :raise RequestError: if the search request fails
        """
        return await query.search(
            self._search,
            only_existing_releases=only_existing_releases,
        )

    @abc.abstractmethod
    async def _search(self, keywords, group=None):
        pass

    @abc.abstractmethod
    async def release_files(self, release_name):
        """
        Map file names to file objects

        What a file object is depends on the subclass implementation.

        :param str release_name: Exact name of the release

        :raise RequestError: if request fails
        """
