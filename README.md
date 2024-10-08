# KRT approximator
Samples of input files can be found in `resources/samples`

## Applying KRT for function approximation
This application exploits KRT ([Kolmogorov Representation Theorem](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Arnold_representation_theorem)), and constructs certain representations (currently only additive ones are supported) which, in turn, approximate certain dependencies of input data given. Feature vectors $x_1, \dots, x_n$ are grouped into sets of such vectors $X_{1}, \dots, X_{N}$. Several target vectors $y_{1}, \dots, y_{m}$ are supported. 

### Additive model
Kolmogorov representation of a hypothesis function $f(x_{1}, \dots, x_{n})$ can be written using an additive hierarchical representation as:
```math
f(x_{1}, \dots, x_{n}) = \sum\limits_{q=1}\limits^{2n+1} \Phi_{q} \left( \sum \limits_{p=1} \limits^{n} \phi_{q, p} (x_{p}) \right) = \sum\limits_{q=1}\limits^{2n+1} c_{q} \left( \sum \limits_{p=1} \limits^{n} a_{q, p} \cdot \left( \lambda^{(0)}_{q, p} \cdot M_{0} (x_{p}) + \dots + \lambda^{(t)}_{q, p} \cdot M_{t} (x_{p}) \right) \right)
```

Here:
- $M_{k}(x)$ is a polynomial function (in this work the following orthogonal polynomials were used: Hermite, Chebyshev, Laguerre, and Legendre) 
- $k$ - the index of a degree
- $t$ - largest allowed degree
- $c_{q} \in \mathbb{R}, \space a_{q, p} \in \mathbb{R}, \space \lambda^{(k)}_{q, p} \in \mathbb{R}$

This way, under the assumption of linear independence of feature vectors, one can define functions of Kolmogorov representation using an additive fashion as follows:
```math
\displaylines{
\Phi_{q} : x \mapsto c_{q} \cdot x \\
\phi_{q, p}: x \mapsto a_{q, p} \cdot \sum \limits_{k=0} \limits^{t} \lambda^{(k)}_{q, p} \cdot M_{k} (x)}
```

It is worth noting that the additive representation requires much less terms than Kolmogorov representation provides ($2n+1$), therefore the following coefficients should be equal to $0$: 
```math
\displaylines{ c_{q} = 0 \quad \forall q \in \{ N+1, \space \dots, \space 2n + 1 \} \\
a_{q, p} = 0 \quad \forall p \notin \{ n_{q_{(-1)} + 1}, \space \dots, \space n_{q} \} }
```
Here:
- $N$ is the total number of vector groups, which are used only for convenience as often some vectors share certain *physical* bounds, 
- $n_{q}$ is the index of last vector of a group $q$, that is, a group $q$ contains such vectors $x_{i}$ that $i \in \{ n_{q_{(-1)} + 1}, \space n_{q_{(-1)} + 2}, \space \dots, \space n_{q} \}$

## App
This application enables to approximate Kolmogorov representation of a hypothesis function from data. It has a graphical user interface (GUI), developed with customtkinter. The application also enables to select from various gradient descent optimizers (Adam, RMSprop, AdaGrad, etc), and supports two languages (English and Ukrainian) as well as two color themes (light and dark).
![gif not found](src/resources/run.gif)
