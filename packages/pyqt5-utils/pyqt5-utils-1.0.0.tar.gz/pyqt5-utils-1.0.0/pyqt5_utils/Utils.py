import os
import subprocess


class Utils:

    def convert_ui_to_py(self, directory='./ui/'):
        for filename in os.listdir(directory):
            if filename.endswith('.ui'):
                print(f'Converting {filename}...')
                subprocess.run(['pyuic5', '-o', os.path.join(directory, os.path.splitext(filename)[0] + '.py'),
                                os.path.join(directory, filename)])
