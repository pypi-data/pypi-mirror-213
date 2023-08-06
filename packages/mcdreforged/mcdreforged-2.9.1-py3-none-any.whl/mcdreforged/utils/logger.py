"""
Custom logger for MCDR
"""
import logging
import os
import sys
import time
import weakref
import zipfile
from contextlib import contextmanager
from enum import Enum, unique, auto
from threading import RLock, local
from typing import Dict, Optional, List, Set

from colorlog import ColoredFormatter

from mcdreforged.constants import core_constant
from mcdreforged.minecraft.rtext.style import RColor, RStyle, RItemClassic
from mcdreforged.utils import string_util, file_util


@unique
class DebugOption(Enum):
	# remember to sync with the debug field in the default config file
	ALL = auto()
	MCDR = auto()
	HANDLER = auto()
	REACTOR = auto()
	PLUGIN = auto()
	PERMISSION = auto()
	COMMAND = auto()
	TASK_EXECUTOR = auto()


class SyncStdoutStreamHandler(logging.StreamHandler):
	__write_lock = RLock()
	__instance_lock = RLock()
	__instances = weakref.WeakSet()  # type: Set[SyncStdoutStreamHandler]

	def __init__(self):
		super().__init__(sys.stdout)
		with self.__instance_lock:
			self.__instances.add(self)

	def emit(self, record) -> None:
		with self.__write_lock:
			super().emit(record)

	@classmethod
	def update_stdout(cls, stream=None):
		if stream is None:
			stream = sys.stdout
		with cls.__instance_lock:
			instances = list(cls.__instances)
		for inst in instances:
			inst.acquire()  # use Handler's lock
			try:
				inst.stream = stream
			finally:
				inst.release()


class MCColorFormatControl:
	MC_CODE_ITEMS: List[RItemClassic] = list(filter(lambda item: isinstance(item, RItemClassic), list(RColor) + list(RStyle)))

	# global flag
	console_color_disabled = False

	__TLS = local()

	@classmethod
	@contextmanager
	def disable_minecraft_color_code_transform(cls):
		cls.__set_mc_code_trans_disable(True)
		try:
			yield
		finally:
			cls.__set_mc_code_trans_disable(False)

	@classmethod
	def __is_mc_code_trans_disabled(cls) -> bool:
		try:
			return cls.__TLS.mc_code_trans
		except AttributeError:
			cls.__set_mc_code_trans_disable(False)
			return False

	@classmethod
	def __set_mc_code_trans_disable(cls, state: bool):
		cls.__TLS.mc_code_trans = state

	def _modify_message_text(self, text: str) -> str:
		if not self.__is_mc_code_trans_disabled():
			# minecraft code -> console code
			for item in self.MC_CODE_ITEMS:
				if item.mc_code in text:
					text = text.replace(item.mc_code, item.console_code)
			# clean the rest of minecraft codes
			text = string_util.clean_minecraft_color_code(text)
		if self.console_color_disabled:
			text = string_util.clean_console_color_code(text)
		return text


class MCDReforgedFormatter(ColoredFormatter, MCColorFormatControl):
	def formatMessage(self, record):
		text = super().formatMessage(record)
		return self._modify_message_text(text)


class ServerOutputFormatter(logging.Formatter, MCColorFormatControl):
	def formatMessage(self, record):
		text = super().formatMessage(record)
		return self._modify_message_text(text)


class NoColorFormatter(logging.Formatter):
	def formatMessage(self, record):
		return string_util.clean_console_color_code(super().formatMessage(record))


class MCDReforgedLogger(logging.Logger):
	DEFAULT_NAME = core_constant.NAME_SHORT
	LOG_COLORS = {
		'DEBUG': 'blue',
		'INFO': 'green',
		'WARNING': 'yellow',
		'ERROR': 'red',
		'CRITICAL': 'bold_red',
	}
	SECONDARY_LOG_COLORS = {
		'message': {
			'WARNING': 'yellow',
			'ERROR': 'red',
			'CRITICAL': 'red'
		}
	}

	@property
	def __file_formatter(self):
		# it's not necessary to try to consider self.__plugin_id here
		# since the only FileHandler to be created is the in logger of the mcdr_server
		# which doesn't have the plugin id thing
		# for loggers for plugins, see mcdreforged.plugin.server_interface.ServerInterface._get_logger
		return NoColorFormatter(
			f'[%(name)s] [%(asctime)s] [%(threadName)s/%(levelname)s]: %(message)s',
			datefmt='%Y-%m-%d %H:%M:%S'
		)

	@property
	def __console_formatter(self):
		extra = '' if self.__plugin_id is None else ' [{}]'.format(self.__plugin_id)
		return MCDReforgedFormatter(
			f'[%(name)s] [%(asctime)s] [%(threadName)s/%(log_color)s%(levelname)s%(reset)s]{extra}: %(message_log_color)s%(message)s%(reset)s',
			log_colors=self.LOG_COLORS,
			secondary_log_colors=self.SECONDARY_LOG_COLORS,
			datefmt='%H:%M:%S'
		)

	debug_options = {}  # type: Dict[DebugOption, bool]

	def __init__(self, plugin_id: Optional[str] = None):
		super().__init__(self.DEFAULT_NAME)
		self.file_handler: Optional[logging.FileHandler] = None
		self.__plugin_id = plugin_id

		self.console_handler = SyncStdoutStreamHandler()
		self.console_handler.setFormatter(self.__console_formatter)

		self.addHandler(self.console_handler)
		self.setLevel(logging.DEBUG)

	def set_debug_options(self, debug_options: Dict[str, bool]):
		for key, value in debug_options.items():
			option = DebugOption[key.upper()]
			MCDReforgedLogger.debug_options[option] = value
		for option, value in MCDReforgedLogger.debug_options.items():
			self.debug('Debug option {} is set to {}'.format(option, value), option=option)

	@classmethod
	def should_log_debug(cls, option: Optional[DebugOption] = None):
		do_log = cls.debug_options.get(DebugOption.ALL, False)
		if option is not None:
			do_log |= cls.debug_options.get(option, False)
		return do_log

	def debug(self, *args, option: Optional[DebugOption] = None, no_check: bool = False):
		if no_check or self.should_log_debug(option):
			with MCColorFormatControl.disable_minecraft_color_code_transform():
				super().debug(*args)

	def set_file(self, file_name: str):
		if self.file_handler is not None:
			self.removeHandler(self.file_handler)
		file_util.touch_directory(os.path.dirname(file_name))
		if os.path.isfile(file_name):
			modify_time = time.strftime('%Y-%m-%d', time.localtime(os.stat(file_name).st_mtime))
			counter = 0
			while True:
				counter += 1
				zip_file_name = '{}/{}-{}.zip'.format(os.path.dirname(file_name), modify_time, counter)
				if not os.path.isfile(zip_file_name):
					break
			zipf = zipfile.ZipFile(zip_file_name, 'w')
			zipf.write(file_name, arcname=os.path.basename(file_name), compress_type=zipfile.ZIP_DEFLATED)
			zipf.close()
			os.remove(file_name)
		self.file_handler = logging.FileHandler(file_name, encoding='utf8')
		self.file_handler.setFormatter(self.__file_formatter)
		self.addHandler(self.file_handler)

	def unset_file(self):
		if self.file_handler is not None:
			self.removeHandler(self.file_handler)
			self.file_handler.close()
			self.file_handler = None


class ServerOutputLogger(logging.Logger):
	server_fmt = ServerOutputFormatter('[%(name)s] %(message)s')

	def __init__(self, name):
		super().__init__(name)

		console_handler = SyncStdoutStreamHandler()
		console_handler.setFormatter(self.server_fmt)

		self.addHandler(console_handler)
		self.setLevel(logging.DEBUG)
