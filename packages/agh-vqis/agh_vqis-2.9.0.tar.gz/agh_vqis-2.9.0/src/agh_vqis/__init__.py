# Authors: Jakub Nawała <jnawala@agh.edu.pl>, Filip Korus <fkorus@student.agh.edu.pl>
# Created: June 1, 2021

import sys

# import functions from __main__ only if '-m' flag is not presented to avoid double imports
if '-m' not in sys.argv:
    from .__main__ import process_single_mm_file, process_folder_w_mm_files, VQIs

__version__ = "2.9.0"
