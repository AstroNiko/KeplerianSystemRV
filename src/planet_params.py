import numpy as np
import astropy.units as u
from astropy import constants as const
#############
"""Codigo creado por Nikola Salazar, Universidad de Concepción.
Se declara el uso de AI para revisión de sintaxis y corrección de legibilidad.
Todo el codigo ha sido escrito y revisado por un humano :)"""




def planet_mass(m_star, P, K, e, K_unit="km/s"):
    """
    Función para calcular la masa mínima del planeta mediante
    la aproximación M_p sin(i).

    Parameters:
    #############################
    m_star : float
        Masa estelar en M_sun.
    
    P : float
        Periodo orbital en días.
    
    K : float
        Semi-amplitud de la velocidad radial.
    
    e : float
        Excentricidad orbital.
    
    K_unit : str
        Unidad de la semiamplitud K. 
        Puede ser:
        "km/s" -> kilómetros por segundo
        "m/s"  -> metros por segundo

 #############################
    """

 
    if K_unit == "km/s":
        K = K * u.km / u.s # Acá se comienza a declarar la unit de K.

    elif K_unit == "m/s":
        K = K * u.m / u.s 

    else:
        raise ValueError(
            "K_unit debe ser 'km/s' o 'm/s'."
        ) #Por si las opciones no son validas, raise ValueError.

    Mstar = m_star * u.M_sun #Se declara la unidad de la masa estelar en M_sun units, se asume como estandar. Declarado en parameters

    # Conversión de unidades
    P_sec = P * 24 * 3600 * u.s #day ---> seg
    K_ms = K.to(u.m / u.s) #Independiente de la unidad entregada para K, esta se covierte a m/s dado la naturaleza fisica del problema.
    #note: La linea anterior no tiene efecto negativo en caso de que las unidades ya sean m/s.
    Mstar_kg = Mstar.to(u.kg)

    # M_p sin(i)
    mp_sini = (
        K_ms
        * np.sqrt(1 - e**2)
        * (P_sec / (2 * np.pi * const.G))**(1/3)
        * Mstar_kg**(2/3)
    ) #Esta ecuación corresponde a la aproximación para cuando M_p << M_star, revisar eq 2.27  (Perryman M. The Exoplanet Handbook. 2nd ed. Cambridge University Press; 2018.)

    # kg -> masas de Júpiter
    mp_sini = mp_sini.to(u.M_jupiter)

    return mp_sini

def mpsini_posterior(
    flat_samples,
    Mstar,
    sigma_Mstar,
    unit="jup",
    K_unit="km/s"
):
    """
    Calcula la distribución posterior de M_p sin(i)
    propagando la incertidumbre de la masa estelar.

    Parameters
    #################
    flat_samples : array
        Muestras del MCMC. Se espera que:
        sample[0] = P
        sample[1] = K
        sample[2] = e

    Mstar : float
        Masa estelar en M_sun.

    sigma_Mstar : float
        Incertidumbre de la masa estelar en M_sun.

    unit : str
        Unidad de la masa del planeta:
        "jup"   -> masas de Júpiter
        "earth" -> masas terrestres

    K_unit : str
        Unidad de K:
        "km/s" -> kilómetros por segundo
        "m/s"  -> metros por segundo

    Returns
    ######################
    mpsini : ndarray
        Distribución posterior de M_p sin(i).

    p50 : float
        Mediana.

    error_inferior : float
        Incertidumbre inferior.

    error_superior : float
        Incertidumbre superior.
    """

    mpsini = []

    for sample in flat_samples:

        # Parámetros orbitales de esta muestra del MCMC
        P = sample[0]       # días
        K = sample[1]       # K_unit
        e = sample[2]

        # Realización aleatoria de la masa estelar
        Mstar_i = np.random.normal(
            Mstar,
            sigma_Mstar
        ) #note: Es importante que el valor de la masa no sea un valor fijo para realizar la propagación de errores de la medición de la masa estelar.
                    #El approach tomado es sacar valores aleatorios con una distribución normal con mean value =  mstar y desviación de sigma_star
       

        # Calcular M_p sin(i)
        mp = planet_mass(
            m_star=Mstar_i,
            P=P,
            K=K,
            e=e,
            K_unit=K_unit
        ) #Calculamos para cada iteración

        # Guardar valor numérico en M_Jup
        mpsini.append(mp.value)

    mpsini = np.array(mpsini) #

    # Seleccionar unidad
    if unit == "earth":

        mpsini = (
            mpsini * u.M_jupiter
        ).to(u.M_earth).value

        unit_label = "M_Earth"

    elif unit == "jup":

        unit_label = "M_Jup"

    else:
        raise ValueError(
            "unit debe ser 'jup' o 'earth'."
        )

    # Percentiles
    p16, p50, p84 = np.percentile(
        mpsini,
        [16, 50, 84]
    )

    # Incertidumbres
    error_inferior = p50 - p16
    error_superior = p84 - p50

    print(f"---- Units: {unit_label} ----")

    return (
        mpsini,
        p50,
        error_inferior,
        error_superior
    )