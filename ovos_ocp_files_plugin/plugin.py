import requests
from os.path import isfile
from ovos_plugin_manager.templates.ocp import OCPStreamExtractor
import shutil
import tempfile
from os import makedirs
from os.path import basename, expanduser, isfile, join, dirname
from .api import load as get_metadata
from ovos_plugin_common_play.ocp.status import TrackState, PlaybackType


class OCPFilesMetadataExtractor(OCPStreamExtractor):
    def __init__(self, ocp_settings=None):
        super().__init__(ocp_settings)
        self.settings = self.ocp_settings.get("files", {})

    @property
    def supported_seis(self):
        """
        skills may return results requesting a specific extractor to be used

        plugins should report a StreamExtractorIds (sei) that identifies it can handle certain kinds of requests

        any streams of the format "{sei}//{uri}" can be handled by this plugin
        """
        return ["file"]

    def validate_uri(self, uri):
        """ return True if uri can be handled by this extractor, False otherwise"""
        if uri.startswith("file//"):
            uri = uri.replace("file//", "")
        return uri.startswith("file://") or isfile(expanduser(uri))

    def extract_stream(self, uri, video=True):
        """ return the real uri that can be played by OCP """
        if uri.startswith("file//"):
            uri = uri.replace("file//", "")
        return self.extract_metadata(uri)

    @staticmethod
    def extract_metadata(uri):
        meta = {"uri": uri,
                "title": basename(uri),
                "playback": PlaybackType.AUDIO,
                "status": TrackState.DISAMBIGUATION}

        uri = expanduser(uri.replace("file://", ""))
        m = get_metadata(uri)
        if m.tags:
            if m.tags.get("title"):
                meta["title"] = m.tags.title[0]
            if m.tags.get("album"):
                meta["album"] = m.tags.album[0]

            if m.tags.get("artist"):
                meta["artist"] = m.tags.artist[0]
            elif m.tags.get("composer"):
                meta["artist"] = m.tags.composer[0]

            if m.tags.get("date"):
                meta["date"] = m.tags.date[0]
            if m.tags.get("audiolength"):
                meta["duration"] = m.tags.audiolength[0]
            if m.tags.get("genre"):
                meta["genre"] = m.tags.genre[0]

        if m.pictures:
            try:
                img_path = f"{tempfile.gettempdir()}/{meta['title']}.jpg"
                with open(img_path, "wb") as f:
                    f.write(m.pictures[0].data)
                meta["image"]: img_path
            except:
                pass
        return meta



