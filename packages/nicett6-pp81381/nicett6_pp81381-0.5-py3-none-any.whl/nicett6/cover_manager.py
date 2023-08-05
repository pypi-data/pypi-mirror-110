import logging
from nicett6.connection import TT6Connection, TT6Writer, TT6Reader
from nicett6.cover import Cover, TT6Cover, wait_for_motion_to_complete
from nicett6.decode import PctPosResponse
from nicett6.ttbus_device import TTBusDeviceAddress

_LOGGER = logging.getLogger(__name__)


class CoverManager:
    def __init__(self, serial_port: str):
        self._serial_port = serial_port
        self._message_tracker_reader: TT6Reader = None
        self._writer: TT6Writer = None
        self._tt6_covers = {}

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, exception_type, exception_value, traceback):
        await self.close()

    async def open(self):
        self._conn = TT6Connection()
        await self._conn.open(self._serial_port)
        # NOTE: reader is created here rather than in self.message_tracker
        # to ensure that all messages from this moment on are captured
        self._message_tracker_reader: TT6Reader = self._conn.add_reader()
        self._writer = self._conn.get_writer()
        await self._writer.send_web_on()

    async def close(self):
        self._conn.close()
        self._conn = None
        self._message_tracker_reader = None
        self._writer = None
        await self.remove_covers()

    async def message_tracker(self):
        _LOGGER.debug("message_tracker started")
        async for msg in self._message_tracker_reader:
            _LOGGER.debug(f"msg:{msg}")
            if isinstance(msg, PctPosResponse):
                if msg.tt_addr in self._tt6_covers:
                    tt6_cover = self._tt6_covers[msg.tt_addr]
                    await tt6_cover.cover.set_drop_pct(msg.pct_pos / 1000.0)
        _LOGGER.debug("message tracker finished")

    async def add_cover(self, tt_addr: TTBusDeviceAddress, cover: Cover):
        tt6_cover = TT6Cover(tt_addr, cover, self._writer)
        await tt6_cover.send_pos_request()
        tt6_cover.enable_notifier()
        self._tt6_covers[tt_addr] = tt6_cover
        return tt6_cover

    async def remove_covers(self):
        for tt6_cover in self._tt6_covers.values():
            await tt6_cover.disable_notifier()
        self._tt6_covers = {}

    async def wait_for_motion_to_complete(self):
        return await wait_for_motion_to_complete(
            [tt6_cover.cover for tt6_cover in self._tt6_covers.values()]
        )
