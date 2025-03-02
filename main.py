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
        return (n * calc_binom ( n - 1, k - 1 )) // k


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

    lista_bernoulli: list[Fract] = [Fract ( 0, 1 )] * (n + 1)
    for k in range ( 0, n ):
        if k == 0:
            lista_bernoulli[0] = Fract ( 1, 1 )
        elif k == 1:
            lista_bernoulli[1] = Fract ( -1, 2 )
        elif k == 2:
            lista_bernoulli[2] = Fract ( 1, 6 )
        elif k % 2 == 1:
            lista_bernoulli[k] = Fract ( 0, 1 )
        else:
            result: Fract = Fract ( 0, 1 )
            for l in range ( 0, k ):
                result += Fract ( calc_binom ( k + 1, l ), k + 1 ) * lista_bernoulli[l]
            lista_bernoulli[k] = -result
    return lista_bernoulli


if __name__ == '__main__':

    # N : int = 20
    # for l in range(0,N+1):
    #    print(f'Coeficientes binomiales de {l}')
    #    suma = 0
    #    for i in range(0,l+1):
    #        binnumber = calc_binom( l, i )
    #        print(f"Binomial({l},{i})  =  {binnumber}")
    #        suma += binnumber
    #    print(f"Sum_(k=0)^({l})[Binomial({l},k)]  = {suma} y 2^{l} = {2**l}")
    #    print("\n")

    print ( " --------------------------------------------------------- " )
    print ( " -------------- NUMEROS DE BERNOULLI EXACTOS ------------- " )
    print ( " --------------------------------------------------------- " )

    lista_de_numeros_de_Bernoulli = calc_bernoulli_list ( 21 )
    for ix in range ( 0, len ( lista_de_numeros_de_Bernoulli ) ):
        if lista_de_numeros_de_Bernoulli[ix] != Fract ( 0, 1 ):
            print ( f"Bernoulli[{ix}]  =  {lista_de_numeros_de_Bernoulli[ix]}" )

        # print ( " --------------------------------------------------------- " )
        # print ( " ------------ NUMEROS DE BERNOULLI EN COMA FLOTANTE ------ " )
        # print ( " --------------------------------------------------------- " )
        #
        # getcontext ().prec = 120
        #
        # for ix in range ( 0, len ( lista_de_numeros_de_Bernoulli ) ):
        #     if lista_de_numeros_de_Bernoulli[ix] != Fract ( 0, 1 ):
        #         numerador: Double = Double ( lista_de_numeros_de_Bernoulli[ix].numerator )
        #         denominador: Double = Double ( lista_de_numeros_de_Bernoulli[ix].denominator )
        #         print ( f"Bernoulli[{ix}]  =  {numerador / denominador}" )
