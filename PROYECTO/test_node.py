import unittest
from node import *

class TestNode(unittest.TestCase): # Clase para testear la clase Node
    def setUp(self): # Método que se ejecuta antes de cada test
        self.n1 = Node("A", 0, 0) # Creamos 3 nodos
        self.n2 = Node("B", 3, 4) # A 3 unidades en x y 4 en y
        self.n3 = Node("C", 6, 8) # Otro nodo a 6 unidades en x y 8 en y
    
    def test_add_Neighbour(self): # Método para testear el método add_Neighbour
        self.assertTrue(AddNeighbour(self.n1, self.n2))  # A priori no deberian haber errores
        self.assertFalse(AddNeighbour(self.n1, self.n2))  # Tiene qeu devolver False porque ya es vecino
        self.assertIn(self.n2, self.n1.Neighbours)  # n2 tiene que ser vecino de n1

    def test_distance(self): # Método para testear el método Distance
        self.assertEqual(Distance(self.n1, self.n2), 5.0)  # 3-4-5 triangulo
        self.assertEqual(Distance(self.n2, self.n3), 5.0)  # otro 3-4-5 triangulo

if __name__ == "__main__":
    unittest.main()