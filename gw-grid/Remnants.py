import numpy as np
import matplotlib.pyplot as plt

"""
Analytically model the remnant mass
of a GW merger event. Compare to 
the given best fit parameter remnant
and plot.
"""

# from GWOSC
events = [
{'event' : "GW150914",
 'm1' : 35.6,
 'm2' : 30.6,
 'fm' : 63.1,
 'fm_uplim' : 3.4,
 'fm_lowlim' : 3.0}, 
{'event' : "GW170817",
 'm1' : 1.46,
 'm2' : 1.27,
 'fm' : 2.8,
 'fm_uplim' : 0,
 'fm_lowlim' : 2.8},
{'event' : "GW190521",
 'm1' : 95.3,
 'm2' : 69.0,
 'fm' : 156.3,
 'fm_uplim' : 36.8,
 'fm_lowlim' : 22.4},
{'event' : "GW190814",
 'm1' : 23.2,
 'm2' : 2.6,
 'fm' : 25.6,
 'fm_uplim' : 1.1,
 'fm_lowlim' : 0.9},
{'event' : "GW191127",
 'm1' : 53.,
 'm2' : 24.,
 'fm' : 76.,
 'fm_uplim' : 39.,
 'fm_lowlim' : 21.},
{'event' : "GW200115",
 'm1' : 5.9,
 'm2' : 1.44,
 'fm' : 7.2,
 'fm_uplim' : 1.8,
 'fm_lowlim' : 1.7}, 
]

# -- analytic model for final mass
def finalMass(a, b):
	# return final mass given two input masses
	m1 = np.vectorize(float)(np.array(a))
	m2 = np.vectorize(float)(np.array(b))

	m = m1 + m2
	eta = m1*m2/(m1+m2)**2.

	return m*(1. + (np.sqrt(8./9.)-1.)*eta - 0.4333*(eta**2.) - (0.4392*(eta**3)))

# driver
def main():
    # model remnant
    final_modeled_masses = []
    for event in events:
        m1 = event['m1']
        m2 = event['m2']
        final_modeled_masses.append(finalMass(m1, m2))

    # given remnant
    final_masses = []
    y_uplims = []
    y_lowlims = []
    for event in events:
        final_masses.append(event['fm'])
        y_uplims.append(event['fm_uplim'])
        y_lowlims.append(event['fm_lowlim'])

    # plot modeled remnant and given remnant with error bars
    x_array = np.arange(len(final_masses))
    plt.plot(x_array, final_modeled_masses, 'o')
    plt.errorbar(x_array, final_masses, yerr=(y_lowlims, y_uplims), fmt='o', color='red')

    for i in range(len(events)):
        event = events[i]
        q = round(event['m1'] / event['m2'], 2)
        label = event['event'] + ' (q={})'.format(q)
        plt.text(x=x_array[i], y=final_masses[i], s='  ' + label)

    plt.xticks([], [])
    plt.xlim([-0.5, len(x_array)+1.5])
    plt.title('Final Mass for Best Fit and Analytical Model')
    plt.ylabel('Final Mass (Solar Mass)')
    plt.show()

    # plot percent error between model and given
    percent_error = []
    for i in range(len(x_array)):
        percent_error.append(np.abs(final_masses[i] - final_modeled_masses[i]) / final_masses[i])

    percent_error = np.array(percent_error) * 100.
    plt.plot(x_array, percent_error, 'o')
    plt.title('Percent Error for Modeled Vs. Best Fit')
    plt.ylabel('Percent Error')
    plt.xticks([], [])
    plt.show()


main()
