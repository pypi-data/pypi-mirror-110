"""Read the latest Real Python tutorials
Usage:
------
    $ realpython [options] [id] [id ...]
List the latest tutorials:
    $ realpython
Read one tutorial:
    $ realpython <id>
    where <id> is the number shown when listing tutorials.
Read the latest tutorial:
    $ realpython 0
Available options are:
    -h, --help         Show this help
    -l, --show-links   Show links in text
Contact:
--------
- https://realpython.com/contact/
More information is available at:
- https://pypi.org/project/realpython-reader/
- https://github.com/realpython/reader
Version:
--------
- realpython-reader v1.0.0
"""
# Standard library imports
import sys
import os

# ai_object_detection imports
import ai_object_detection
from ai_object_detection import ImageProcessor


def main():
  try:
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    opts = [o for o in sys.argv[1:] if o.startswith("-")]

    print("Process ID:", os.getpid())

    # Show help message
    if "-h" in opts or "--help" in opts:
      viewer.show(__doc__)
      return 0

    # Should links be shown in the text
    show_links = "-l" in opts or "--show-links" in opts

    # Get URL from config file
    url_register = ai_object_detection.URL_REGISTER
    print (url_register)

    img_processor = ImageProcessor()
    img_processor.copyImageFiles()

    print ("Finished!")
    sys.exit()
  except (KeyboardInterrupt, SystemExit):
    sys.exit()

if __name__ == "__main__":
  main()
  quit()
  raise SystemExit 
  Thread.exit()
  sys.exit()
