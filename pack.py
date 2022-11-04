import os
from time import localtime, strftime
import shutil
import re
import zipfile


class Pack:
    """Transform a Uitrace project to zip for CloudTesting

    The class Pack can zip the current uitrace project in order to upload to
    CloudTesting, the zip includes the followings:
    - images(.jpg) that used in all .py files, exclude code comment lines
    - all .py files
    - other files/folders, exclude .codecc, .vscode, log, .gitignore, .zip and .DS_Store
    """
    def __init__(self):
        self.current_dir = os.path.dirname(__file__)
        self.all_py = self.find_py()
        self.all_img = self.find_img()
        self.dir_name = self.mkdir()


    def find_py(self) -> list:
        """Get all .py file under current dir"""

        py_files = []
        for root, _, filename in os.walk(self.current_dir):
            for file in filename:
                if file.endswith(r".py") and file != 'pack.py':
                    py_files.append(os.path.join(root[len(self.current_dir)+1:], file))
        return py_files


    def find_img(self) -> list:
        """Get all absolute path of .jpg that are used in code lines"""

        pattern = re.compile(r'.jpg')
        imgs_path = []
        for py_file in self.all_py:
            with open(py_file, 'r') as f:
                lineno = 0
                lines = f.readlines()
                for line in lines:
                    lineno += 1
                    if not line.startswith('#'):
                        end_index = re.search(pattern, line, flags=0)
                        if end_index:
                            end_index = end_index.span()[1]
                            start_index = max(line.find("'", 0, end_index), line.find('"', 0, end_index))
                            img_name = line[start_index+1:end_index]
                            if os.path.exists(self.current_dir + '/' + img_name):
                                img_name = self.current_dir + '/' + img_name
                            elif os.path.exists(self.current_dir + '/data/img/' + img_name):
                                img_name = self.current_dir + '/data/img/' + img_name
                            else:
                                dir = os.path.abspath(py_file)
                                dir = os.path.dirname(dir)
                                if os.path.exists(dir + '/' +  img_name):
                                    img_name = dir + '/' + img_name
                                elif os.path.exists(dir + '/data/img/' + img_name):
                                    img_name = dir + '/data/img/' + img_name
                                else:
                                    print(f'checkout your img path in {py_file} - {lineno}')
                                    break
                            if img_name not in imgs_path:
                                imgs_path.append(img_name)
        return imgs_path


    def mkdir(self) -> str:
        dir_path = strftime('%Y%m%d%H%M%S', localtime())
        os.makedirs(dir_path)
        return dir_path


    def copy_file(self) -> None:
        """Copy all useful files to the specified directory"""

        pattern = re.compile(
            f"{self.dir_name}|.codecc|log|.vscode|.gitignore|.jpg| \
            .git|.DS_Store|.zip|.history|.pytest_cache|.idea|__pycache__"
            )
        for root, _, filename in os.walk(self.current_dir):
            for file in filename:
                from_path = os.path.join(root, file)
                if not re.search(pattern, from_path):
                    dir_name = self.dir_name + os.path.dirname(from_path)[len(self.current_dir):]
                    to_path = dir_name + '/' + file
                    if not os.path.isdir(dir_name):
                        os.makedirs(dir_name)
                    shutil.copy(from_path, to_path)
        for img_path in self.all_img:
            img_dir = os.path.dirname(img_path)[len(self.current_dir):]
            if not os.path.isdir(self.dir_name + img_dir):
                os.makedirs(self.dir_name + img_dir)
            shutil.copy(img_path, self.dir_name+img_path[len(self.current_dir):])


    def mkzip(self) -> bool:
        """Zip the specified directory"""

        self.copy_file()
        zip = zipfile.ZipFile(self.dir_name+'.zip', 'w', zipfile.ZIP_DEFLATED)
        for path, _, filenames in os.walk(self.dir_name):
            fpath = path.replace(self.dir_name, '')
            for filename in filenames:
                zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
        zip.close()
        shutil.rmtree(os.path.join(self.current_dir, self.dir_name))


if __name__ == '__main__':
    p = Pack()
    p.mkzip()
