#!/usr/bin/env python

# Simulate value flowing from protected balance into available balance that drains via wealth tax.

from math import log as ln, exp, e

Ta = 1 # The half life in time units of value in A... ie A(t+Ta) = A(t)/2
Tb = 7 # The half life in time units for value in B... ie, B(t)

alpha_a = ln(2)/Ta
alpha_b = ln(2)/Tb

A0 = 1
B0 = 0

dt = 0.000001 # Size between calculations
Ts = 7 # Total simulation time

A = A0
B = B0

t = 0.0

def VA(t):
    return A0*exp(-t*alpha_a)

def VB(t):
    if t==0:
        return B0
    # print(exp(-t*alpha_b))
    return (A0 - VA(t) + B0)*exp(-t*alpha_b) # + (A0 - VA(t))*exp(t*(alpha_b + alpha_a))

while t<Ts+dt:
    # leaks from A
    A_leak = A*(1-exp(-dt*alpha_a))
    B_leak = B*(1-exp(-dt*alpha_b))
    t = round(t/dt)*dt
    if t == int(t):
        print("%16f %16f %16f %16f %16f %16f %16f %16f %16f %16f %16f" % (t, A, VA(t), B, VB(t), A_leak, VA(t) - VA(t+dt), B_leak - A_leak, VB(t) - VB(t+dt), B - VB(t), exp(-t*(alpha_b))*(1-exp(-t*(alpha_a)))  ))
    A -= A_leak
    B += A_leak
    B -= B_leak
    t+=dt    