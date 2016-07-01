#!/usr/bin/env python

# Simulate value flowing from protected balance into available balance that drains via wealth tax.
# The analogy is two buckets A and B... B drains at a rate proportional to the amount it holds
# such that the amount it holds at t+Tb is 1/2 half the original value, and A drains in the same
# way, but what pours out of A goes into B.
#
# The analytic solution is interesting.
#    http://kr5ddit.com/post/193

from math import log as ln, exp, e, sqrt

Ta = 1.0 # The half life in time units of value in A... ie A(t+Ta) = A(t)/2
Tb = 1.0 # The half life in time units for value in B... ie, B(t)
A0 = 1.0
B0 = 0.0

dt = 0.000001       # Size between calculations
Ts = 10             # Total simulation time
print_time = 0.1    # Print values at this many time units (every hour)

max_error = 1e-5

alpha_a = ln(2)/Ta
alpha_b = ln(2)/Tb

# Use close but incorrect analytic function
USE_INCORRECT = False

def numerical(A0, B0, alpha_a, alpha_b, dt):
    i  = 0
    t  = 0.0
    A = A0
    B = B0
    while True: #i<(Ts/dt+1):
        yield i, t, A, B
        A_leak = A*alpha_a*dt
        B_leak = B*alpha_b*dt
        B += A_leak
        A -= A_leak
        B -= B_leak
        t+=dt
        i+=1

def analytic_a(t, A0, alpha_a):
    return A0*exp(-t*alpha_a)

def analytic_b(t, A0, B0, alpha_a, alpha_b):
    if alpha_a == alpha_b:
        return (B0 + alpha_b*A0*t)*exp(-t*alpha_b)
    return (B0 - alpha_a*A0/(alpha_b-alpha_a))*exp(-t*alpha_b) + alpha_a*A0/(alpha_b-alpha_a)*exp(-t*alpha_a)

def incorrect_analytic_b(t, A0, B0, alpha_a, alpha_b):
    alpha_ab = 0.375215296 # This is correct at Bmax for Ta=Tb=A0=1 and B0=0
    return (A0 - analytic_a(t, A0, alpha_a))*exp(-t*alpha_ab) + B0*exp(-t*alpha_b)

def main(USE_INCORRECT= USE_INCORRECT):
    VA = lambda t: analytic_a(t, A0, alpha_a)
    VB = lambda t: analytic_b(t, A0, B0, alpha_a, alpha_b)
    if USE_INCORRECT:
        VB = lambda t: incorrect_analytic_b(t, A0, B0, alpha_a, alpha_b)
    V  = lambda t: VA(t) + VB(t)

    exceeded_error = False
    print("%16s, %16s, %16s, %16s, %16s, %16s, %16s, %16s" % ('t', 'A', 'B', 'A+B', 'VA(t)', 'VB(t)', 'V(t)', 'A + B - V(t)'))
    for i, t, A, B in numerical(A0, B0, alpha_a, alpha_b, dt):
        if t>Ts: break
        if (not exceeded_error) and (abs(A + B - V(t)) > max_error):
            exceeded_error = True
        if i%round(print_time/dt)==0:
            print("%16f, %16f, %16f, %16f, %16f, %16f, %16f, %16f" % (t, A, B, A+B, VA(t), VB(t), V(t), A + B - V(t)))
    if exceeded_error:
        print("WARNING: THE ANALYICAL SOLUTION IS LIKELY TO BE INCORRECT")

def syntaxerrorhere() # DELETE THIS LINE!

if __name__=="__main__":
    # main(True)
    main()
