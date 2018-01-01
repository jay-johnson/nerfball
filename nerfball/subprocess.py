import os


if os.getenv("NERF_SUBPROCESS_CALL", "1") == "1":
    def call(*popenargs, timeout=None, **kwargs):
        print(("subprocess - call popen args={} kwargs={}")
              .format(popenargs,
                      kwargs))
        return 0
# end of call
