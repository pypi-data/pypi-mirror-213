import unittest
import json
from jw_lensegua.lensegua import *


class TestLensegua_Validation(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_validatonSolution(self):
        self.assertIsInstance(self._solution, Jw_Lensegua)

class TestLensegua_ExecutionA(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\A.json')
        data = json.load(f)
        self._data = data
        f.close()
        ##--- mutch data
        VALUES = list("BCDEGHIKLMNOPQRTUVWXYZ")
        VALUES.append("ENIE")
        VALUES.append("P1")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_A(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "A")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_A(data)
                self.assertIsNotNone(result)
                self.assertEqual(result['hand_value'], "A")
                self.assertFalse(result['rule_match'])
                self._solution.destroy()

class TestLensegua_ExecutionB(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\B.json')
        data = json.load(f)
        self._data = data
        f.close()
        ##--- mutch data
        VALUES = list("ACDEGHIKLMNOPQRTUVWXYZ")
        VALUES.append("ENIE")
        VALUES.append("P1")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_B(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "B")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_B(data)
                self.assertIsNotNone(result)
                self.assertEqual(result['hand_value'], "B")
                self.assertFalse(result['rule_match'])
                self._solution.destroy()

class TestLensegua_ExecutionC(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\C.json')
        data = json.load(f)
        self._data = data
        f.close()
        ##--- mutch data
        VALUES = list("ABDEGHIKLMNOPQRTUVWXYZ")
        VALUES.append("ENIE")
        VALUES.append("P1")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_C(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "C")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_C(data)
                self.assertIsNotNone(result)
                self.assertEqual(result['hand_value'], "C")
                self.assertFalse(result['rule_match'])
                self._solution.destroy()


class TestLensegua_ExecutionD(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\D.json')
        data = json.load(f)
        self._data = data
        f.close()
        ##--- mutch data
        VALUES = list("ABCEGHIKLMNOPQRTUVWXYZ")
        VALUES.append("ENIE")
        VALUES.append("P1")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_D(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "D")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_D(data)
                self.assertIsNotNone(result)
                self.assertEqual(result['hand_value'], "D")
                self.assertFalse(result['rule_match'])
                self._solution.destroy()

class TestLensegua_ExecutionE(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\E.json')
        data = json.load(f)
        self._data = data
        f.close()
        ##--- mutch data
        VALUES = list("ABCDGHIKLMNOPQRTUVWXYZ")
        VALUES.append("ENIE")
        VALUES.append("P1")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_E(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "E")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_E(data)
                self.assertIsNotNone(result)
                self.assertEqual(result['hand_value'], "E")
                self.assertFalse(result['rule_match'])
                self._solution.destroy()

class TestLensegua_ExecutionG(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\G.json')
        data = json.load(f)
        self._data = data
        f.close()
        ##--- mutch data
        VALUES = list("ABCDEHIKLMNOPQRTUVWXYZ")
        VALUES.append("ENIE")
        VALUES.append("P1")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_G(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "G")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_G(data)
                self.assertIsNotNone(result)
                self.assertEqual(result['hand_value'], "G")
                self.assertFalse(result['rule_match'])
                self._solution.destroy()

class TestLensegua_ExecutionH(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\H.json')
        data = json.load(f)
        self._data = data
        f.close()
        ##--- mutch data
        VALUES = list("ABCDEGIKLMNOPQRTUVWXYZ")
        VALUES.append("ENIE")
        VALUES.append("P1")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_H(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "H")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_H(data)
                self.assertIsNotNone(result)
                self.assertEqual(result['hand_value'], "H")
                self.assertFalse(result['rule_match'])
                self._solution.destroy()

class TestLensegua_ExecutionI(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\I.json')
        data = json.load(f)
        self._data = data
        f.close()
        ##--- mutch data
        VALUES = list("ABCDEGHKLMNOPQRTUVWXYZ")
        VALUES.append("ENIE")
        VALUES.append("P1")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_I(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "I")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_I(data)
                self.assertIsNotNone(result)
                self.assertEqual(result['hand_value'], "I")
                self.assertFalse(result['rule_match'])
                self._solution.destroy()

class TestLensegua_ExecutionK(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\K.json')
        data = json.load(f)
        self._data = data
        f.close()
        ##--- mutch data
        VALUES = list("ABCDEGHILMNOPQRTUVWXYZ")
        VALUES.append("ENIE")
        VALUES.append("P1")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_K(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "K")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_K(data)
                self.assertIsNotNone(result)
                self.assertEqual(result['hand_value'], "K")
                self.assertFalse(result['rule_match'])
                self._solution.destroy()

class TestLensegua_ExecutionL(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\L.json')
        data = json.load(f)
        self._data = data
        f.close()
        ##--- mutch data
        VALUES = list("ABCDEGHIKMNOPQRTUVWXYZ")
        VALUES.append("ENIE")
        VALUES.append("P1")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_L(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "L")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_L(data)
                self.assertIsNotNone(result)
                self.assertEqual(result['hand_value'], "L")
                self.assertFalse(result['rule_match'])
                self._solution.destroy()

class TestLensegua_ExecutionM(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\M.json')
        data = json.load(f)
        self._data = data
        f.close()
        ##--- mutch data
        VALUES = list("ABCDEGHIKLNOPQRTUVWXYZ")
        VALUES.append("ENIE")
        VALUES.append("P1")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_M(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "M")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_M(data)
                self.assertIsNotNone(result)
                self.assertEqual(result['hand_value'], "M")
                self.assertFalse(result['rule_match'])
                self._solution.destroy()

class TestLensegua_ExecutionN(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\N.json')
        data = json.load(f)
        self._data = data
        f.close()
        ##--- mutch data
        VALUES = list("ABCDEGHIKLMOPQRTUVWXYZ")
        VALUES.append("P1")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_N(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "N")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_N(data)
                self.assertIsNotNone(result)
                self.assertEqual(result['hand_value'], "N")
                self.assertFalse(result['rule_match'])
                self._solution.destroy()

class TestLensegua_ExecutionENIE(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\ENIE.json')
        data = json.load(f)
        self._data = data
        f.close()
        ##--- mutch data
        VALUES = list("ABCDEGHIKLMOPQRTUVWXYZ")
        VALUES.append("P1")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_ENIE(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "ENIE")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()

class TestLensegua_ExecutionO(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\O.json')
        data = json.load(f)
        self._data = data
        f.close()
        ##--- mutch data
        VALUES = list("ABCDEGHIKLMNPQRTUVWXYZ")
        VALUES.append("ENIE")
        VALUES.append("P1")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_O(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "O")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_O(data)
                self.assertIsNotNone(result)
                self.assertEqual(result['hand_value'], "O")
                self.assertFalse(result['rule_match'])
                self._solution.destroy()

class TestLensegua_ExecutionP(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\P.json')
        data = json.load(f)
        self._data = data
        f.close()
        f = open('src\\jw_lensegua\\tests\\muestras_json\\P1.json')
        data = json.load(f)
        self._data1 = data
        f.close()
        ##--- mutch data
        VALUES = list("ABCDEGHIKLNOQRTUVWXYZ")
        VALUES.append("ENIE")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_P(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "P")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_true1(self):
        result = self._solution.recog_P(self._data1)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "P")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_P(data)
                self.assertIsNotNone(result)
                self.assertEqual(result['hand_value'], "P")
                self.assertFalse(result['rule_match'])
                self._solution.destroy()

class TestLensegua_ExecutionQ(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\Q.json')
        data = json.load(f)
        self._data = data
        f.close()
        ##--- mutch data
        VALUES = list("ABCDEGHIKLMNPRTUVWYZ")
        VALUES.append("P1")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_Q(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "Q")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_Q(data)
                self.assertIsNone(result)
                self._solution.destroy()

class TestLensegua_ExecutionR(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\R.json')
        data = json.load(f)
        self._data = data
        f.close()
        ##--- mutch data
        VALUES = list("ABCDEGHIKLMNOPQTUVWXYZ")
        VALUES.append("ENIE")
        VALUES.append("P1")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_R(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "R")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_R(data)
                self.assertIsNotNone(result)
                self.assertEqual(result['hand_value'], "R")
                self.assertFalse(result['rule_match'])
                self._solution.destroy()

class TestLensegua_ExecutionT(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\T.json')
        data = json.load(f)
        self._data = data
        f.close()
        ##--- mutch data
        VALUES = list("ABCDEGHIKLMNOPQRUVWXYZ")
        VALUES.append("ENIE")
        VALUES.append("P1")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_T(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "T")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_T(data)
                self.assertIsNotNone(result)
                self.assertEqual(result['hand_value'], "T")
                self.assertFalse(result['rule_match'])
                self._solution.destroy()

class TestLensegua_ExecutionU(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\U.json')
        data = json.load(f)
        self._data = data
        f.close()
        ##--- mutch data
        VALUES = list("ABCDEGHIKLMNOPQRTVWXYZ")
        VALUES.append("ENIE")
        VALUES.append("P1")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_U(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "U")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_U(data)
                self.assertIsNotNone(result)
                self.assertEqual(result['hand_value'], "U")
                self.assertFalse(result['rule_match'])
                self._solution.destroy()
            
class TestLensegua_ExecutionV(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\V.json')
        data = json.load(f)
        self._data = data
        f.close()
        ##--- mutch data
        VALUES = list("ABCDEGHIKLMNOPQRTUWXYZ")
        VALUES.append("ENIE")
        VALUES.append("P1")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_V(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "V")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_V(data)
                self.assertIsNotNone(result)
                self.assertEqual(result['hand_value'], "V")
                self.assertFalse(result['rule_match'])
                self._solution.destroy()

class TestLensegua_ExecutionW(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\W.json')
        data = json.load(f)
        self._data = data
        f.close()
        ##--- mutch data
        VALUES = list("ABCDEGHIKLMNOPQRTUVXYZ")
        VALUES.append("ENIE")
        VALUES.append("P1")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_W(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "W")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_W(data)
                self.assertIsNotNone(result)
                self.assertEqual(result['hand_value'], "W")
                self.assertFalse(result['rule_match'])
                self._solution.destroy()

class TestLensegua_ExecutionX(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\X.json')
        data = json.load(f)
        self._data = data
        f.close()
        ##--- mutch data
        VALUES = list("ABCDEGHIKLMNPRTUVWYZ")
        VALUES.append("P1")
        VALUES.append("Y1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_X(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "X")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_X(data)
                self.assertIsNone(result)
                self._solution.destroy()

class TestLensegua_ExecutionY(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\Y.json')
        data = json.load(f)
        self._data = data
        f.close()
        f = open('src\\jw_lensegua\\tests\\muestras_json\\Y1.json')
        data = json.load(f)
        self._data1 = data
        f.close()
        ##--- mutch data
        VALUES = list("ABCDEGHIKLNOPQRTUVWXZ")
        VALUES.append("ENIE")
        VALUES.append("P1")
        VALUES.append("Z1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_Y(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "Y")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_true1(self):
        result = self._solution.recog_Y(self._data1)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "Y")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_Y(data)
                self.assertIsNotNone(result)
                self.assertEqual(result['hand_value'], "Y")
                self.assertFalse(result['rule_match'])
                self._solution.destroy()

class TestLensegua_ExecutionZ(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._solution = Jw_Lensegua()
        self._datas = []
        f = open('src\\jw_lensegua\\tests\\muestras_json\\Z.json')
        data = json.load(f)
        self._data = data
        f.close()
        f = open('src\\jw_lensegua\\tests\\muestras_json\\Z1.json')
        data = json.load(f)
        self._data1 = data
        f.close()
        ##--- mutch data
        VALUES = list("ABCDEGHIKLNOQRTUVWXY")
        VALUES.append("ENIE")
        VALUES.append("Y1")
        VALUES.append("P1")

        for idx, file in enumerate(VALUES):
            f = open('src\\jw_lensegua\\tests\\muestras_json\\'+file+'.json')
            data = json.load(f)
            self._datas.append(data)
            f.close()

    @classmethod
    def tearDownClass(self):
        self._solution.destroy()
        self._solution = None

    def test_true(self):
        result = self._solution.recog_Z(self._data)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "Z")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_true1(self):
        result = self._solution.recog_Z(self._data1)
        self.assertIsNotNone(result)
        self.assertEqual(result['hand_value'], "Z")
        self.assertTrue(result['rule_match'])
        self._solution.destroy()
    
    def test_false(self):
        for data in self._datas:
            with self.subTest(data):
                result = self._solution.recog_Z(data)
                self.assertIsNotNone(result)
                self.assertEqual(result['hand_value'], "Z")
                self.assertFalse(result['rule_match'])
                self._solution.destroy()

if __name__ == '__main__':
    unittest.main()