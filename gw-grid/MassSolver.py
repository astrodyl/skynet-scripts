import numpy as np

""" 
    Calculate the value of mass,1 and mass,2 given 
    a total mass and a mass ratio. mass,1 and 
    mass,2 will be used to generate a grid of 
    models using LALSuite. Output to txt.
"""

def equation_solver(a, b):
	x = a / (b + 1.)
	return x, a - x


def createTXT(tms, mrs):
    # mass,1 values
    with open('values1.txt', 'w') as filehandle:
        # populate with values
        for i in tms:
            filehandle.write('{}\n'.format(round(10**i, 5)))
            for j in mrs:
                a, b = equation_solver(10**i, 10**j)
                filehandle.write('{} '.format(round(a, 5)))
            filehandle.write('\n\n')

    # mass,2 values
    with open('values2.txt', 'w') as filehandle:
        # populate with values
        for i in tms:
            filehandle.write('{}\n'.format(round(10**i, 5)))
            for j in mrs:
                a, b = equation_solver(10**i, 10**j)
                filehandle.write('{} '.format(round(b, 5)))
            filehandle.write('\n\n')


def main():
    # define grid steps (Arbitrarily defined by Dan)
    total_mass_steps = np.arange(np.log10(2.5), np.log10(251.), 0.2)
    mass_ratio_steps = np.arange(np.log10(1.), np.log10(10.1), 0.01)

    # output to txt
    createTXT(total_mass_steps, mass_ratio_steps)