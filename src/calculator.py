"""
Module Calculator - Application simple pour démonstration des tests IA
"""


class Calculator:
    """Calculatrice avec opérations de base"""

    def add(self, a: float, b: float) -> float:
        """Additionne deux nombres"""
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Soustrait b de a"""
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Multiplie deux nombres"""
        return a * b

    def divide(self, a: float, b: float) -> float:
        """Divise a par b

        Raises:
            ValueError: Si b est égal à 0
        """
        if b == 0:
            raise ValueError("Division par zéro impossible")
        return a / b

    def power(self, base: float, exponent: float) -> float:
        """Calcule base^exponent"""
        return base ** exponent

    def modulo(self, a: float, b: float) -> float:
        """Retourne le reste de a divisé par b"""
        if b == 0:
            raise ValueError("Modulo par zéro impossible")
        return a % b


class AdvancedCalculator(Calculator):
    """Calculatrice avancée avec fonctions mathématiques"""

    def factorial(self, n: int) -> int:
        """Calcule la factorielle de n

        Args:
            n: Entier positif

        Returns:
            Factorielle de n

        Raises:
            ValueError: Si n est négatif
        """
        if n < 0:
            raise ValueError("Factorielle définie uniquement pour les entiers positifs")
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def is_prime(self, n: int) -> bool:
        """Vérifie si n est un nombre premier"""
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True