import numpy as np

def poly_somme(P, Q):
    """
    Function to add two polynomials P and Q represented as arrays or single coefficients.

    Parameters:
    P, Q (array or int or float): Polynomials or coefficients to be added. 

    Returns:
    R (array): Resulting polynomial after addition.
    """
    
    # If both P and Q are int or float, simply add them
    if isinstance(P, (int, float)) and isinstance(Q, (int, float)):
        return P + Q

    # Convert P and Q to numpy arrays if they are int or float
    if isinstance(P, (int, float)):
        P = np.array([P])
    elif isinstance(Q, (int, float)):
        Q = np.array([Q])

    Np = P.shape[0]  # Length of P
    Nq = Q.shape[0]  # Length of Q

    # If P is longer than Q, prepend Q with zeros to match P's length
    if Np > Nq:
        Q = np.concatenate((np.zeros(Np - Nq, dtype=P.dtype), Q))
    # If Q is longer than P, prepend P with zeros to match Q's length
    elif Np < Nq:
        P = np.concatenate((np.zeros(Nq - Np, dtype=Q.dtype), P))

    R = P + Q  # Add the two polynomials
    return R  # Return the resulting polynomial
