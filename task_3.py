import os
import time
import psutil
from os.path import expanduser


class PrepareException(Exception):
    pass


class BaseTest:
    def __init__(self, tc_id, name):
        self.tc_id = tc_id
        self.name = name
        with open(log_file, 'a') as f:
            f.write('Test #{} {} created.\n'.format(self.tc_id, self.name))

    def prep(self):
        raise NotImplementedError('Определите clean_up в %s.' % (self.__class__.__name__))

    def run(self):
        raise NotImplementedError('Определите clean_up в %s.' % (self.__class__.__name__))

    def clean_up(self):
        raise NotImplementedError('Определите clean_up в %s.' % (self.__class__.__name__))

    def execute(self):
        try:
            with open(log_file, 'a') as f:
                f.write('Prepare to run test #{} {}\n'.format(self.tc_id, self.name))
                try:
                    self.prep()
                except PrepareException as e:
                    f.write(
                        'Failed to prepare to test #{} {}. {}\n\n'.format(
                            self.tc_id, self.name, e))
                    f.close()
                    return None

                f.write('Try to run test #{} {}\n'.format(self.tc_id, self.name))
                self.run()
                f.write('Test #{} {} running succesfully!\n'.format(self.tc_id, self.name))

                f.write('Cleaning up after test #{} {}\n'.format(self.tc_id, self.name))
                self.clean_up()
                f.write('Execution test #{} {} is done!\n\n'.format(self.tc_id, self.name))

        except BaseException as e:
            with open(log_file, 'a') as f:
                f.write('Error {} when running test {} {}\n'.format(e, self.tc_id, self.name))


class FileListTest(BaseTest):
    def prep(self):
        if int(time.time()) % 2 != 0:
            raise PrepareException('Current system time since Unix-era in seconds is odd.')

    def run(self):
        for f in os.listdir(home_dir):
            print(f)

    def clean_up(self):
        pass


class RandomFileTest(BaseTest):
    test_file = 'test'

    def prep(self):
        mem = psutil.virtual_memory()
        if mem.total / (1024 * 1024 * 1024) < 1:
            raise PrepareException('Less then 1GB RAM on your device!')

    def run(self):
        with open(RandomFileTest.test_file, 'wb') as f:
            f.write(os.urandom(1024 * 1024))

    def clean_up(self):
        os.remove(RandomFileTest.test_file)


log_file = 'log.txt'    # Определяем путь файла для логгирования(опять, же можно было использовать модуль, но сделаем ручками)
home_dir = expanduser("~")  # Интересный способ с просторов, как определить домашнюю директорию "на всех платформах"

test_case_1 = FileListTest(tc_id=1, name='FileListTest_case')
test_case_1.execute()

test_case_2 = RandomFileTest(tc_id=2, name='RandomFileTest_case')
test_case_2.execute()
