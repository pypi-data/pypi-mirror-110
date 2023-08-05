
from chrysacase import ChrysalideTestCase
from pychrysalide.common import BitField


class TestBitFields(ChrysalideTestCase):
    """TestCase for common.BitField*"""

    def testDuplicateBitField(self):
        """Check duplicated bitfield value."""

        bf = BitField(10, 0)

        bf2 = bf.dup()

        self.assertEqual(bf, bf2)

        self.assertEqual(bf.size, bf2.size)

        self.assertEqual(bf.popcount, bf2.popcount)


    def testBitFieldValues(self):
        """Evaluate bitfields basic values."""

        bf_a = BitField(75, 1)

        bf_b = BitField(75, 0)

        self.assertNotEqual(bf_a, bf_b)

        bf_a = BitField(75, 1)

        bf_b = BitField(75, 0)
        bf_b.set_all()

        self.assertEqual(bf_a, bf_b)

        self.assertEqual(bf_a.popcount, bf_b.popcount)

        bf_a = BitField(75, 1)
        bf_a.reset_all()

        bf_b = BitField(75, 0)

        self.assertEqual(bf_a, bf_b)

        self.assertEqual(bf_a.popcount, bf_b.popcount)


    def testBitFieldLogicalOperations(self):
        """Perform logical operations on bitfields."""

        bf_a = BitField(75, 1)

        bf_b = BitField(75, 0)

        self.assertEqual(bf_a.size, bf_b.size)

        bf_f = bf_a & bf_b

        self.assertEqual(bf_f, bf_b)

        self.assertEqual(bf_f.popcount, bf_b.popcount)

        bf_f = bf_a | bf_b

        self.assertEqual(bf_f, bf_a)

        self.assertEqual(bf_f.popcount, bf_a.popcount)


    def testBitFieldSwitch(self):
        """Switch various bits in bitfields."""

        bf_1 = BitField(75, 1)

        bf_0 = BitField(75, 0)

        bf_t = BitField(75, 0)

        for i in range(75):
            bf_t.set(i, 1)

        self.assertEqual(bf_t, bf_1)

        self.assertEqual(bf_t.popcount, bf_1.popcount)

        for i in range(75):
            bf_t.reset(i, 1)

        self.assertEqual(bf_t, bf_0)

        self.assertEqual(bf_t.popcount, bf_0.popcount)


    def testBitFieldBits(self):
        """Test bits in bitfields."""

        bf = BitField(54, 1)

        self.assertTrue(bf.test(0))

        self.assertTrue(bf.test(53))

        self.assertTrue(bf.test_all(0, 54))

        self.assertFalse(bf.test_none(0, 54))

        bf = BitField(54, 0)

        self.assertFalse(bf.test(0))

        self.assertFalse(bf.test(53))

        self.assertFalse(bf.test_all(0, 54))

        self.assertTrue(bf.test_none(0, 54))


    def testPopCountForBitField(self):
        """Count bits set to 1 in bitfield."""

        bf = BitField(65, 1)

        self.assertEqual(bf.size, 65)

        self.assertEqual(bf.popcount, 65)


    def testBitFieldComparison(self):
        """Check bitfield comparison."""

        bf_a = BitField(9, 0)
        bf_a.set(0, 1)
        bf_a.set(5, 1)

        bf_b = BitField(9, 1)

        self.assertNotEqual(bf_a, bf_b)
