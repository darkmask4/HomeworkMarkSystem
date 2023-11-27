from unittestreport import TestRunner,ddt,list_data
import unittest

suite = unittest.defaultTestLoader.discover(r'E:\shixun\HomeworkMarkSystem\houduan')


runner = TestRunner(suite)

runner.run()
