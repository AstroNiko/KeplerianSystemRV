# KeplerianSystemRV
 Este repositorio provee rutinas para realizar inferencia bayesiana de parámetros orbitales (sistemas planetarios) a partir de series temporales de velocidad radial. El ajuste paramétrico se realiza mediante cadenas de Markov Monte Carlo (MCMC) utilizando el paquete `emcee` y permite la derivación de distribuciones posteriores para los elementos orbitales.

 ## Estructura del Repositorio
* `data/`: Contiene los datos observacionales de entrada (ej. series de tiempo HIRES). *(Nota: Asegurar que los datos no publicados estén protegidos si el repositorio se abre en el futuro).*
* `src/`: Código fuente del proyecto. Incluye `orbital_model.py` con la clase principal `OrbitalSystem_infe` y las resoluciones de la ecuación de Kepler.
* `notebooks/`: Cuadernos de Jupyter empleados para la ejecución de ajustes, evaluación de la convergencia de las cadenas y generación de *corner plots*. Archivo principal: `RadialVelocities_emcee.ipynb`.
* `results/`: Directorio de salida para los estadísticos derivados (ej. `parametros_orbitales_mcmc.txt`).

## Requisitos e Instalación
Para poder utilizar el código, instale las dependencias especificadas en ``requirements.txt``:
```bash
pip install -r requirements.txt
``` 
