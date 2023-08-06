import unittest
from unittest.mock import Mock

from leanit_mweb.testutils import Form


class TestForm(unittest.TestCase):
    def setUp(self):
        self.html = """
        <form action="/test1" method="post" id="form1" name="form1">
            <input type="text" name="username" value="te">
            <input type="password" name="password" value="">
            <input type="hidden" name="hidden" value="hiddenvalue">
            <input type="checkbox" name="checkbox" checked>
            <input type="submit" value="Submit">
        </form>
        <form action="/test2" method="get" id="form2" name="form2">
            <input type="text" name="username" value="frank">
            <input type="password" name="password" value="">
            <input type="submit" value="Submit">
        </form>
        """
        self.client = Mock()

    def test_parse_index(self):
        form = Form.parse(self.html, index=1)
        self.assertEqual(form.action, '/test2')
        self.assertEqual(form.method, 'get')
        self.assertEqual(form.data['username'], 'frank')

    def test_parse_id(self):
        form = Form.parse(self.html, id='form1')
        self.assertEqual(form.action, '/test1')
        self.assertEqual(form.method, 'post')

    def test_parse_name(self):
        form = Form.parse(self.html, name='form2')
        self.assertEqual(form.action, '/test2')
        self.assertEqual(form.method, 'get')

    def test_hidden_input(self):
        form = Form.parse(self.html, index=0)
        self.assertIn('hidden', form.data)
        self.assertEqual(form.data['hidden'], 'hiddenvalue')

    def test_checkbox(self):
        form = Form.parse(self.html, index=0)
        self.assertIn('checkbox', form.data)
        self.assertTrue(form.data['checkbox'])

if __name__ == '__main__':
    unittest.main()
