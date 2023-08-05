import numpy as np


def lda_x(n):
    '''Slater exchange functional (spin-paired).
    Thesis: Eq. 2.11
    '''
    f = -3 / 4 * (3 / (2 * np.pi))**(2 / 3)
    rs = (3 / (4 * np.pi * n))**(1 / 3)

    ex = f / rs
    vx = 4 / 3 * ex
    return ex, vx


def lda_c_chachiyo(n):
    '''Chachiyo parametrization of the correlation functional (spin-paired).'''
    a = -0.01554535  # (np.log(2) - 1) / (2 * np.pi**2)
    b = 20.4562557

    rs = (3 / (4 * np.pi * n))**(1 / 3)

    ec = a * np.log(1 + b / rs + b / rs**2)
    vc = ec + a * b * (2 + rs) / (3 * (b + b * rs + rs**2))
    return ec, vc


def lda_c_vwn(n):
    '''Vosko-Wilk-Nusair parametrization of the correlation functional (spin-paired).
    Not used, only for reference as it was used in the master thesis.
    Thesis: Eq. 2.12 ff.
    '''
    A = 0.0310907
    b = 3.72744
    c = 12.9352
    x0 = -0.10498

    rs = (3 / (4 * np.pi * n))**(1 / 3)

    x = np.sqrt(rs)
    X = rs + b * x + c
    Q = np.sqrt(4 * c - b**2)
    fx0 = b * x0 / (x0**2 + b * x0 + c)
    f3 = 2 * (2 * x0 + b) / Q
    tx = 2 * x + b
    tanx = np.arctan(Q / tx)

    ec = A * (np.log(rs / X) + 2 * b / Q * tanx - fx0 * (np.log((x - x0)**2 / X) + f3 * tanx))

    tt = tx**2 + Q**2
    vc = ec - x * A / 6 * (2 / x - tx / X - 4 * b / tt - fx0 * (2 / (x - x0) - tx / X - 4 * (2 * x0 + b) / tt))  # noqa: E501
    return ec, vc
