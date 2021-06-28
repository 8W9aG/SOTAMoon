"""The class used for providing files on distributed bittorrent systems."""
import typing
import time
import logging
import os

import libtorrent as lt

from .provider import Provider
from .file_provider import file_path_for_file_hash
from ..network.node import Node


DHT_ROUTERS = [
    "router.utorrent.com",
    "router.bittorrent.com",
    "dht.transmissionbt.com",
    "router.bitcomet.com",
    "dht.aelitis.com",
]
BITTORRENT_STATES = [
    "QUEUED",
    "CHECKING",
    "DOWNLOADING METADATA",
    "DOWNLOADING",
    "FINISHED",
    "SEEDING",
    "ALLOCATING"
]


class BitTorrentProvider(Provider):
    """The class for providing files via BitTorrent."""
    def __init__(self, torrent_folder: str, resolved_folder: str):
        super().__init__("bittorrent", resolved_folder)
        self.torrent_folder = torrent_folder
        self.ses = lt.session()
        self.ses.listen_on(6881, 6891)
        for dht_router in DHT_ROUTERS:
            self.ses.add_dht_router(dht_router, 6881)
        self.ses.start_dht()
        with open(os.path.join(os.path.dirname(__file__), "trackers.txt"), "r") as trackers_txt_handle:
            self.trackers = [x.strip() for x in trackers_txt_handle.readlines() if x]
        os.makedirs(self.torrent_folder, exist_ok = True)
        os.makedirs(self.cache_folder, exist_ok = True)

    def path(self, file_hash: str, link: str = None, skip_check: bool = False) -> typing.Optional[str]:
        """Find the path of the file hash."""
        file_path = file_path_for_file_hash(file_hash, self.cache_folder)
        if file_path is not None:
            return file_path
        if link is None:
            return None
        handle = lt.add_magnet_uri(self.ses, link, {
            'save_path': self.cache_folder,
            'storage_mode': lt.storage_mode_t(2),
        })
        for tracker in self.trackers:
            handle.add_tracker({
                "url": tracker,
                "tier": 1
            })
        logging.info(f"Downloading metadata for link: {link}")
        while not handle.has_metadata():
            logging.info(f"Downloading metadata for link: {link}")
            time.sleep(5)
        logging.info(f"Downloaded metadata for link: {link}")
        if len(handle.get_torrent_info().files()) == 1 or skip_check:
            while handle.status().state != lt.torrent_status.seeding:
                s = handle.status()
                logging.info(f"{(s.progress * 100.0):.2f} complete (down: {(s.download_rate / 1000.0):.1f} kb/s up: {(s.upload_rate / 1000.0):.1f} kB/s peers: {s.num_peers}) {BITTORRENT_STATES[s.state]} {(s.total_download / 1000000.0):.1f}")
                time.sleep(1)
            if not skip_check:
                file_path = file_path_for_file_hash(file_hash, self.cache_folder)
                if file_path is not None:
                    return file_path
            else:
                return None
        self.ses.remove_torrent(handle)
        return None

    def distribute(self, file_hash: str) -> typing.Optional[str]:
        """Distribute the file to other nodes via BT."""
        fs = lt.file_storage()
        file_path = os.path.join(self.cache_folder, file_hash)
        if not os.path.exists(file_path):
            logging.error(f"Could not distribute file: {file_hash}")
            return None
        lt.add_files(fs, file_path_for_file_hash(file_hash, self.cache_folder))
        t = lt.create_torrent(fs)
        # Only add 1 tracker here so we get a consistent BTIH
        t.add_tracker("udp://tracker.openbittorrent.com:6969/announce", 0)
        t.set_creator(f"sotamoon")
        t.set_comment(file_hash)
        lt.set_piece_hashes(t, file_path)
        torrent = t.generate()
        torrent_file = os.path.join(self.torrent_folder, file_hash + ".torrent")
        with open(torrent_file, "wb") as f:
            f.write(lt.bencode(torrent))
        torrent_info = lt.torrent_info(torrent_file)
        self.ses.add_torrent({
            'ti': torrent_info,
            'save_path': self.cache_folder,
        })
        return lt.make_magnet_uri(torrent_info)

    def write(self, file_name: str, content: bytes) -> typing.Optional[str]:
        """Writes contents to a file hash."""
        return None

    def copy(self, file_path: str) -> typing.Optional[str]:
        """Copy file to the cache."""
        return None

    def nodes(self, port: int) -> typing.Set[Node]:
        """Report all the nodes the provider is connected to."""
        nodes = set()
        for torrent in self.ses.get_torrents():
            for peer_info in torrent.get_peer_info():
                ip_address, _ = peer_info.ip
                nodes.add(Node(ip_address, port))
        return nodes
