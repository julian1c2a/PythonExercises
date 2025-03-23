from decimal import getcontext
from decimal import Decimal as Dec
from fractions import Fraction as Fract
from numeric_calc import calc_bernoulli_list as bernoulli_list
from numeric_calc import calc_bernoulli_list_approximated as bernoulli_list_aprox

if __name__ == "__main__":

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

    print(" --------------------------------------------------------- ")
    print(" -------------- NUMEROS DE BERNOULLI EXACTOS ------------- ")
    print(" --------------------------------------------------------- ")

    lista_de_numeros_de_Bernoulli: list[Fract] = bernoulli_list(66)
    lista_de_numeros_de_Bernoulli_aproximados: list[Dec] = bernoulli_list_aprox(66)
    for ix in range(0, len(lista_de_numeros_de_Bernoulli)):
        if lista_de_numeros_de_Bernoulli[ix] != Fract(0, 1):
            print(f"Bernoulli[{ix}]  =  {lista_de_numeros_de_Bernoulli[ix]}")

    print(" --------------------------------------------------------- ")
    print(" ------------ NUMEROS DE BERNOULLI EN COMA FLOTANTE ------ ")
    print(" --------------------------------------------------------- ")

    getcontext().prec = 120

    for ix in range(0, len(lista_de_numeros_de_Bernoulli)):
        if lista_de_numeros_de_Bernoulli[ix] != Fract(0, 1):
            numerador: Dec = Dec(lista_de_numeros_de_Bernoulli[ix].numerator)
            denominador: Dec = Dec(lista_de_numeros_de_Bernoulli[ix].denominator)
            print(f"Bernoulli[{ix}]  =  {numerador / denominador}")

    print(" --------------------------------------------------------- ")
    print(" ------------ NUMEROS DE BERNOULLI EN COMA FLOTANTE ------ ")
    print(" --------- COMPARADOS CON LOS EXACTOS CON FRACCIONES ----- ")
    print(" --------------------------------------------------------- ")

    getcontext().prec = 120

    for ix in range(0, len(lista_de_numeros_de_Bernoulli)):
        if lista_de_numeros_de_Bernoulli[ix] != Fract(0, 1):
            numerador: Dec = Dec(lista_de_numeros_de_Bernoulli[ix].numerator)
            denominador: Dec = Dec(lista_de_numeros_de_Bernoulli[ix].denominator)
            mas_exacto: Dec = numerador / denominador
            diferencia_abs: Dec = abs(
                mas_exacto - lista_de_numeros_de_Bernoulli_aproximados[ix]
            )
            diferencia_rel: Dec = abs(diferencia_abs / mas_exacto)
            print(
                f"Diferencia entre formas de calcularBernoulli[{ix}]  =  {diferencia_rel}"
            )
