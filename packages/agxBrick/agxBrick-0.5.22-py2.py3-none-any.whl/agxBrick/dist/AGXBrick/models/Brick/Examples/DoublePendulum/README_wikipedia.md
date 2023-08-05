```{=mediawiki}
{{more footnotes|date=June 2013}}
```
![A double pendulum consists of two [pendulums](pendulum "wikilink")
attached end to
end.](Double-Pendulum.svg "fig:A double pendulum consists of two pendulums attached end to end.")
In [physics](physics "wikilink") and
[mathematics](mathematics "wikilink"), in the area of [dynamical
systems](dynamical_systems "wikilink"), a **double pendulum** is a
[pendulum](pendulum "wikilink") with another pendulum attached to its
end, and is a simple [physical system](physical_system "wikilink") that
exhibits rich [dynamic behavior](dynamical_systems "wikilink") with a
[strong sensitivity to initial
conditions](butterfly_effect "wikilink").[^1] The motion of a double
pendulum is governed by a set of coupled [ordinary differential
equations](ordinary_differential_equation "wikilink") and is
[chaotic](chaos_theory "wikilink").

Analysis and interpretation {#analysis_and_interpretation}
---------------------------

Several variants of the double pendulum may be considered; the two limbs
may be of equal or unequal lengths and masses, they may be [simple
pendulums](simple_pendulum "wikilink") or [compound
pendulums](compound_pendulum "wikilink") (also called complex pendulums)
and the motion may be in three dimensions or restricted to the vertical
plane. In the following analysis, the limbs are taken to be identical
compound pendulums of length `{{mvar|l}}`{=mediawiki} and mass
`{{mvar|m}}`{=mediawiki}, and the motion is restricted to two
dimensions.

![Double compound
pendulum](Double-compound-pendulum-dimensioned.svg "fig:Double compound pendulum")
![Motion of the double compound pendulum (from numerical integration of
the equations of
motion)](double-compound-pendulum.gif "fig:Motion of the double compound pendulum (from numerical integration of the equations of motion)")
![Trajectories of a double
pendulum](Trajektorie_eines_Doppelpendels.gif "fig:Trajectories of a double pendulum")

In a compound pendulum, the mass is distributed along its length. If the
mass is evenly distributed, then the [center of
mass](center_of_mass "wikilink") of each limb is at its midpoint, and
the limb has a [moment of inertia](moment_of_inertia "wikilink") of
`{{math|''I'' {{=}}`{=mediawiki} `{{sfrac|1|12}}`{=mediawiki}*ml*^2^}}
about that point.

It is convenient to use the angles between each limb and the vertical as
the [generalized coordinates](generalized_coordinates "wikilink")
defining the [configuration](Configuration_space_(physics) "wikilink")
of the system. These angles are denoted
`{{math|''θ''<sub>1</sub>}}`{=mediawiki} and
`{{math|''θ''<sub>2</sub>}}`{=mediawiki}. The position of the center of
mass of each rod may be written in terms of these two coordinates. If
the origin of the [Cartesian coordinate
system](Cartesian_coordinate_system "wikilink") is taken to be at the
point of suspension of the first pendulum, then the center of mass of
this pendulum is at:

$$\begin{align}
x_1 &= \frac{l}{2} \sin \theta_1 \\
y_1 &= -\frac{l}{2} \cos \theta_1
\end{align}$$ and the center of mass of the second pendulum is at

$$\begin{align}
x_2 &= l \left ( \sin \theta_1 + \tfrac{1}{2} \sin \theta_2 \right ) \\
y_2 &= -l \left ( \cos \theta_1 + \tfrac{1}{2} \cos \theta_2 \right )
\end{align}$$ This is enough information to write out the Lagrangian.

### Lagrangian

The [Lagrangian](Lagrangian_mechanics "wikilink") is

$$\begin{align}L & = \text{kinetic energy} - \text{potential energy} \\
 & = \tfrac{1}{2} m \left ( v_1^2 + v_2^2 \right ) + \tfrac{1}{2} I \left ( {\dot \theta_1}^2 + {\dot \theta_2}^2 \right ) - m g \left ( y_1 + y_2 \right ) \\
 & = \tfrac{1}{2} m \left ( {\dot x_1}^2 + {\dot y_1}^2 + {\dot x_2}^2 + {\dot y_2}^2 \right ) + \tfrac{1}{2} I \left ( {\dot \theta_1}^2 + {\dot \theta_2}^2 \right ) - m g \left ( y_1 + y_2 \right ) \end{align}$$
The first term is the *linear* [kinetic
energy](kinetic_energy "wikilink") of the [center of
mass](center_of_mass "wikilink") of the bodies and the second term is
the *rotational* kinetic energy around the center of mass of each rod.
The last term is the [potential energy](potential_energy "wikilink") of
the bodies in a uniform gravitational field. The
[dot-notation](Newton's_notation "wikilink") indicates the [time
derivative](time_derivative "wikilink") of the variable in question.

Substituting the coordinates above and rearranging the equation gives

$$L = \tfrac{1}{6} m l^2 \left ( {\dot \theta_2}^2 + 4 {\dot \theta_1}^2 + 3 {\dot \theta_1} {\dot \theta_2} \cos (\theta_1-\theta_2) \right ) + \tfrac{1}{2} m g l \left ( 3 \cos \theta_1 + \cos \theta_2 \right ).$$
There is only one conserved quantity (the energy), and no conserved
[momenta](generalized_momentum "wikilink"). The two momenta may be
written as

$$\begin{align}
p_{\theta_1} &= \frac{\partial L}{\partial {\dot \theta_1}} = \tfrac{1}{6} m l^2 \left ( 8 {\dot \theta_1} + 3 {\dot \theta_2} \cos (\theta_1-\theta_2) \right ) \\
p_{\theta_2} &= \frac{\partial L}{\partial {\dot \theta_2}} = \tfrac{1}{6} m l^2 \left ( 2 {\dot \theta_2} + 3 {\dot \theta_1} \cos (\theta_1-\theta_2) \right ).
\end{align}$$

These expressions may be
[inverted](invertible_matrix#Inversion_of_2_.C3.97_2_matrices "wikilink")
to get

$$\begin{align}
{\dot \theta_1} &= \frac{6}{ml^2} \frac{ 2 p_{\theta_1} - 3 \cos(\theta_1-\theta_2) p_{\theta_2}}{16 - 9 \cos^2(\theta_1-\theta_2)} \\
{\dot \theta_2} &= \frac{6}{ml^2} \frac{ 8 p_{\theta_2} - 3 \cos(\theta_1-\theta_2) p_{\theta_1}}{16 - 9 \cos^2(\theta_1-\theta_2)}.
\end{align}$$

The remaining equations of motion are written as

$$\begin{align}
{\dot p_{\theta_1}} &= \frac{\partial L}{\partial \theta_1} = -\tfrac{1}{2} m l^2 \left ( {\dot \theta_1} {\dot \theta_2} \sin (\theta_1-\theta_2) + 3 \frac{g}{l} \sin \theta_1 \right ) \\
{\dot p_{\theta_2}} &= \frac{\partial L}{\partial \theta_2} = -\tfrac{1}{2} m l^2 \left ( -{\dot \theta_1} {\dot \theta_2} \sin (\theta_1-\theta_2) + \frac{g}{l} \sin \theta_2 \right ).
\end{align}$$

These last four equations are explicit formulae for the time evolution
of the system given its current state. It is not possible to go further
and integrate these equations analytically, to get formulae for
`{{math|''θ''<sub>1</sub>}}`{=mediawiki} and
`{{math|''θ''<sub>2</sub>}}`{=mediawiki} as functions of time. It is,
however, possible to perform this integration numerically using the
[Runge Kutta](Runge–Kutta_methods "wikilink") method or similar
techniques.

Chaotic motion {#chaotic_motion}
--------------

![Graph of the time for the pendulum to flip over as a function of
initial
conditions](Double_pendulum_flips_graph.png "fig:Graph of the time for the pendulum to flip over as a function of initial conditions")
![Long exposure of double pendulum exhibiting chaotic motion (tracked
with an
[LED](LED "wikilink"))](DPLE.jpg "fig:Long exposure of double pendulum exhibiting chaotic motion (tracked with an LED)")

The double pendulum undergoes [chaotic
motion](chaotic_motion "wikilink"), and shows a sensitive dependence on
[initial conditions](initial_conditions "wikilink"). The image to the
right shows the amount of elapsed time before the pendulum flips over,
as a function of initial position when released at rest. Here, the
initial value of `{{math|''θ''<sub>1</sub>}}`{=mediawiki} ranges along
the `{{mvar|x}}`{=mediawiki}-direction from −3 to 3. The initial value
`{{math|''θ''<sub>2</sub>}}`{=mediawiki} ranges along the
`{{mvar|y}}`{=mediawiki}-direction, from −3 to 3. The colour of each
pixel indicates whether either pendulum flips within:

-   ```{=mediawiki}
    {{math|10{{sqrt|{{frac|''l''|''g''}}}}}}
    ```
    (green)

-   ```{=mediawiki}
    {{math|100{{sqrt|{{frac|''l''|''g''}}}}}}
    ```
    (red)

-   ```{=mediawiki}
    {{math|1000{{sqrt|{{frac|''l''|''g''}}}}}}
    ```
    (purple) or

-   ```{=mediawiki}
    {{math|10000{{sqrt|{{frac|''l''|''g''}}}}}}
    ```
    (blue).

![Three double pendulums with near identical initial conditions diverge
over time displaying the chaotic nature of the system.
](Demonstrating_Chaos_with_a_Double_Pendulum.gif "fig:Three double pendulums with near identical initial conditions diverge over time displaying the chaotic nature of the system. ")
Initial conditions that do not lead to a flip within
`{{math|10000{{sqrt|{{frac|''l''|''g''}}}}}}`{=mediawiki} are plotted
white.

The boundary of the central white region is defined in part by energy
conservation with the following curve:

$$3 \cos \theta_1 + \cos \theta_2 = 2.$$

Within the region defined by this curve, that is if

$$3 \cos \theta_1 + \cos \theta_2 > 2,$$

then it is energetically impossible for either pendulum to flip. Outside
this region, the pendulum can flip, but it is a complex question to
determine when it will flip. Similar behavior is observed for a double
pendulum composed of two [point masses](point_mass "wikilink") rather
than two rods with distributed mass.[^2]

The lack of a natural excitation frequency has led to the use of [double
pendulum systems in seismic resistance
designs](Tuned_mass_damper "wikilink") in buildings, where the building
itself is the primary inverted pendulum, and a secondary mass is
connected to complete the double pendulum.

See also {#see_also}
--------

-   [Double inverted pendulum](Double_inverted_pendulum "wikilink")
-   [Pendulum (mathematics)](Pendulum_(mathematics) "wikilink")
-   Mid-20th century physics textbooks use the term \"double pendulum\"
    to mean a single bob suspended from a string which is in turn
    suspended from a V-shaped string. This type of
    [pendulum](pendulum "wikilink"), which produces [Lissajous
    curves](Lissajous_curves "wikilink"), is now referred to as a
    [Blackburn pendulum](Blackburn_pendulum "wikilink").

Notes
-----

```{=mediawiki}
{{reflist}}
```
References
----------

-   ```{=mediawiki}
    {{cite book
     | last = Meirovitch
     | first = Leonard
     | year = 1986
     | title = Elements of Vibration Analysis
     | edition = 2nd
     | publisher = McGraw-Hill Science/Engineering/Math
     | isbn = 0-07-041342-8
    }}
    ```
-   Eric W. Weisstein, *[Double
    pendulum](http://scienceworld.wolfram.com/physics/DoublePendulum.html)*
    (2005), ScienceWorld *(contains details of the complicated equations
    involved)* and \"[Double
    Pendulum](http://demonstrations.wolfram.com/DoublePendulum/)\" by
    Rob Morris, [Wolfram Demonstrations
    Project](Wolfram_Demonstrations_Project "wikilink"), 2007
    (animations of those equations).
-   [Peter Lynch](Peter_Lynch_(meteorologist) "wikilink"), *[Double
    Pendulum](https://web.archive.org/web/20030608233118/http://www.maths.tcd.ie/~plynch/SwingingSpring/doublependulum.html)*,
    (2001). *(Java applet simulation.)*
-   Northwestern University, *[Double
    Pendulum](http://www.physics.northwestern.edu/vpl/mechanics/pendulum.html)*,
    *(Java applet simulation.)*
-   Theoretical High-Energy Astrophysics Group at UBC, *[Double
    pendulum](https://web.archive.org/web/20070310213326/http://tabitha.phas.ubc.ca/wiki/index.php/Double_pendulum)*,
    (2005).

External links {#external_links}
--------------

-   Animations and explanations of a [double
    pendulum](http://www.physics.usyd.edu.au/~wheat/dpend_html/) and a
    [physical double pendulum (two square
    plates)](http://www.physics.usyd.edu.au/~wheat/sdpend/) by Mike
    Wheatland (Univ. Sydney)

<!-- -->

-   Interactive Open Source Physics JavaScript simulation with detailed
    equations [double
    pendulum](http://iwant2study.org/ospsg/index.php/interactive-resources/physics/02-newtonian-mechanics/02-dynamics/454-e-double-pendulum-drivenwee)
-   Interactive Javascript simulation of a [double
    pendulum](http://bestofallpossibleurls.com/double-pendulum.html)
-   Double pendulum physics simulation from
    [www.myphysicslab.com](https://www.myphysicslab.com/dbl_pendulum.html)
    using [open source JavaScript
    code](https://github.com/myphysicslab/myphysicslab)
-   Simulation, equations and explanation of [Rott\'s
    pendulum](http://www.chris-j.co.uk/rott.php)
-   ```{=mediawiki}
    {{YouTube|O2ySvbL3-yA|Comparison videos of a double pendulum with the same initial starting conditions}}
    ```
-   [Double Pendulum
    Simulator](http://freddie.witherden.org/tools/doublependulum/) - An
    open source simulator written in [C++](C++ "wikilink") using the [Qt
    toolkit](Qt_(toolkit) "wikilink").
-   [Online Java
    simulator](http://www.imaginary2008.de/cinderella/english/G2.html)
    of the [Imaginary exhibition](Imaginary_(exhibition) "wikilink").

```{=mediawiki}
{{Chaos theory}}
```
[Category:Chaotic maps](Category:Chaotic_maps "wikilink")
[Category:Pendulums](Category:Pendulums "wikilink")

[^1]: `{{cite journal |last=Levien |first=R. B. |last2=Tan |first2=S. M. |title=Double Pendulum: An experiment in chaos |journal=[[American Journal of Physics]] |year=1993 |volume=61 |issue=11 |page=1038 |doi=10.1119/1.17335 |bibcode=1993AmJPh..61.1038L }}`{=mediawiki}

[^2]: Alex Small, *[Sample Final Project: One Signature of Chaos in the
    Double
    Pendulum](https://12d82b32-a-62cb3a1a-s-sites.googlegroups.com/site/physicistatlarge/Computational%20Physics%20Sample%20Project-Alex%20Small-v1.pdf)*,
    (2013). A report produced as an example for students. Includes a
    derivation of the equations of motion, and a comparison between the
    double pendulum with 2 point masses and the double pendulum with 2
    rods.
