# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import builtins
import colourspace.av.filter.colourspace
import pickle
import pylru

from logging import getLogger

# See: https://docs.python.org/3/library/pickle.html#restricting-globals


class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        safe_builtins = {
            'range',
            'complex',
            'set',
            'frozenset',
            'slice',
        }

        # Only allow safe classes from builtins.
        if module == "builtins" and name in safe_builtins:
            return getattr(builtins, name)
        elif (module == "pylru"):
            return getattr(pylru, name)
        elif (module == "colourspace.av.filter.colourspace"):
            return getattr(colourspace.av.filter.colourspace, name)

        # Forbid everything else.
        raise pickle.UnpicklingError("global '%s.%s' is forbidden" % (module, name))


class Settings:
    def __init__(self, filename, version):
        self._filename = filename
        self._version = version

    def _get_store(self):
        try:
            with open(self._filename, "rb") as f:
                # Load the dict data from the store
                data = RestrictedUnpickler(f).load()

                # If the version is not correct, ignore the contents
                version = data.get("version", None)
                if version != self._version:
                    raise Exception(f"Expected version {self._version}, but got {version}")

                return data
        except:
            getLogger(__name__).warning(
                f"Could not read from settings file {self._filename}", exc_info=True)
            return {
                "version": self._version,
            }

    def get(self, setting, default=None):
        return self._get_store().get(setting, default)

    def set(self, setting, value):
        data = self._get_store()

        # Update the data
        data[setting] = value

        try:
            with open(self._filename, "wb") as f:
                # Save to the file
                pickle.dump(data, f)
        except:
            getLogger(__name__).warning(
                f"Could not write to settings file {self._filename}", exc_info=True)

    def remove(self, setting):
        try:
            with open(self._filename, "rb") as f:
                # Load the dict data from the store
                data = RestrictedUnpickler(f).load()

            if setting in data:
                del data[setting]

                with open(self._filename, "wb") as f:
                    # Save to the file
                    pickle.dump(data, f)
        except:
            getLogger(__name__).warning(
                f"Could not update settings file {self._filename}", exc_info=True)
