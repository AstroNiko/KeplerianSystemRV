import numpy as np
########### Main ########## 

class OrbitalSystem_infe:
    def __init__(self, e, w, P, K, T_0=0.0, gamma=0.0):
        """
        Clase para modelar un sistema binario/exoplanetario usando velocidades radiales.
        
        e : Excentricidad (0 <= e < 1)
        w : Argumento del periastro (en radianes)
        P : Período orbital (en días)
        K : Semi-amplitud de la velocidad radial (en m/s o km/s)
        T_0 : Época de paso por el periastro (en días)
        gamma : Velocidad sistémica/offset (en m/s o km/s)
        """
        self.e = e
        self.w = w
        self.P = P
        self.K = K
        self.T_0 = T_0
        self.gamma = gamma

    def MeanAnomaly(self, t):
        """Calcular la anomalía media M(t) para un tiempo t."""
        return 2 * np.pi * (t - self.T_0) / self.P #Sacada del Handbook ec 2.9

    def EccentricAnomaly(self, M, tolerancia=1e-6, max_iteraciones=100):
        """Resolver la ecuación de Kepler mediante el método Newton-Raphson."""
        E = M.copy()  # Suposición inicial
        for i in range(max_iteraciones):
            f = E - self.e * np.sin(E) - M
            f_prima = 1 - self.e * np.cos(E)
            E_next = E - (f / f_prima)
            if np.all(np.abs(E_next - E) < tolerancia):
                return E_next
            E = E_next
        return E

    def TrueAnomaly(self, t):
        """Calcula la anomalía verdadera v(t) para un tiempo t o arreglo de tiempos."""
        M = self.MeanAnomaly(t)
        E = self.EccentricAnomaly(M)
        
        x_comp = np.sqrt(1 + self.e) * np.sin(E / 2)
        y_comp = np.sqrt(1 - self.e) * np.cos(E / 2)
        v = 2 * np.arctan2(x_comp, y_comp)
        return v

    def RadialVelocity(self, t):
        """Calcula la velocidad radial en los tiempos t."""
        v = self.TrueAnomaly(t)
        vr = self.K * (np.cos(self.w + v) + self.e * np.cos(self.w)) + self.gamma
        return vr

    def OrbitalPhase(self, t):
        """Calcula la fase orbital (de 0 a 1) para un tiempo t."""
        return ((t - self.T_0) / self.P) % 1