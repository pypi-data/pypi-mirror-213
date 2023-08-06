from ctypes import (
    byref, c_bool, c_char, c_char_p, c_double, c_size_t, c_uint64, c_void_p,
    cdll, POINTER
)
from datetime import datetime
import errno
import gc
import logging
import os
from pathlib import Path
import platform
import re
from typing import Any, List, Optional, Union
import warnings

import numpy as np


# Set to diveplane.amalgam so that it uses the 'diveplane' logger config
_logger = logging.getLogger('diveplane.amalgam')


class Amalgam:
    r"""
    A general python direct interface to the Amalgam library.

    This is implemented with ctypes for accessing binary amalgam builds in
    Linux, MacOS and Windows.

    Parameters
    ----------
    library_path : str
        Path to either the amalgam DLL, DyLib or SO (Windows, MacOS or
        Linux, respectively). If not specified it will search in the
        default location: /<user_home>/.diveplane/lib/dev/amlg/<amalgam.ext>

    gc_interval : int, default None
        If set, garbage collection will be forced at the specified interval
        of amalgam operations. Note that this reduces memory consumption at
        the compromise of performance. Only use if models are exceeding
        your host's process memory limit or if paging to disk. As an
        example, if this operation is set to 0 (force garbage collection
        every operation), it results in a performance impact of 150x.
        Default value does not force garbage collection.

    sbf_datastore_enabled : bool, default False
        If true, sbf tree structures are enabled.

    max_num_threads : int, default 0
        If a multithreaded Amalgam binary is used, sets the maximum number
        of threads to the value specified. If 0, will use the number of
        visible logical cores.

    debug : bool, optional
        Deprecated, use "trace" parameter instead.

    trace: bool, optional
        If true, enables debug output and execution trace.

    execution_trace_file : str, default "execution.trace"
        The full or relative path to the execution trace used in debugging.

    execution_trace_dir : Union[str, None], default None
        A directory path for writing trace files.

    library_postfix : str, optional
        For configuring use of different amalgam builds i.e. -openmp for
        OpenMP build, by default None. Ignored when `library_path`
        is specified.

    Raises
    ------
    FileNotFoundError
        Amalgam library not found in default location, and not configured to
        retrieve automatically.
    """

    def __init__(self, library_path: Optional[str] = None,  # noqa: C901
                 gc_interval: Optional[int] = None,
                 sbf_datastore_enabled: bool = True, max_num_threads: int = 0,
                 debug: Optional[bool] = None, trace: Optional[bool] = None,
                 execution_trace_file: str = "execution.trace",
                 execution_trace_dir: Optional[str] = None,
                 library_postfix: Optional[str] = None, **kwargs):
        self.library_path = library_path

        if debug is not None:
            if trace is None:
                trace = debug
            _logger.warning('The Amalgam "debug" parameter is deprecated '
                            'use "trace" instead.')

        if len(kwargs):
            warnings.warn(f'Unexpected keyword arguments '
                          f'[{", ".join(list(kwargs.keys()))}] '
                          f'passed to Amalgam ''constructor.')

        if trace:
            # Determine where to put the trace files ...
            self.base_execution_trace_file = execution_trace_file
            # default to current directory, and expand relative paths ..
            if execution_trace_dir is None:
                self.execution_trace_dir = Path.cwd()
            else:
                self.execution_trace_dir = Path(execution_trace_dir).expanduser().absolute()
            # Create the trace directory if needed
            if not self.execution_trace_dir.exists():
                self.execution_trace_dir.mkdir(parents=True)

            # increment a counter on the file name, if file already exists..
            self.execution_trace_filepath = Path(self.execution_trace_dir, execution_trace_file)
            counter = 1
            while self.execution_trace_filepath.exists():
                self.execution_trace_filepath = Path(
                    self.execution_trace_dir,
                    f'{self.base_execution_trace_file}.{counter}'
                )
                counter += 1

            self.trace = open(self.execution_trace_filepath, 'w+',
                              encoding='utf-8')
            _logger.debug("Opening Amalgam trace file: " +
                          str(self.execution_trace_filepath))
        else:
            self.trace = None

        operating_system = platform.system().lower()
        if self.library_path is None:
            if operating_system == 'windows':
                # Create a default filepath for Windows
                amalgam_binary = f"Amalgam{library_postfix or ''}.dll"
            elif operating_system == "darwin":
                # Create a default filepath for Darwin
                amalgam_binary = f"amalgam{library_postfix or ''}.dylib"
            else:
                # Create a default filepath for Unix
                amalgam_binary = f"amalgam{library_postfix or ''}.so"

            # Default path for Amalgam binary should be at ~/.diveplane/lib/dev/amlg/
            self.library_path = Path(Path.home(), '.diveplane', 'lib', 'dev', 'amlg', amalgam_binary)
        else:
            self.library_path = Path(library_path)

        _logger.debug("Loading amalgam library: " + str(self.library_path))
        if not self.library_path.exists():
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), str(self.library_path))
        _logger.debug("SBF_DATASTORE enabled: " + str(sbf_datastore_enabled))
        self.amlg = cdll.LoadLibrary(str(self.library_path))
        self.set_amlg_flags(sbf_datastore_enabled)
        self.set_max_num_threads(max_num_threads)
        self.gc_interval = gc_interval
        self.op_count = 0
        self.load_command_log_entry = None

    @property
    def library_postfix(self) -> Union[None, str]:
        """Return the Amalgam library postfix."""
        filename = self.library_path.name
        matches = re.findall(r'-(.+?)\.', filename)
        if len(matches) > 0:
            return f'-{matches[-1]}'
        return None

    def is_sbf_datastore_enabled(self) -> bool:
        """
        Return whether the SBF Datastore is implemented.

        Returns
        -------
        bool
            True if sbf tree structures are currently enabled.
        """
        self.amlg.IsSBFDataStoreEnabled.restype = c_bool
        return self.amlg.IsSBFDataStoreEnabled()

    def set_amlg_flags(self, sbf_datastore_enabled: bool = True) -> None:
        """
        Set various amalgam flags for data structure and compute features.

        Parameters
        ----------
        sbf_datastore_enabled : bool, default True
            If true, sbf tree structures are enabled.
        """
        self.amlg.SetSBFDataStoreEnabled.argtype = [c_bool]
        self.amlg.SetSBFDataStoreEnabled.restype = c_void_p
        self.amlg.SetSBFDataStoreEnabled(sbf_datastore_enabled)

    def set_max_num_threads(self, max_num_threads: int = 0) -> None:
        """
        Set the maximum number of threads.

        Will have no effect if a single-threaded version of Amalgam is used.

        Parameters
        ----------
        max_num_threads : int, default 0
            If a multithreaded Amalgam binary is used, sets the maximum number
            of threads to the value specified. If 0, will use the number of
            visible logical cores.
        """
        self.amlg.SetMaxNumThreads.argtype = [c_size_t]
        self.amlg.SetMaxNumThreads.restype = c_void_p
        self.amlg.SetMaxNumThreads(max_num_threads)

    def reset_trace(self, file: str) -> None:
        """
        Close the open trace file and opens a new one with the specified name.

        Parameters
        ----------
        file : str
            The file name for the new execution trace.
        """
        _logger.debug(f"Execution trace file being reset: "
                      f"{self.execution_trace_filepath} to be closed ...")
        if self.trace is not None:
            # Write exit command.
            self.trace.write("EXIT\n")
            self.trace.close()
        self.execution_trace_filepath = Path(self.execution_trace_dir, file)
        self.trace = open(self.execution_trace_filepath, 'w')
        _logger.debug(f"New trace file: {self.execution_trace_filepath} "
                      f"opened.")
        # Write load command used to instantiate the amalgam instance.
        if self.load_command_log_entry is not None:
            self.trace.write(self.load_command_log_entry + "\n")
        self.trace.flush()

    def __str__(self) -> str:
        """Implement the str() method."""
        return (f"Amalgam Path:\t\t {self.library_path}\n"
                f"Amalgam GC Interval:\t {self.gc_interval}\n")

    def __del__(self) -> None:
        """Implement a "destructor" method to finalize log files, if any."""
        if (
            getattr(self, 'debug', False) and
            getattr(self, 'trace', None) is not None
        ):
            try:
                self.trace.write("EXIT\n")
            except:  # noqa - deliberately broad
                pass

    def _log_comment(self, comment: str) -> None:
        """
        Log a comment into the execution trace file.

        Allows notes of information not captured in the raw execution commands.

        Parameters
        ----------
        reply : str
            The raw reply string to log.
        """
        if self.trace:
            self.trace.write("# NOTE >" + str(comment) + "\n")
            self.trace.flush()

    def _log_reply(self, reply: Any) -> None:
        """
        Log a raw reply from the amalgam process.

        Uses a pre-pended '#RESULT >' so it can be filtered by tools like grep.

        Parameters
        ----------
        reply : Any
            The raw reply string to log.
        """
        if self.trace:
            self.trace.write("# RESULT >" + str(reply) + "\n")
            self.trace.flush()

    def _log_time(self, label: str) -> None:
        """
        Log a labelled timestamp to the tracefile.

        Parameters
        ----------
        label: str
            A string to annotate the timestamped trace entry
        """
        if self.trace:
            dt = datetime.now()
            self.trace.write(f"# TIME {label} {dt:%Y-%m-%d %H:%M:%S},"
                             f"{f'{dt:%f}'[:3]}\n")
            self.trace.flush()

    def _log_execution(self, execution_string: str) -> None:
        """
        Log an execution string.

        Logs an execution string that is sent to the amalgam process for use in
        command line debugging.

        Parameters
        ----------
        execution_string : str
            A formatted string that can be piped into an amalgam command line
            process for use in debugging.

            .. NOTE::
                No formatting checks are performed, it is assumed the exeuction
                string passed is valid.
        """
        if self.trace:
            self.trace.write(execution_string + "\n")
            self.trace.flush()

    def gc(self) -> None:
        """Force garbage collection when called if self.force_gc is set."""
        if (
            self.gc_interval is not None
            and self.op_count > self.gc_interval
        ):
            _logger.debug("Collecting Garbage")
            gc.collect()
            self.op_count = 0
        self.op_count += 1

    def str_to_char_p(self, value: str, size: Optional[int] = None) -> c_char:
        """
        Convert a string to a c++ char pointer.

        Parameters
        ----------
        value : str
            The value of the string.
        size : int or None
            The size of the string. If not provided, the length of the
            string is used.

        Returns
        -------
        c_char
            A c++ char point for the string.
        """
        if isinstance(value, str):
            value = value.encode('utf8')
        buftype = c_char * (size if size is not None else (len(value) + 1))
        buf = buftype()
        buf.value = value
        return buf

    def get_json_from_label(self, handle: str, label: str) -> str:
        """
        Get a label from almalgam and returns it in json format.

        Parameters
        ----------
        handle : str
            The handle of the amalgam entity.
        label : str
            The label to retrieve.

        Returns
        -------
        str
            The json representation of the amalgam label.
        """
        self.amlg.GetJSONPtrFromLabel.restype = c_char_p
        self.amlg.GetJSONPtrFromLabel.argtype = [c_char_p, c_char_p]
        handle_buf = self.str_to_char_p(handle)
        label_buf = self.str_to_char_p(label)
        result = self.amlg.GetJSONPtrFromLabel(handle_buf, label_buf)
        self._log_execution("GET_JSON_FROM_LABEL " + handle + " " + label)
        del handle_buf
        del label_buf
        self.gc()
        return result

    def set_json_to_label(self, handle: str, label: str, json: str) -> None:
        """
        Set a label in amalgam using json.

        Parameters
        ----------
        handle : str
            The handle of the amalgam entity.
        label : str
            The label to set.
        json : str
            The json representation of the label value.
        """
        self.amlg.SetJSONToLabel.restype = c_void_p
        self.amlg.SetJSONToLabel.argtype = [c_char_p, c_char_p, c_char_p]
        handle_buf = self.str_to_char_p(handle)
        label_buf = self.str_to_char_p(label)
        json_buf = self.str_to_char_p(json)
        self._log_execution("SET_JSON_TO_LABEL " + handle +
                            " " + label + " " + json)
        self.amlg.SetJSONToLabel(handle_buf, label_buf, json_buf)
        del handle_buf
        del label_buf
        del json_buf
        self.gc()

    def load_entity(self, handle: str, amlg_path: str, persist: bool = False,
                    load_contained: bool = False, write_log: str = "",
                    print_log: str = "") -> bool:
        """
        Load an entity from an amalgam source file.

        Parameters
        ----------
        handle : str
            The handle to assign the entity.
        amlg_path : str
            The path to the diveplane.amlg/caml file
        persist : bool
            If set to true, all transactions will trigger the entity to be
            saved over the original source.
        load_contained : bool
            If set to true, contained entities will be loaded.
        write_log : str, default ""
            Path to the write log. If empty string, the write log is
            not generated.
        print_log : str, default ""
            Path to the print log. If empty string, the print log is
            not generated.

        Returns
        -------
        bool
            True if the entity was successfully loaded.
        """
        self.amlg.LoadEntity.argtype = [
            c_char_p, c_char_p, c_bool, c_bool, c_char_p, c_char_p]
        self.amlg.LoadEntity.restype = c_bool
        handle_buf = self.str_to_char_p(handle)
        amlg_path_buf = self.str_to_char_p(amlg_path)
        write_log_buf = self.str_to_char_p(write_log)
        print_log_buf = self.str_to_char_p(print_log)

        result = self.amlg.LoadEntity(
            handle_buf, amlg_path_buf, persist, load_contained,
            write_log_buf, print_log_buf)
        self.load_command_log_entry = (
            f"LOAD_ENTITY {handle} {amlg_path} {str(persist).lower()} "
            f"{str(load_contained).lower()} {write_log} {print_log}"
        )
        self._log_execution(self.load_command_log_entry)
        self._log_reply(result)
        del handle_buf
        del amlg_path_buf
        del write_log_buf
        del print_log_buf
        self.gc()
        return result

    def get_entities(self) -> List[str]:
        """
        Get loaded top level entities.

        Returns
        -------
        list of str
            The list of entity handles.
        """
        self.amlg.GetEntities.argtype = [POINTER(c_uint64)]
        self.amlg.GetEntities.restype = POINTER(c_char_p)
        num_entities = c_uint64()
        entities = self.amlg.GetEntities(byref(num_entities))
        result = [entities[i].decode() for i in range(num_entities.value)]
        del entities
        del num_entities
        self.gc()
        return result

    def execute_entity_json(self, handle: str, label: str, json: str) -> str:
        """
        Execute a label with parameters provided in json format.

        Parameters
        ----------
        handle : str
            The handle of the amalgam entity.
        label : str
            The label to execute.
        json : str
            A JSON representation of parameters for the label to be executed.

        Returns
        -------
        str
            A json representation of the response.
        """
        self.amlg.ExecuteEntityJsonPtr.restype = c_char_p
        self.amlg.ExecuteEntityJsonPtr.argtype = [c_char_p, c_char_p,
                                                  c_char_p]
        handle_buf = self.str_to_char_p(handle)
        label_buf = self.str_to_char_p(label)
        json_buf = self.str_to_char_p(json)
        self._log_time("EXECUTION START")
        self._log_execution("EXECUTE_ENTITY_JSON " +
                            handle + " " + label + " " + json)
        result = self.amlg.ExecuteEntityJsonPtr(
            handle_buf, label_buf, json_buf)
        self._log_time("EXECUTION STOP")
        self._log_reply(result)
        del handle_buf
        del label_buf
        del json_buf
        return result

    def set_number_value(self, handle: str, label: str, value: float) -> None:
        """
        Set a numeric value to a label in an amalgam entity.

        Parameters
        ----------
        handle : str
            The handle of the amalgam entity.
        label : str
            The label to set.
        value : float
            A numeric value to assign to a label.
        """
        self.amlg.SetNumberValue.restype = c_void_p
        self.amlg.SetNumberValue.argtype = [c_char_p, c_char_p, c_double]
        handle_buf = self.str_to_char_p(handle)
        label_buf = self.str_to_char_p(label)
        val = c_double(value)
        self.amlg.SetNumberValue(handle_buf, label_buf, val)
        del handle_buf
        del label_buf
        del val
        self.gc()

    def get_number_value(self, handle: str, label: str) -> float:
        """
        Retrieve the numeric value of a label in an amalgam entity.

        Parameters
        ----------
        handle : str
            The handle of the amalgam entity.
        label : str
            The label to execute.

        Returns
        -------
        float
            The numeric value of the label.
        """
        self.amlg.GetNumberValue.restype = c_double
        self.amlg.GetNumberValue.argtype = [c_char_p, c_char_p]
        handle_buf = self.str_to_char_p(handle)
        label_buf = self.str_to_char_p(label)
        result = self.amlg.GetNumberValue(handle_buf, label_buf)
        del handle_buf
        del label_buf
        return result

    # NOTE - Not currently supported by core but may be re-implemented at a
    #        later date.
    # def set_number_matrix(self, handle: str, label: str,
    #                       matrix: Union[np.array, List[List[float]]]) -> None:
    #     """
    #     Set a numeric matrix to a label in an amalgam entity.

    #     Parameters
    #     ----------
    #     handle : str
    #         The handle of the amalgam entity.
    #     label : str
    #         The label to set in the amalgam entity.
    #     matrix : np.array or list of list of float
    #         A 2d matrix of numbers.
    #     """
    #     self.amlg.SetNumberMatrix.restype = c_void_p
    #     self.amlg.SetNumberMatrix.argtype = [
    #         c_char_p, c_char_p, POINTER(c_double), c_size_t, c_size_t]
    #     m = np.array(matrix)
    #     cols = m.shape[0]
    #     rows = m.shape[1]
    #     size = rows * cols
    #     m_as_list = list(m.flatten())
    #     arr = (c_double * size)()
    #     for i in range(size):
    #         arr[i] = m_as_list[i]
    #     handle_buf = self.str_to_char_p(handle)
    #     label_buf = self.str_to_char_p(label)
    #     self.amlg.SetNumberMatrix(handle_buf, label_buf, arr, cols, rows)
    #     del handle_buf
    #     del label_buf

    # NOTE - Not currently supported by core but may be re-implemented at a
    #        later date.
    # def get_number_matrix(self, handle: str, label: str) -> np.array:
    #     """
    #     Retrieve a number matrix from an amalgam entity.

    #     Parameters
    #     ----------
    #     handle : str
    #         The handle of the amalgam entity.
    #     label : str
    #         The label to retrieve.

    #     Returns
    #     -------
    #     np.array
    #         A 2d numpy array of numbers.

    #     """
    #     self.amlg.GetNumberMatrixPtr.restype = POINTER(c_double)
    #     self.amlg.GetNumberMatrixPtr.argtype = [c_char_p, c_char_p]
    #     self.amlg.GetNumberMatrixWidth.restype = c_size_t
    #     self.amlg.GetNumberMatrixWidth.argtype = [c_char_p, c_char_p]
    #     self.amlg.GetNumberMatrixHeight.restype = c_size_t
    #     self.amlg.GetNumberMatrixHeight.argtype = [c_char_p, c_char_p]
    #     handle_buf = self.str_to_char_p(handle)
    #     label_buf = self.str_to_char_p(label)
    #     w = self.amlg.GetNumberMatrixWidth(handle_buf, label_buf)
    #     h = self.amlg.GetNumberMatrixHeight(handle_buf, label_buf)
    #     result = self.amlg.GetNumberMatrixPtr(handle_buf, label_buf)
    #     result = [result[i] for i in range(w * h)]
    #     result = np.reshape(np.array(result), (w, h))
    #     del handle_buf
    #     del label_buf
    #     self.gc()
    #     return result

    def set_string_value(self, handle: str, label: str, value: str) -> None:
        """
        Set a string value to a label in an amalgam entity.

        Parameters
        ----------
        handle : str
            The handle of the amalgam entity.
        label : str
            The label to set.
        value : str
            A string value.
        """
        self.amlg.SetStringValue.restype = c_void_p
        self.amlg.SetStringValue.argtype = [c_char_p, c_char_p, c_char_p]
        handle_buf = self.str_to_char_p(handle)
        label_buf = self.str_to_char_p(label)
        val_buf = self.str_to_char_p(value)
        self.amlg.SetStringValue(handle_buf, label_buf, val_buf)
        del handle_buf
        del label_buf
        del val_buf
        self.gc()

    def get_string_value(self, handle: str, label: str) -> str:
        """
        Retrieve a string value from a label in an amalgam entity.

        Parameters
        ----------
        handle : str
            The handle of the amalgam entity.
        label : str
            The label to retrieve.

        Returns
        -------
        str
            The string value of the label in the amalgam entity.
        """
        self.amlg.GetStringListPtr.restype = POINTER(c_char_p)
        self.amlg.GetStringListPtr.argtype = [c_char_p, c_char_p]
        handle_buf = self.str_to_char_p(handle)
        label_buf = self.str_to_char_p(label)
        result = self.amlg.GetStringListPtr(handle_buf, label_buf)
        del handle_buf
        del label_buf
        self.gc()
        return result[0]

    def set_string_list(self, handle: str, label: str,
                        value: Union[np.array, List[str]]) -> None:
        """
        Set a list of strings to an amalgam entity.

        Parameters
        ----------
        handle : str
            The handle of the amalgam entity.
        label : str
            The label to set.
        value : np.array or list of str
            A 1d list of string values.
        """
        self.amlg.SetStringList.restype = c_void_p
        self.amlg.SetStringList.argtype = [
            c_char_p, c_char_p, POINTER(c_char_p), c_size_t]
        # Convert to std list just in case value passed as a numpy array.
        std_list = np.array(value)
        l_buff = (c_char_p * std_list.shape[0])()
        for i in range(std_list.shape[0]):
            l_buff[i] = c_char_p(std_list[i].encode('utf-8'))
        handle_buf = self.str_to_char_p(handle)
        label_buf = self.str_to_char_p(label)
        self.amlg.SetStringList(handle_buf, label_buf, l_buff,
                                len(std_list))
        del handle_buf
        del label_buf
        self.gc()

    def get_string_list(self, handle: str, label: str) -> np.array:
        """
        Retrieve a list of numbers from a label in an amalgam entity.

        Parameters
        ----------
        handle : str
            The handle of the amalgam entity.
        label : str
            The label to execute.

        Returns
        -------
        np.array
            A 1d list of string values from the label in the amalgam entity.
        """
        self.amlg.GetStringListLength.restype = c_size_t
        self.amlg.GetStringListLength.argtype = [c_char_p, c_char_p]
        self.amlg.GetStringListPtr.restype = POINTER(c_char_p)
        self.amlg.GetStringListPtr.argtype = [c_char_p, c_char_p]
        handle_buf = self.str_to_char_p(handle)
        label_buf = self.str_to_char_p(label)
        size = self.amlg.GetStringListLength(handle_buf, label_buf)
        result = self.amlg.GetStringListPtr(handle_buf, label_buf)
        result = np.array([result[i] for i in range(size)])
        del handle_buf
        del label_buf
        self.gc()
        return result

    def get_version_string(self) -> bytes:
        """
        Get the version string of the amalgam dynamic library.

        Returns
        -------
        bytes
            A version byte-encoded string with major, minor, point version.
            Ex. b'0.0.0'
        """
        self.amlg.GetVersionString.restype = c_char_p
        amlg_version = self.amlg.GetVersionString()
        self._log_comment(f"call to amlg.getVersionSring() - returned: "
                          f"{amlg_version}\n")
        return amlg_version
