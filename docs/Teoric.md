# Documentación ``Main Notebook``
### Por: Nikola Salazar Varas, Universidad de Concepción

Con el objetivo de obtener velocidades radiales es necesario conocer las anamolias que describen nuestro sistema, para ello utilizaremos las definiciones y relaciones presentes en el *Exoplanet Handbook (Perryman, 2018)*, a continuación se trabajan alguna de ellas.
### Anomalia Media
Para empezar a describir nuestro objeto, comenzamos con la anomalía media, en particular una idealización:
$$M = \frac{2\pi}{P} t$$
Esta anomalía corresponde a una medida de tiempo uniforme escalada a radianes, en particular con t siendo el tiempo transcurrido desde el paso por el periastro y P el periodo orbital.
*"The relation between the mean anomaly,$ M (t)$, and the
eccentric anomaly, $E(t)$, can be derived from orbital dynamics. This relation, Kepler’s equation, is given by:"*

$$M = E - e \sin(E)$$

#### Metodo Newton-Raphson 
Debido a que la relación entre $M$ y $E$ es una ecuación que no se puede resolver de forma algebraica, es necesario utilizar un metodo distinto de resolución, debido a que ya conocemos un valor aproximado (ideal) es posible aplicar Newton-Raphson para hallar un valor de $E$.

$$f(E) = E - e \sin(E) - M = 0$$
Sabemos que el algoritmo refina el valor de la raiz usando una formula del tipo: 
$$E_{n+1} = E_n - \frac{f(E_n)}{f'(E_n)}$$

Donde: 

La derivada de $f$ corresponde a: $f'(E) = 1 - e \cos(E)$
De forma que: $$E_{n+1} = E_n - \frac{E_n - e \sin(E_n) - M}{1 - e \cos(E_n)}$$

### Anomalia verdadera 
Para describir la posición fisica del objeto, es necesario calcular su anomalía verdadera ($v$) esta última está relacionada con la Eccentric anomaly ($E$) mediante: 

$$\tan\left(\frac{v}{2}\right) = \sqrt{\frac{1 + e}{1 - e}} \tan\left(\frac{E}{2}\right)$$


Debido a que en python se tiene una limitación en cuanto a la función arcotangente(solo devuelve valores entre $-90^\circ$ y $+90^\circ$ ($-\pi/2$ a $\pi/2$ radianes)), es necesario usar (arctan2) la cual recibe componentes cartesianas. Por ello se hará el siguiente despeje:

$$\frac{\sin\left(\frac{v}{2}\right)}{\cos\left(\frac{v}{2}\right)} = \frac{\sqrt{1 + e} \cdot \sin\left(\frac{E}{2}\right)}{\sqrt{1 - e} \cdot \cos\left(\frac{E}{2}\right)}$$
$$\frac{v}{2} = \text{atan2}\left( \sqrt{1 + e} \sin\left(\frac{E}{2}\right) , \sqrt{1 - e} \cos\left(\frac{E}{2}\right) \right)$$
### Semi-Amplitude
La máxima variación de la velocidad radial de una estrella respecto a su velocidad sistémica, causada por la atracción gravitacional de un planeta u otro objeto compañero.
$$K = \frac{2\pi \cdot a \cdot \sin(i)}{P \cdot \sqrt{1 - e^2}}$$
En nuestro caso la relacionamos con la velocidades radiales mediante: 
$$v_r(t) = K \left[ \cos\big(\omega + \nu(t)\big) + e \cos \omega \right] + \gamma + d (t - t_0)$$

Donde: 
- $\gamma$: Velocidad sistemica
- $d(t-t_0)$: Desplazamiento instrumental

## En construcción...
### Periodograma de Lomb-Scargle
### Estadistica Bayesiana
### Inferencia Bayesiana y Muestreo MCMC
