#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.conf import settings

def initialize_debugger():
    import debugpy
    
    # optionally check to see what env you're running in, you probably only want this for 
    # local development, for example: if os.getenv("MY_ENV") == "dev":

    # RUN_MAIN envvar is set by the reloader to indicate that this is the 
    # actual thread running Django. This code is in the parent process and
    # initializes the debugger
    if not os.getenv("RUN_MAIN") and settings.DEBUG:
        debugpy.listen(("0.0.0.0", 3000))
        sys.stdout.write("Debugpy started at 0.0.0.0:3000\n")
        #sys.stdout.write("Start the VS Code debugger now, waiting...\n")
        #debugpy.wait_for_client()
        #sys.stdout.write("Debugger attached, starting server...\n")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    initialize_debugger()  # add this

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

