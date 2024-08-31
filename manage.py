#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gimnasium.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()





#DEBUG
# !/usr/bin/env python
# import os
# import sys
# import cProfile
# import io
# import pstats
#
#
# def profile(func):
#     def wrapper(*args, **kwargs):
#         profiler = cProfile.Profile()
#         try:
#             return profiler.runcall(func, *args, **kwargs)
#         finally:
#             s = io.StringIO()
#             ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
#             ps.print_stats(20)
#             print(s.getvalue())
#     return wrapper
#
#
# def main():
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gimnasium.settings')
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     profile(execute_from_command_line)(sys.argv)
#
#
# if __name__ == '__main__':
#     main()
