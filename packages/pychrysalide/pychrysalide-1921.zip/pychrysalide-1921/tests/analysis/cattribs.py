#!/usr/bin/python3
# -*- coding: utf-8 -*-


# S'assure du bon fonctionnement des attributs de contenus binaires à charger


from chrysacase import ChrysalideTestCase
from pychrysalide.analysis import ContentAttributes


class TestProjectFeatures(ChrysalideTestCase):
    """TestCase for binary content attributes."""

    def testEmptyContentAttributeSet(self):
        """Check properties of empty content attribute set."""

        attribs = ContentAttributes('')
        self.assertIsNotNone(attribs)

        self.assertIsNone(attribs.filename)

        self.assertEqual(len(attribs.keys), 0)


    def testContentAttributeSet(self):
        """Check properties of a basic content attribute set."""

        model = {
            'a': '0',
            'bb': '1',
            'ccc': '2',
            'dddd': '3',
        }

        filename = 'filename'
        path = filename

        for k in model.keys():
            path += '&%s=%s' % (k, model[k])

        attribs = ContentAttributes(path)
        self.assertIsNotNone(attribs)

        self.assertEqual(attribs.filename, filename)

        kcount = 0

        for key in attribs.keys:
            self.assertTrue(key in model.keys())
            kcount += 1

        self.assertEqual(kcount, len(model.keys()))


    def testMultiContentAttributeSet(self):
        """Check properties of a multi level content attribute set."""

        model = {
            'a': '0',
            'bb': '1',
            'ccc': '2',
            'dddd': '3',
        }

        path = ''

        for k in model.keys():
            path += '&%s=%s' % (k, model[k])

        path += '&'

        for k in model.keys():
            path += '&e%s=%s' % (k, model[k])

        attribs = ContentAttributes(path)
        self.assertIsNotNone(attribs)

        self.assertIsNone(attribs.filename)

        kcount = 0

        for key in attribs.keys:
            self.assertTrue(key in model.keys())
            kcount += 1

        self.assertEqual(kcount, len(model.keys()))


    def testEmptyContentAttributeSet(self):
        """Check properties of empty content attribute sets."""

        path = '&&'

        attribs = ContentAttributes(path)
        self.assertIsNotNone(attribs)

        self.assertIsNone(attribs.filename)

        self.assertEqual(len(attribs.keys), 0)

        path = '&&&'

        attribs = ContentAttributes(path)
        self.assertIsNotNone(attribs)

        self.assertIsNone(attribs.filename)

        self.assertEqual(len(attribs.keys), 0)

        path = 'filename'

        attribs = ContentAttributes(path)
        self.assertIsNotNone(attribs)

        self.assertEqual(len(attribs.keys), 0)

        self.assertEqual(attribs.filename, path)


    def testContentAttributesKeyAccess(self):
        """Test some access keys for content attributes."""

        model = {
            'a': '0',
        }

        path = ''

        for k in model.keys():
            path += '&%s=%s' % (k, model[k])

        attribs = ContentAttributes(path)
        self.assertIsNotNone(attribs)

        with self.assertRaisesRegex(Exception, 'key must be a string value'):

            val = attribs[2]

        with self.assertRaisesRegex(Exception, 'attribute value not found for the provided key'):

            val = attribs['2']
