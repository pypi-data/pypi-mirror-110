# import click

# @click.command()
# @click.argument('f')
# def F_to_K(f):
#     print("Convertir de Fahrenheit a Kelvin")
#     k = 273.5 + ((float(f) - 32.0) * (5.0/9.0))
#     print(f"{f} °F es igual a {round(k,2)} °K")

# @click.command()
# @click.argument('c')
# def C_to_R(c):
#     print("Convertir de Celsius a Rankine")
#     r = ((9* float(c))/5) + 491.67
#     print(f"{c} °C es igual a {round(r,2)} °Ra")

# @click.command()
# @click.argument('c')
# def C_to_F(c):
#     print("Convertir de Celsius a Fahrenheit")
#     f = (9.0/5.0) * float(c) + 32
#     print(f"{c} °C es igual a {round(f,2)} °F")

# if __name__ == '__main__':
#     C_to_F()



def main():
    pass


def F_to_K(f):
    print("Convertir de Fahrenheit a Kelvin")
    k = 273.5 + ((float(f) - 32.0) * (5.0/9.0))
    print(f"{f} °F es igual a {round(k,2)} °K")


def C_to_R(c):
    print("Convertir de Celsius a Rankine")
    r = ((9* float(c))/5) + 491.67
    print(f"{c} °C es igual a {round(r,2)} °Ra")


def C_to_F(c):
    print("Convertir de Celsius a Fahrenheit")
    f = (9.0/5.0) * float(c) + 32
    print(f"{c} °C es igual a {round(f,2)} °F")

if __name__ == '__main__':
    import sys
    print(sys.argv)
    v = sys.argv[1]
    valor = int(sys.argv[2])

    if v == 'C_to_F':
        C_to_F(valor)
    elif v == 'C_to_R':
        C_to_R(valor)
    elif v == 'F_to_K':
        F_to_K(valor)
    #import sys
    #C_to_F(int(sys.argv[1]))
    #C_to_R(int(sys.argv[1]))
    #F_to_K(int(sys.argv[1]))
    