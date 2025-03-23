import random
import unittest
from decimal import Decimal as Dec
from fractions import Fraction as Fract


def calc_binom(n: int, k: int) -> int:
    """
    Calculate the binomial coefficient (n choose k).

    This function calculates the number of ways to choose k items from n items
    without replacement and without order. It implements the recursive formula for
    binomial coefficients, using memoization to avoid redundant computation.

    Args:
        n (int): The total number of items.
        k (int): The number of items to choose.

    Returns:
        int: The binomial coefficient of (n choose k).
    """
    if (n < 0) or (k < 0) or (k > n):
        return 0
    elif n == k or k == 0:
        return 1
    elif n - 1 == k or k == 1:
        return n
    elif n - 2 == k or k == 2:
        return n * (n - 1) // 2
    elif n - 3 == k or k == 3:
        return n * (n - 1) * (n - 2) // 6
    elif n - 4 == k or k == 4:
        return n * (n - 1) * (n - 2) * (n - 3) // 24
    else:
        # result = 1
        # for i in range(1,k+1):
        #    result *= (n+1-i)//(i*(n-k-i))
        # return result
        return (n * calc_binom(n - 1, k - 1)) // k


def calc_bernoulli_list(n: int) -> list[Fract]:
    """
    Calculate the list of Bernoulli numbers up to the n-th index.

    This function computes Bernoulli numbers using their recursive properties.
    It initializes a list of fractions, `lista_bernoulli`, to store the
    Bernoulli numbers from B_0 to B_n. The function calculates each Bernoulli
    number based on previously computed values and the binomial coefficients.

    Args:
        n (int): The highest index of the Bernoulli number to compute.

    Returns:
        list[Fract]: A list containing Bernoulli numbers from B_0 to B_n
        represented as fractions.
    """

    lista_bernoulli: list[Fract] = [Fract(0, 1)] * (n + 1)
    for k in range(0, n):
        if k == 0:
            lista_bernoulli[0] = Fract(1, 1)
        elif k == 1:
            lista_bernoulli[1] = Fract(-1, 2)
        elif k == 2:
            lista_bernoulli[2] = Fract(1, 6)
        elif k % 2 == 1:
            lista_bernoulli[k] = Fract(0, 1)
        else:
            result: Fract = Fract(0, 1)
            for l in range(0, k):
                result += Fract(calc_binom(k + 1, l), k + 1) * lista_bernoulli[l]
            lista_bernoulli[k] = -result
    return lista_bernoulli


def calc_bernoulli_list_approximated(n: int) -> list[Dec]:
    """
    Calculate the list of Bernoulli numbers up to the n-th index.

    This function computes Bernoulli numbers using their recursive properties.
    It initializes a list of fractions, `lista_bernoulli`, to store the
    Bernoulli numbers from B_0 to B_n. The function calculates each Bernoulli
    number based on previously computed values and the binomial coefficients.

    Args:
        n (int): The highest index of the Bernoulli number to compute.

    Returns:
        list[Fract]: A list containing Bernoulli numbers from B_0 to B_n
        represented as fractions.
    """

    lista_bernoulli: list[Dec] = [Dec(0)] * (n + 1)
    for k in range(0, n):
        if k == 0:
            lista_bernoulli[0] = Dec(1)
        elif k == 1:
            lista_bernoulli[1] = Dec(-1) / Dec(2)
        elif k == 2:
            lista_bernoulli[2] = Dec(1) / Dec(6)
        elif k % 2 == 1:
            lista_bernoulli[k] = Dec(0)
        else:
            result: Dec = Dec(0)
            for l in range(0, k):
                result += (Dec(calc_binom(k + 1, l)) / Dec(k + 1)) * lista_bernoulli[l]
            lista_bernoulli[k] = -result
    return lista_bernoulli


def lin_calc_for_decimals(c1: Dec, c0: Dec, x: Dec) -> Dec:
    return (c1 * x) + c0


def poly_calc_for_decimals(c: list[Dec], x: Dec) -> Dec | None:
    """

    Sea p[X] = a_n X^n + a_{n-1} X^{n-1} + ... + a_3 X^3 + a_2 X^2 + a_1 X + a_0.

    Vemos que p[X] = c_0                                       = c_0
    Vemos que p[X] = c_0 + X c_1                               = c_1 X + c_0
    Vemos que p[X] = c_0 + X (c_1 + X c_2)                     = c_2 X^2 + c_1 X + c_0
    Vemos que p[X] = c_0 + X (c_1 + X (c_2 + X c_3))           = c_3 X^3 + c_2 X^2 + c_1 X + c_0
    Vemos que p[X] = c_0 + X (c_1 + X (c_2 + X ( c_3 + X c_4)) = c_4 X^4 + c_3 X^3 + c_2 X^2 + c_1 X + c_0

    Si tenemos como función primitiva la evaluación del polinomio lineal q[X] = a_1 X + a_0, ev[p[X],X<-x] se puede
    realizar con evaluaciones repetidas ev[q[X],X<-x].

    Caso p[X] constante     p_0[x] = q[[0,c_0],x].
    Caso p[X] lineal        p_1[x] = q[[c_1,c_0],x].
    Caso p[X] cuadrático    p_2[x] = q[[q[c_2,c_1],x],c_0],x].
    Caso p[X] cúbico        p_3[x] = q[q[[q[c_3,c_2],x],c_1],x],x].
    Caso p[X] general       p_n[x] = qoqo..n..oq[[[...[c_n,c_{n-1}],x],c_{n-2}],x],...,c_0],x].

    Son n llamadas a la evaluación lineal con parejas de coeficientes consecutivos, excepto la última quizás.

    :param c:
              lista de coeficientes del polinomio p[X]
    :param x:
              número x en que se quiere evaluar el polinomio p[X]
    :return:
              evaluación del polinomio p[X] en el punto x
    """

    c_len: int = len(c)
    if c_len < 1:
        return None
    elif c_len >= 1:
        grado: int = c_len - 1
        if grado == 0:
            return c[0]
        elif grado == 1:
            result: Dec = lin_calc_for_decimals(c[1], c[0], x)
            return result
        else:
            result: Dec = lin_calc_for_decimals(c[grado], c[grado - 1], x)
            for i in range(1, grado):
                result = lin_calc_for_decimals(result, c[grado - i - 1], x)
            return result


def lin_calc_for_fractions(c1: Fract, c0: Fract, x: Fract) -> Fract:
    return (c1 * x) + c0


def poly_calc_for_fractions(c: list[Fract], x: Fract) -> Fract | None:
    """

    Sea p[X] = a_n X^n + a_{n-1} X^{n-1} + ... + a_3 X^3 + a_2 X^2 + a_1 X + a_0.

    Vemos que p[X] = c_0                                       = c_0
    Vemos que p[X] = c_0 + X c_1                               = c_1 X + c_0
    Vemos que p[X] = c_0 + X (c_1 + X c_2)                     = c_2 X^2 + c_1 X + c_0
    Vemos que p[X] = c_0 + X (c_1 + X (c_2 + X c_3))           = c_3 X^3 + c_2 X^2 + c_1 X + c_0
    Vemos que p[X] = c_0 + X (c_1 + X (c_2 + X ( c_3 + X c_4)) = c_4 X^4 + c_3 X^3 + c_2 X^2 + c_1 X + c_0

    Si tenemos como función primitiva la evaluación del polinomio lineal q[X] = a_1 X + a_0, ev[p[X],X<-x] se puede
    realizar con evaluaciones repetidas ev[q[X],X<-x].

    Caso p[X] constante     p_0[x] = q[[0,c_0],x].
    Caso p[X] lineal        p_1[x] = q[[c_1,c_0],x].
    Caso p[X] cuadrático    p_2[x] = q[[q[c_2,c_1],x],c_0],x].
    Caso p[X] cúbico        p_3[x] = q[q[[q[c_3,c_2],x],c_1],x],x].
    Caso p[X] general       p_n[x] = qoqo..n..oq[[[...[c_n,c_{n-1}],x],c_{n-2}],x],...,c_0],x].

    Son n llamadas a la evaluación lineal con parejas de coeficientes consecutivos, excepto la última quizás.

    :param c:
              lista de coeficientes del polinomio p[X]
    :param x:
              número x en que se quiere evaluar el polinomio p[X]
    :return:
              evaluación del polinomio p[X] en el punto x
    """

    c_len: int = len(c)
    if c_len < 1:
        return None
    elif c_len >= 1:
        grado: int = c_len - 1
        if grado == 0:
            return c[0]
        elif grado == 1:
            result: Fract = lin_calc_for_fractions(c[1], c[0], x)
            return result
        else:
            result: Fract = lin_calc_for_fractions(c[grado], c[grado - 1], x)
            for i in range(1, grado):
                result = lin_calc_for_fractions(result, c[grado - i - 1], x)
            return result


# def gregory_coefficients(n: int) -> list[Dec]:
#    """Calculates Gregory coefficients up to G_n"""
#    coeffs: list[Dec] = [Dec(0)] * (n + 1)
#    coeffs[1] = Dec(1)  # Initialize G_1 to 1 (important correction)
#    for i in range(2, n + 1):
#        coeffs[i] = Dec((-1)**(i+1))/Dec(2*i-1)
#    return coeffs

# def arctan(xarg: Dec, n: int = 100) -> Dec:
#    """Approximates arctan(xarg) using the Gregory series with n terms."""
#    getcontext().prec = 50 # Set desired precision
#    resultado: Dec = Dec( 0 )
#    coeffs: list[Dec] = gregory_coefficients(n) # Removed unnecessary re-calculation
#
#    x_pow = xarg
#    for i in range(1, n+1):
#        resultado += coeffs[i] * x_pow
#        x_pow *= (xarg * xarg) # More efficient exponentiation
#
#    return resultado


# Examples
class TestPolyCalc(unittest.TestCase):
    def test_constant_polynomial(self):
        """Test a constant polynomial."""
        self.assertEqual(poly_calc_for_decimals([Dec(5)], Dec(2)), Dec(5))
        self.assertEqual(poly_calc_for_decimals([Dec(-3)], Dec(-1)), Dec(-3))
        self.assertEqual(poly_calc_for_decimals([Dec(0)], Dec(100)), Dec(0))

    def test_linear_polynomial(self):
        """Test a linear polynomial."""
        self.assertEqual(poly_calc_for_decimals([Dec(2), Dec(3)], Dec(1)), Dec(5))
        # 3x + 2 at x=1
        self.assertEqual(poly_calc_for_decimals([Dec(-1), Dec(2)], Dec(0)), Dec(-1))
        # 2x - 1 at x=0
        self.assertEqual(
            poly_calc_for_decimals([Dec(1), Dec(-1)], Dec(-2)), Dec(3)
        )  # -x + 1 at x=-2

    def test_quadratic_polynomial(self):
        """Test a quadratic polynomial."""
        self.assertEqual(
            poly_calc_for_decimals([Dec(1), Dec(2), Dec(1)], Dec(2)), Dec(9)
        )  # x^2 + 2x + 1 at x=2
        self.assertEqual(
            poly_calc_for_decimals([Dec(0), Dec(0), Dec(1)], Dec(3)), Dec(9)
        )  # x^2 at x = 3
        self.assertEqual(
            poly_calc_for_decimals([Dec(-1), Dec(1), Dec(-1)], Dec(1)), Dec(-1)
        )  # -x^2+x-1 at x=1

    def test_cubic_polynomial(self):
        """Test a cubic polynomial."""
        self.assertEqual(
            poly_calc_for_decimals([Dec(1), Dec(0), Dec(0), Dec(1)], Dec(1)), Dec(2)
        )  # x^3 + 1 at x=1
        self.assertEqual(
            poly_calc_for_decimals([Dec(0), Dec(0), Dec(0), Dec(2)], Dec(-1)), Dec(-2)
        )  # 2x^3 at x=-1
        self.assertEqual(
            poly_calc_for_decimals([Dec(1), Dec(1), Dec(1), Dec(1)], Dec(0)), Dec(1)
        )  # x^3+x^2+x+1 at x=0

    def test_higher_degree_polynomial(self):
        """Test a polynomial of degree greater than 3."""
        coeffs = [Dec(1), Dec(2), Dec(0), Dec(-1), Dec(3)]  # 3x^4 - x^3 + 2x + 1
        self.assertEqual(poly_calc_for_decimals(coeffs, Dec(1)), Dec(5))
        coeffs = [Dec(1), Dec(-2), Dec(3), Dec(-4), Dec(5), Dec(-6)]
        self.assertEqual(poly_calc_for_decimals(coeffs, Dec(1)), Dec(-3))

    def test_random_degree_13_polynomial(self):
        """Test a polynomial of degree 13 with random coefficients."""
        degree = 13
        coeffs = [
            Dec(random.randint(-10, 10)) for _ in range(degree + 1)
        ]  # degree+1 coefficients
        x_val = Dec(random.randint(-5, 5))

        # Calculate the expected value using direct polynomial evaluation
        expected_result = Dec(0)
        for i, coeff in enumerate(coeffs):
            expected_result += coeff * (x_val**i)

        self.assertEqual(poly_calc_for_decimals(coeffs, x_val), expected_result)

    def test_empty_polynomial(self):
        """Test an empty polynomial (should return None)."""
        self.assertIsNone(poly_calc_for_decimals([], Dec(2)))


if __name__ == "__main__":
    unittest.main()
