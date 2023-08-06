import matplotlib.pyplot as plt
from mpmath import zeta, j
import numpy as np


def critical_strip():
    plt.rcParams['text.usetex'] = True

    fig, ax = plt.subplots()
    x = plt.xlim([-2, 4])
    y = plt.ylim([-5, 70])

    threshold1 = 0.
    threshold2 = .5
    threshold3 = 1.

    plt.axvline(threshold1, -1, 70, linestyle='-', color='black')
    plt.axvline(threshold2, -1, 70, linestyle='--', color='blue')
    plt.axvline(threshold3, -1, 70, linestyle='-', color='black')
    plt.fill_betweenx(y, threshold1, threshold3, color='#999', alpha=.5)
    x_zeros = [.5] * 15
    y_zeros = [14.13, 21.02, 25.01, 30.42, 32.93, 37.58, 40.91, 43.32, 48.00, 49.77, 52.97, 56.44, 59.34, 60.83, 65.11]
    plt.scatter(x_zeros, y_zeros)
    for i in range(len(y_zeros)):
        plt.text(x_zeros[i] + .04, y_zeros[i] + .04, "1/2 + " + str(y_zeros[i]) + "i", fontsize=7)

    ax.set_yticks([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ax.set_yticklabels(['0', '0i', '10i', '20i', '30i', '40i', '50i', '60i', '70i'])

    ax.spines['left'].set_position('zero')
    ax.spines['left'].set_linewidth(2.0)
    ax.spines['bottom'].set_position('zero')
    ax.spines['bottom'].set_linewidth(2.0)

    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')


    plt.gcf().text(.8, .01, r'\it{by Adrian Zapała}', fontsize=12)
    plt.title(r'First 15 $\displaystyle\zeta(s)$ nontrivial zeros', fontsize=28, pad=20)
    plt.xlabel('Re(s)', fontsize=14)
    plt.ylabel('Im(s)', fontsize=14)
    plt.grid()
    plt.savefig('critical_strip.jpg', dpi=300)
    plt.show()


def riemann_zeta():
    plt.rcParams['text.usetex'] = True

    critical_line_b = np.linspace(.0, 100, 10000)  # Generating complex arguments, imaginary part
    zeta_values = [zeta(0.5 + b * j) for b in critical_line_b]  # Complex values
    # To plot we must separate all complex numbers into two parts
    re_val = np.array([float(zeta_values[i].real) for i in range(len(zeta_values))])
    im_val = np.array([float(zeta_values[i].imag) for i in range(len(zeta_values))])

    fig = plt.figure(figsize=(20, 20), frameon=False)
    ax = plt.axes(xlim=(-5, 5), ylim=(-3, 3))

    ax.spines['left'].set_position('zero')
    ax.spines['left'].set_linewidth(2.0)
    ax.spines['bottom'].set_position('zero')
    ax.spines['bottom'].set_linewidth(2.0)

    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    ax.set_yticks([1, 2, 3, 4, 5, 6, 7, 8])
    ax.set_yticklabels(['-41', '-3i', '-2i', '-i', '0i', 'i', '2i', '3i'])
    plt.gcf().text(.8, .01, r'\it{by Adrian Zapała}', fontsize=12)
    plt.gcf().text(.01, .93,
                   r'$\displaystyle\zeta(s) = \sum_{n = 1}^\infty n^{-s} = \prod_{p}^{} \frac{1}{1 - p ^{-s}}$',
                   fontsize=18, fontfamily='Arial')
    plt.plot(re_val, im_val, lw=1, color='brown')
    plt.title(r'Riemann Zeta Function $\displaystyle\zeta(s), s = \frac{1}{2} + bi$', fontsize=28, pad=20)
    plt.xlabel('Re(s)', fontsize=14)
    plt.ylabel('Im(s)', fontsize=14)
    plt.axis('equal')
    plt.grid()
    plt.savefig('riemann_zeta.jpg', dpi=300)
    plt.show()
