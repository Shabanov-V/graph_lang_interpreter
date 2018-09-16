import unittest
import os
from main import *


class TestInputProcessing(unittest.TestCase):
    def test_empty_params(self):
        self.assertEqual(is_line_correct('[]s[]'), True)

    def test_many_params(self):
        self.assertTrue(is_line_correct('[s][a][342][c][asd]3sd2wa3dawd[orty][ooo][s][a]'))

    def test_empty_func_name(self):
        self.assertFalse(is_line_correct('[asd][ksd][][iuh]'))

    def test_multiline_input(self):
        s = ["[0]a[1]]", "[1]b[2]", "[2]c[3]", "[4]d[3]"]
        graph, rules = input_graph(s)
        self.assertDictEqual(graph, {'1': {'2': 'b'}, '0': {'1': 'a'}, '2': {'3': 'c'}, '4': {'3': 'd'}})
        self.assertItemsEqual(rules, [(['1'], 'b', ['2']), (['0'], 'a', ['1']),  (['2'], 'c', ['3']), (['4'], 'd', ['3'])])

    def test_multiline_input_with_error(self):
        s = ["[0]a[1]]", "[1]b[2]", "", "[2]c[3]", "[4]d[3]"]
        graph, rules = input_graph(s)
        self.assertIsNone(graph)


class TestFunctions(unittest.TestCase):
    def test_top_sort(self):
        self.assertEqual(top_sort({'1': {'3': 'c'}, '0': {'1': 'a'}, '2': {'1': 'b'}}), ['2', '0', '1', '3'])

    def test_top_sort_with_cycle(self):
        self.assertIsNone(top_sort({'1': {'3': 'c'}, '0': {'1': 'a'}, '3': {'0': 'd'}, '2': {'1': 'b'}}))

    def test_refactor_answer(self):
        ans = [(['b.mp4'], 'scale=360:480', ['vid2']), (['a.mp4'], 'scale=360:480', ['inScale']), ([''], 'color=c=black@1.0:s=720x480:r=29.75:d=9.0', ['bg']), (['bg', 'vid2'], 'overlay=360:0', ['basis1']), (['basis1', 'inScale'], 'overlay=0:0', ['out.mp4'])]
        refactored_ans = refactor_answer(ans)
        for line in refactored_ans:
            self.assertRegexpMatches(line, '^(\[.*\])+[^\[\]]+(\[.*\])+$')


class TestMain(unittest.TestCase):
    def tearDown(self):
        os.remove('input')

    def test_cycle(self):
        s = "[0]a[1]\n[2]b[1]\n[1]c[3]\n[3]d[0]\n"
        f = open('input', 'w')
        f.write(s)
        f.close()
        self.assertEqual(main("input"), 'Cycle was found')

    def test_incorect_input(self):
        s = "[0]a[1]\n\n[2]b[1]\n[1]c[3]\n[3]d[0]\n"
        f = open('input', 'w')
        f.write(s)
        f.close()
        self.assertEqual(main("input"), 'Incorect input')

    def test_sample(self):
        s = "[1]a[2]\n[0]b[1]\n[2]c[3]"
        f = open('input', 'w')
        f.write(s)
        f.close()
        self.assertEqual(main("input"), '[0]b[1]\n[1]a[2]\n[2]c[3]')


if __name__ == '__main__':
    unittest.main()
