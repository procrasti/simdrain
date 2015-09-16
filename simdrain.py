#!/usr/bin/env python

# Simulate value flowing from protected balance into available balance that drains via wealth tax.

from math import log as ln, exp, e, sqrt

Ta = 1.0 # The half life in time units of value in A... ie A(t+Ta) = A(t)/2
Tb = 1.0 # The half life in time units for value in B... ie, B(t)

alpha_a = ln(2)/Ta
alpha_b = ln(2)/Tb

A0 = 1.0
B0 = 0.0

dt = 0.00001 # Size between calculations
Ts = 10 # Total simulation time

A = A0
B = B0

t = 0.0

def VA(t):
    return A0*exp(-t*alpha_a)

def VB(t):
    if t==0:
        return B0
    # print(exp(-t*alpha_b))
    # return (A0 - VA(t) + B0)*exp(-t*alpha_b) # + (A0 - VA(t))*exp(t*(alpha_b + alpha_a))
    return B0*exp(-t*alpha_b) - A0*exp(-t*alpha_a) + A0*exp(-t*alpha_a*alpha_b)

def V(t):
    return A0*exp(-t*(alpha_a*alpha_b)) + B0*exp(-t*alpha_b)

i=0

while i<(Ts/dt+1):
    # leaks from A
    # A_leak = A*(1-exp(-alpha_a*dt))
    # B_leak = B*(1-exp(-alpha_b*dt))
    A_leak = A*alpha_a*dt
    B_leak = B*alpha_b*dt
    if i%round(1.0/dt/10.0)==0:
        # print("%16f %16f %16f %16f %16f %16f" % (t, A, B, A+B, V(t), A + B - V(t)))
        print("%16f, %16f, %16f, %16f, %16f, %16f" % (t, A, B, A+B, V(t), A + B - V(t)))
    B += A_leak
    A -= A_leak
    B -= B_leak
    t+=dt
    i+=1