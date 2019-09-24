import shlex
import os


class GreetServer(object):

    def __init__(self):
        pass

    def command_success(self):
        return "command success"

    def command_not_found(self):
        return "command not found"

    def bye(self) -> str:
        return "exit success"
   
    def delete_file(self, path, name) -> str:
        status = self.command_success()
        try:
            os.remove(os.path.join(path, name))
        except Exception as e:
            return str(e)
        return status

    def _process_file(self, path, name, operation, *args, **kwargs) -> str:
        status = self.command_success()
        try:
            f = open(os.path.join(path, name), operation)
            if operation == "r":
                status = f.read()
            elif operation == "a+":
                f.write(kwargs.get('content', None))
            f.close()

        except Exception as e:
            return str(e)
        return status

    def _root_folder_exists(self, root):
        if not os.path.exists(root):
            os.makedirs(root)

    def _get_storage_path(self) -> str:
        root = os.path.dirname(os.path.abspath(__file__)) + "/storage"
        self._root_folder_exists(root)
        return root

    def list(self, req) -> str:
        args = req.split()
        dirs = os.listdir(self._get_storage_path())
        status = ""
        if len(args) == 1:
            for dir in dirs:
                status = status + "{}   ".format(dir)
        elif len(args) == 2 and args[1] in ["-a", "-all"]:
            status = status + "."
            for dir in dirs:
                status = status + "\n{}".format(dir)
        else:
            status = self.command_not_found()
        return status

    def create(self, req) -> str:
        args = shlex.split(req)
        dirs = self._get_storage_path()
        status = ""
        if len(args) > 1:
            for file_name in args[1:]:
                status = self._process_file(dirs, file_name, "w+")
                if status != self.command_success():
                    return status
        else:
            status = self.command_not_found()
        return status

    def delete(self, req) -> str:
        args = shlex.split(req)
        dirs = self._get_storage_path()
        status = ""
        if len(args) > 1:
            for file_name in args[1:]:
                status = self.delete_file(dirs, file_name)
                if status != self.command_success():
                    return status
        else:
            status = self.command_not_found()
        return status

    def read(self, req) -> str:
        args = shlex.split(req)
        dirs = self._get_storage_path()
        status = ""
        if len(args) > 1:
            status = self._process_file(dirs, args[1], "r")
        else:
            status = self.command_not_found()
        return status

    def update(self, req):
        args = shlex.split(req)
        dirs = self._get_storage_path()
        status = ""
        if len(args) == 4:
            if args[1] in ["-append", "-a"]:
                status = self._process_file(dirs, args[2], "a+", content=args[3])
            elif args[1] in ["-overwrite", "-o"]:
                status = self._process_file(dirs, args[2], "w")
                status = self._process_file(dirs, args[2], "a+", content=args[3])
            else:
                status = self.command_not_found()
        else:
            status = self.command_not_found()
        return status
