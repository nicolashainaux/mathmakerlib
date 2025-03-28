#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2006-2017 Nicolas Hainaux <nh.techn@gmail.com>

# This file is part of Mathmakerlib.

# Mathmakerlib is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# Mathmakerlib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Mathmakerlib; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import sys

import polib
from exitstatus import ExitStatus

from mathmakerlib import shared

LOCALE_PATH = shared.LOCALEDIR
POT_FILE_PATH = LOCALE_PATH / 'mathmakerlib.pot'
UPDATES_PATH = LOCALE_PATH / 'mathmakerlib_updates.pot'

# EXIT WITH SUCCESS IF UPDATES HAVE BEEN FOUND AND WRITTEN;
# WITH FAILURE OTHERWISE


def main():
    sys.stdout.write("[merge_py_updates_to_main_pot_file] Starting...\n")
    if not os.path.isfile(UPDATES_PATH):
        sys.stderr.write("UPDATES_PATH=" + str(UPDATES_PATH) + "\n"
                         + "No updates file found. Exiting.")
        sys.exit(1)

    main_pot_file = polib.pofile(POT_FILE_PATH)
    updates_file = polib.pofile(UPDATES_PATH)
    main_pot_file_msgids = [entry.msgid for entry in main_pot_file]
    updates_file_msgids = [entry.msgid for entry in updates_file]
    something_changed = False

    # First, remove the msgids present in the old file and absent from
    # the new one; remove the obsolete occurrences in main file entries,
    # if necessary
    to_delete = []
    for main_entry in main_pot_file:
        if main_entry.msgid in updates_file_msgids:
            for updates_entry in updates_file:
                if updates_entry.msgid == main_entry.msgid:
                    o_to_delete = []
                    for o in main_entry.occurrences:
                        if (o not in updates_entry.occurrences
                            and not o[0].endswith('.xml')
                            and not o[0].endswith('.yaml')):
                            o_to_delete.append(o)
                            something_changed = True
                    for o in o_to_delete:
                        sys.stderr.write("Deleting this occurrence: "
                                         + str(o) + " from this entry: "
                                         + str(main_entry.msgid) + "\n")
                        del main_entry.occurrences[
                            main_entry.occurrences.index(o)]

        else:  # This entry is absent from the update, so...
            # either there is no .xml occurrence, then remove the entry
            ext_list = [o[0][-3:] for o in main_entry.occurrences]
            if all(ext == ".py" for ext in ext_list):
                to_delete.append(main_entry)
                something_changed = True
            # Or there is at least one .xml occurence, then remove all
            # .py occurrences.
            else:
                o_to_delete = []
                for o in main_entry.occurrences:
                    if o[0][-3] == ".py":
                        o_to_delete.append(o)
                        something_changed = True
                for o in o_to_delete:
                    sys.stderr.write("Deleting this occurrence: "
                                     + str(o) + " from this entry: "
                                     + str(main_entry.msgid) + "\n")
                    del main_entry.occurrences[main_entry.occurrences.index(o)]

    for entry in to_delete:
        sys.stderr.write("Removing this entry: " + str(entry) + "\n")
        del main_pot_file[main_pot_file.index(entry)]

    # Now, add new msgids and new occurrences of preexisting msgdis
    # in main_pot_file:
    for updates_entry in updates_file:
        if updates_entry.msgid in main_pot_file_msgids:
            for main_entry in main_pot_file:
                if updates_entry.msgid == main_entry.msgid:
                    for ref in updates_entry.occurrences:
                        if ref not in main_entry.occurrences:
                            sys.stderr.write("Merging this entry: \n"
                                             + str(updates_entry) + "\n")
                            main_entry.merge(updates_entry)
                            main_entry.occurrences = list(
                                set(main_entry.occurrences))
                            something_changed = True
                            break

        else:  # This entry is absent from the main pot file, so add it
            sys.stderr.write("Adding new entry: \n"
                             + str(updates_entry) + "\n")
            main_pot_file.append(updates_entry)
            something_changed = True

    if something_changed:
        sys.stderr.write("Writing changes to " + str(POT_FILE_PATH) + "\n")
        main_pot_file.save(POT_FILE_PATH)
    else:
        sys.stderr.write("No changes to save. " + str(POT_FILE_PATH)
                         + " remains unchanged.\n")

    sys.stdout.write("[merge_py_updates_to_main_pot_file] Done.\n\n")

    if something_changed:
        sys.exit(ExitStatus.success)
    else:
        sys.exit(ExitStatus.failure)


if __name__ == '__main__':
    main()
