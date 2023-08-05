#!/usr/bin/python3-dbg
# -*- coding: utf-8 -*-


from chrysacase import ChrysalideTestCase
from pychrysalide.plugins.yaml import YamlReader
import tempfile


class TestYamlReader(ChrysalideTestCase):
    """TestCase for the Yaml reader."""


    @classmethod
    def setUpClass(cls):

        super(TestYamlReader, cls).setUpClass()

        cls._simple_map = tempfile.NamedTemporaryFile()

        cls._simple_map_data = b'''
a: av
b: bv
c: cv

'''

        cls._simple_seq = tempfile.NamedTemporaryFile()

        cls._simple_seq_data = b'''
- a: av
- b: bv
- c: cv

'''

        cls._nested = tempfile.NamedTemporaryFile()

        cls._nested_data = b'''
root:
  a: v0
  b: v1
  c: v2
  sub:
    aa: v00
    bb: v01
    cc: v02
      - i: w
      - j: x
      - k: c
  d: v3

'''

        cls._mixed = tempfile.NamedTemporaryFile()

        cls._mixed_data = b'''
root:
  - a: av
    aa: aav
    ab: abv
  - b: bv
    ba: bav
    bb: bbv

'''

        tmp = [
            [ cls._simple_map, cls._simple_map_data ],
            [ cls._simple_seq, cls._simple_seq_data ],
            [ cls._nested, cls._nested_data ],
            [ cls._mixed, cls._mixed_data ],
        ]

        for f, d in tmp:

            f.write(d)
            f.flush()

            cls.log('Using temporary file "%s"' % f.name)


    @classmethod
    def tearDownClass(cls):

        super(TestYamlReader, cls).tearDownClass()

        tmp = [
            cls._simple_map,
            cls._simple_seq,
            cls._nested,
            cls._mixed,
        ]

        for f in tmp:

            cls.log('Delete file "%s"' % f.name)

            f.close()


    def testSimpleYamlContent(self):
        """Validate Yaml content readers."""

        def _build_node_desc(node, left, extra = ''):

            if hasattr(node, 'key'):

                line = node.yaml_line

                prefix = '- ' if line.is_list_item else extra
                desc = left + prefix + line.key + ':' + (' ' + line.value if line.value else '') + '\n'
                indent = '  '

                collec = node.collection

            else:

                desc = ''
                indent = ''

                if hasattr(node, 'nodes'):
                    collec = node

            if collec:

                if collec.is_sequence:
                    extra = '  '

                for child in collec.nodes:
                    desc += _build_node_desc(child, left + indent, extra)

            return desc


        reader = YamlReader.new_from_path(self._simple_map.name)
        self.assertIsNotNone(reader)
        self.assertIsNotNone(reader.tree)

        fulldesc = _build_node_desc(reader.tree.root, '')

        self.assertEqual('\n' + fulldesc + '\n', self._simple_map_data.decode('ascii'))

        reader = YamlReader.new_from_path(self._simple_seq.name)
        self.assertIsNotNone(reader)
        self.assertIsNotNone(reader.tree)

        fulldesc = _build_node_desc(reader.tree.root, '')

        self.assertEqual('\n' + fulldesc + '\n', self._simple_seq_data.decode('ascii'))

        reader = YamlReader.new_from_path(self._nested.name)
        self.assertIsNotNone(reader)
        self.assertIsNotNone(reader.tree)

        fulldesc = _build_node_desc(reader.tree.root, '')

        self.assertEqual('\n' + fulldesc + '\n', self._nested_data.decode('ascii'))

        reader = YamlReader.new_from_path(self._mixed.name)
        self.assertIsNotNone(reader)
        self.assertIsNotNone(reader.tree)

        fulldesc = _build_node_desc(reader.tree.root, '')

        self.assertEqual('\n' + fulldesc + '\n', self._mixed_data.decode('ascii'))


    def testSimpleYamlContentFinder(self):
        """Validate Yaml nested content search."""

        reader = YamlReader.new_from_path(self._nested.name)
        self.assertIsNotNone(reader)

        found = reader.tree.find_by_path('/root/sub')

        self.assertEqual(len(found), 1)

        if len(found) == 1:
            self.assertEqual(found[0].key, 'sub')

        found = reader.tree.find_by_path('/root/sub/')

        self.assertEqual(len(found), 3)

        found = reader.tree.find_by_path('/root/sub/xx')

        self.assertEqual(len(found), 0)

        found = reader.tree.find_by_path('/root/sub/cc/i')

        self.assertEqual(len(found), 1)

        if len(found) == 1:
            self.assertEqual(found[0].key, 'i')
            self.assertEqual(found[0].yaml_line.is_list_item, True)

        found = reader.tree.find_by_path('/root/sub/cc')

        self.assertEqual(len(found), 1)

        if len(found) == 1:

            root = found[0]

            found = root.find_by_path('cc/i')

            self.assertEqual(len(found), 1)

            if len(found) == 1:

                self.assertEqual(found[0].key, 'i')
                self.assertEqual(found[0].yaml_line.is_list_item, True)

            found = root.find_by_path('/cc/i')

            self.assertEqual(len(found), 1)

            if len(found) == 1:

                self.assertEqual(found[0].key, 'i')
                self.assertEqual(found[0].yaml_line.is_list_item, True)

            found = root.find_by_path('//i')

            self.assertEqual(len(found), 1)

            if len(found) == 1:

                self.assertEqual(found[0].key, 'i')
                self.assertEqual(found[0].yaml_line.is_list_item, True)


    def testMixedYamlContentFinder(self):
        """Validate Yaml mixed content search."""

        reader = YamlReader.new_from_path(self._mixed.name)
        self.assertIsNotNone(reader)

        found = reader.tree.find_by_path('/root')

        self.assertEqual(len(found), 1)

        if len(found) == 1:
            self.assertEqual(found[0].key, 'root')

        found = reader.tree.find_by_path('/root/', True)

        self.assertEqual(len(found), 1)

        found = reader.tree.find_one_by_path('/root/', True)

        self.assertIsNotNone(found)

        if found:

            sub = found.find_one_by_path('/a')
            self.assertIsNotNone(sub)
            self.assertEqual(sub.key, 'a')

            sub = found.find_one_by_path('/aa')
            self.assertIsNotNone(sub)
            self.assertEqual(sub.key, 'aa')

        found = reader.tree.find_by_path('/root/')

        self.assertEqual(len(found), 2)

        if len(found) == 2:

            sub = found[0].find_one_by_path('/a')
            self.assertIsNotNone(sub)
            self.assertEqual(sub.key, 'a')

            sub = found[0].find_one_by_path('/aa')
            self.assertIsNotNone(sub)
            self.assertEqual(sub.key, 'aa')
