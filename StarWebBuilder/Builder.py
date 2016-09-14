import errno
import filecmp
import os
import shutil
import sys
import time
from timeout import timeout
from StarWeb import StarWeb

class Builder(object):
  def __init__(self, network_path, absolute_path, work_dir, env, run, user, password):
    self.network_path = network_path
    self.absolute_path = absolute_path
    self.work_dir = work_dir
    self.env = env
    self.run = run
    self.user = user
    self.password = password

    if not self.run:
      try:
        self.relative_path = os.path.relpath(self.absolute_path, start=self.work_dir)
      except:
        try:
          self.relative_path = os.path.relpath(self.absolute_path, start=self.network_path)
        except:
          print("Failed! Perhaps you should use the --work_dir parameter?")
          sys.exit(0)

  @timeout(5, os.strerror(errno.ETIMEDOUT))
  def copy(self):
    print("Checking paths...", end="", flush=True)
    destination_path = self.network_path + self.relative_path
    files_are_the_same = shutil._samefile(self.absolute_path, destination_path)
    print(" DONE!")

    if files_are_the_same:
      print("Files are the same. Skipping copy!")
      return
    else:
      print("Copying '" + self.absolute_path + "' to '" + destination_path + "'...", end="", flush=True)

    success = False
    try:
      shutil.copy(self.absolute_path, destination_path)
      success = True
    except shutil.Error as e:
      print(" FAILED!\n\tError: %s" % e)
    except OSError as e:
      print(" FAILED!\n\tOS Error: {m} ({n}).".format(m=e.strerror, n=e.errno))

    if (not success):
      print("\nBuild aborted!")
      sys.exit(0)

    print(" DONE!")

  @timeout(20, os.strerror(errno.ETIMEDOUT))
  def build(self):
    file_name, file_extension = os.path.splitext(self.relative_path)
    if file_extension == ".i":
      print("Skipping build for {e} files.".format(e=file_extension))
      return

    star_web = StarWeb(self.env, self.user, self.password)
    star_web.build(self.relative_path)

  @timeout(20, os.strerror(errno.ETIMEDOUT))
  def run_script(self):
    with open(self.absolute_path, "r", encoding="cp1252") as script_file:
      script = script_file.read()

    star_web = StarWeb(self.env, self.user, self.password)
    star_web.run(script)
