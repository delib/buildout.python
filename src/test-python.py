def test(options, buildout):
    from subprocess import Popen, PIPE
    import os
    import sys

    python = options['python']
    if not os.path.exists(python):
        raise IOError("There is no file at %s" % python)
    if sys.platform == 'darwin':
        output = Popen([python, "-c", "import platform; print (platform.mac_ver())"], stdout=PIPE).communicate()[0]
        if not output.startswith("('10."):
            raise IOError("Your python at %s doesn't return proper data for platform.mac_ver(), got: %s" % (python, output))
    elif sys.platform == 'linux2' and (2, 4) <= sys.version_info < (2, 5):
        output = Popen([python, "-c", "import socket; print (hasattr(socket, 'ssl'))"], stdout=PIPE).communicate()[0]
        if not output.startswith("True"):
            raise IOError("Your python at %s doesn't have ssl support, got: %s" % (python, output))

    output = Popen([python, "-c", "import readline; print (readline)"], stdout=PIPE).communicate()[0]
    # The leading escape sequence is sometimes printed by readline on import (see https://bugs.python.org/msg191824)
    if not output.lstrip("\x1b[?1034h").startswith("<module"):
        raise IOError("Your python at %s doesn't have readline support, got: %s" % (python,output))
