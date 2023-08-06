"""
Utilities for managing units of measurement and physical quantities.

This module is a comprehensive suite for managing units of measurement and representing physical quantities in a
precise, unambiguous way.
It sets up a unit registry and provides a matching definition of a physical quantity with an associated quantity and
unit.
The module further offers a great variety of classes that specify physical dimensions such as length, mass, area, speed,
density, electrical charge, and more. These classes can be used as generic type annotations for the Pydantic-compatible
fields {py:class}`~optool.fields.quantities.UnitLike`, {py:class}`~optool.fields.quantities.QuantityLike`,
{py:class}`optool.fields.series.SeriesLike`, etc.
"""

from typing import Optional

import pint
import pint_pandas

UNITS = pint.get_application_registry()
"""
The application's {py:class}`pint.UnitRegistry`, retrieved via {py:func}`pint.get_application_registry`.

:::{seealso}
See [the answer on stackoverflow](https://stackoverflow.com/a/68089489) for why this is a good idea.
:::
"""

UNITS.define('square_meter = meter**2 = m² = m2')
UNITS.define('cubic_meter = meter**3 = m3')

# Exchange rates as of May 10, 2022, 3:48 p.m., taken from https://finance.yahoo.com/currency-converter/
UNITS.define('USD = [currency] = $ = usd')
UNITS.define('CHF = USD / 0.9918 = _ = chf')
UNITS.define('EUR = USD / 0.9484 = € = eur')

Quantity = UNITS.Quantity  # Should use this registry, see https://github.com/hgrecco/pint/issues/1480
"""
Representation of a physical quantity with a value and associated unit.

This class represents a physical quantity, consisting of a numerical value and an associated unit. It provides
functionality for performing mathematical operations and conversions between different units.


:param magnitude: The numerical value of the quantity.
:param units: The unit associated with the quantity.

:::{note}
This class is a reference to {py:class}`pint.Quantity` that has {py:data}`UNITS` as its {py:class}`pint.UnitRegistry`.
:::

::::{admonition} Examples
:class: example, dropdown

- Creating a Quantity object:
  ```python
  from optool.uom import Quantity, UNITS
  length = Quantity(5, UNITS.meter)
  print(length)
  ```
  yields `5 meter`.

- Performing arithmetic operations:
  ```python
  width = Quantity(3, UNITS.meter)
  area = length * width
  print(area)
  ```
  yields `15 meter ** 2`.

- Converting between units:
  ```python
  length = Quantity(1000, UNITS.millimeter)
  print(length.to(UNITS.meter))
  ```
  yields `1 meter`.

::::
"""

Unit = UNITS.Unit
"""
Representation of a unit of measurement.

This class represents a unit of measurement, which provides a standard and consistent way to quantify and compare
quantities in their respective domains.

:::{note}
This class is a reference to {py:class}`pint.Unit`.
:::

::::{admonition} Examples
:class: example, dropdown

- Creating a Unit object:
  ```python
  from optool.uom import UNITS
  meter = UNITS.meter
  print(meter)
  ```
  yields `meter`.

- Performing arithmetic operations:
  ```python
  from optool.uom import UNITS
  area = UNITS.meter**2
  print(area)
  ```
  yields `meter ** 2`.

- Parsing strings:
  ```python
  from optool.uom import UNITS
  kilometer = UNITS.parse_units("km")
  print(kilometer)
  ```
  yields `kilometer`.
"""

pint_pandas.PintType.ureg = UNITS


class PhysicalDimension:
    """
    Base class representing a physical dimension.

    The dimensionality attribute is a string representing the SI unit of the specific physical dimension. Subclasses of
    `PhysicalDimension` represent specific physical dimensions and should provide an appropriate dimensionality.

    :::{note}
    This class does not implement specific behavior and should not be instantiated directly. Instead, use or create a
    subclass that represents a specific physical dimension.
    :::

    :::{seealso}
    [Wikipedia: Dimensional analysis](wiki:Dimensional_analysis)
    :::
    """
    dimensionality: Optional[str] = None
    """String representing the SI unit of the specific physical dimension."""


class Absement(PhysicalDimension):
    """
    A measure of sustained displacement of an object from its initial position, i.e. a measure of how far away and for
    how long. In SI units, it is usually measured in meter-seconds (m·s).

    :::{seealso}
    [Wikipedia: Absement](wiki:Absement)
    :::
    """
    strict = False
    dimensionality = '[length] * [time]'


class Acceleration(PhysicalDimension):
    """
    Rate of change of the velocity of an object with respect to time. In SI units, it is usually measured in meters per
    square seconds (m/s²).

    :::{seealso}
    [Wikipedia: Acceleration](wiki:Acceleration)
    :::
    """
    strict = False
    dimensionality = '[acceleration]'


class Action(PhysicalDimension):
    """
    Energy multiplied by a duration, used to describe how a physical system has changed over time.

    :::{seealso}
    [Wikipedia: Action (physics)](wiki:Action_(physics))
    :::
    """
    strict = False
    dimensionality = '[energy] * [time]'


class AmountOfSubstance(PhysicalDimension):
    """
    Number of elementary entities of a substance. It is one of the seven fundamental physical quantities in both the
    International System of Units (SI) and the International System of Quantities (ISQ). The SI base unit of time is the
    mole (mol).

    One mole contains exactly 6.022 140 76 × 10²³ elementary entities. This number is the fixed numerical value of
    the Avogadro constant, NA, when expressed in the unit 1/mol and is called the Avogadro number.

    :::{seealso}
    [Wikipedia: Amount of substance](wiki:Amount_of_substance)
    :::
    """
    strict = False
    dimensionality = '[substance]'


class Angle(PhysicalDimension):
    """
    A dimensionless measure describing the relative position of two beams to each other.

    :::{seealso}
    [Wikipedia: Angle](wiki:Angle)
    :::
    """
    strict = False
    dimensionality = '[]'


class AngularAcceleration(PhysicalDimension):
    """
    The time rate of change of angular velocity. In SI units, it is usually measured in radians per square second
    (rad/s²).

    :::{seealso}
    [Wikipedia: Angular acceleration](wiki:Angular_acceleration)
    :::
    """
    strict = False
    dimensionality = '[] / [time] ** 2'


class AngularVelocity(PhysicalDimension):
    """
    A measure of how fast the angular position or orientation of an object changes with time. In SI units, it is usually
    measured in radians per second (rad/s).

    :::{seealso}
    [Wikipedia: Angular velocity](wiki:Angular_velocity)
    :::
    """
    strict = False
    dimensionality = '[] / [time]'


class Area(PhysicalDimension):
    """
    Measure of a region's size on a surface. In SI units, it is usually measured in square meters (m²).

    :::{seealso}
    [Wikipedia: Area](wiki:Area)
    :::
    """
    strict = False
    dimensionality = '[area]'


class AreaDensity(PhysicalDimension):
    """
    Measure of the mass per unit area of a two-dimensional object. In SI units, it is usually measured in kilograms per
    square meters (kg/m²).

    :::{seealso}
    [Wikipedia: Area density](wiki:Area_density)
    :::
    """
    strict = False
    dimensionality = '[mass] / [area]'


class CatalyticActivity(PhysicalDimension):
    """
    Measure for quantifying the catalytic activity of enzymes and other catalysts. The SI derived unit for measuring the
    catalytic activity of a catalyst is the katal, which is quantified in moles per second (mol/s).

    :::{seealso}
    [Wikipedia: Catalysis](wiki:Catalysis)
    :::
    """
    strict = False
    dimensionality = '[activity]'


class Concentration(PhysicalDimension):
    """
    Measure of the concentration of a chemical species in terms of amount of substance per unit volume of solution. In
    SI units, it is usually measured in moles per liter (mol/l).

    :::{seealso}
    [Wikipedia: Molar concentration](wiki:Molar_concentration)
    :::
    """
    strict = False
    dimensionality = '[concentration]'


class Density(PhysicalDimension):
    """
    Measure of a substance's mass per unit of volume. In SI units, it is usually measured in kilograms per cubic meters
    (kg/m3).

    :::{seealso}
    [Wikipedia: Density](wiki:Density)
    :::
    """
    strict = False
    dimensionality = '[density]'


class Dimensionless(PhysicalDimension):
    """
    A quantity to which no physical dimension is assigned, with a corresponding SI unit of measurement of one.

    :::{seealso}
    [Wikipedia: Dimensionless quantity](wiki:Dimensionless_quantity)
    :::
    """
    strict = False
    dimensionality = '[]'


class ElectricalConductivity(PhysicalDimension):
    """
    A measure of a material's ability to conduct electric current. Electrical conductivity is also called specific
    conductance and is the reciprocal of {py:class}`ElectricalResistivity`. In SI units, it is usually measured in
    siemens per metre (S/m).

    :::{seealso}
    [Wikipedia: Electrical resistivity and conductivity
       ](wiki:Electrical_resistivity_and_conductivity)
    :::
    """
    strict = False
    dimensionality = '[conductance] / [length]'


class ElectricalResistivity(PhysicalDimension):
    """
    A measure of how strongly a material resists electric current. Electrical resistivity is also called specific
    electrical resistance or volume resistivity. In SI units, it is usually measured in ohm-meters (Ω⋅m).

    :::{seealso}
    [Wikipedia: Electrical resistivity and conductivity
       ](wiki:Electrical_resistivity_and_conductivity)
    :::
    """
    strict = False
    dimensionality = '[resistivity]'


class ElectricCapacitance(PhysicalDimension):
    """
    The capability of a material object or device to store electric charge, measured by the change in charge in response
    to a difference in electric potential. The unit commonly used in the SI unit system is the farad (F).

    :::{seealso}
    [Wikipedia: Capacitance](wiki:Capacitance)
    :::
    """
    strict = False
    dimensionality = '[capacitance]'


class ElectricCharge(PhysicalDimension):
    """
    The physical property of matter that causes charged matter to experience a force when placed in an electromagnetic
    field. The units commonly used in the SI unit system are the coulomb (C) and the ampere-hours (A·h).

    :::{seealso}
    [Wikipedia: Electric charge](wiki:Electric_charge)
    :::
    """
    strict = False
    dimensionality = '[charge]'


class ElectricConductance(PhysicalDimension):
    """
    A measure for the ease with which an electric current passes. Its reciprocal quantity is
    {py:class}`ElectricResistance`. The unit commonly used in the SI unit system is the siemens (S).

    :::{seealso}
    [Wikipedia: Electrical resistance and conductance
       ](wiki:Electrical_resistance_and_conductance)
    :::
    """
    strict = False
    dimensionality = '[conductance]'


class ElectricCurrent(PhysicalDimension):
    """
    A measure for the net rate of flow of electric charge through a surface or into a control volume. It is one of the
    seven fundamental physical quantities in both the International System of Units (SI) and the International System of
    Quantities (ISQ). The SI base unit of time is the ampere (A).

    :::{seealso}
    [Wikipedia: Electric current](wiki:Electric_current)
    :::
    """
    strict = False
    dimensionality = '[current]'


class ElectricInductance(PhysicalDimension):
    """
    The ratio of the induced voltage to the rate of change of current causing it. The unit commonly used in the SI unit
    system is the henry (H).

    :::{seealso}
    [Wikipedia: Inductance](wiki:Inductance)
    :::
    """
    strict = False
    dimensionality = '[inductance]'


class ElectricPermittivity(PhysicalDimension):
    """
    A measure of the electric polarizability of a dielectric. TIn SI units, it is usually measured in farads per meter
    (F/m).

    :::{seealso}
    [Wikipedia: Permittivity](wiki:Permittivity)
    :::
    """
    strict = False
    dimensionality = '[capacitance] / [length]'


class ElectricPotential(PhysicalDimension):
    """
    A measure for the amount of work energy needed to move a unit of electric charge from a reference point to the
    specific point in an electric field. The unit commonly used in the SI unit system is the volt (V).

    :::{seealso}
    [Wikipedia: Electric potential](wiki:Electric_potential)
    :::
    """
    strict = False
    dimensionality = '[electric_potential]'


class ElectricResistance(PhysicalDimension):
    """
    A measure for the ease with which an electric current passes. Its reciprocal quantity is
    {py:class}`ElectricConductance`. The unit commonly used in the SI unit system is the ohm (Ω).

    :::{seealso}
    [Wikipedia: Electrical resistance and conductance
       ](wiki:Electrical_resistance_and_conductance)
    :::
    """
    strict = False
    dimensionality = '[resistance]'


class Energy(PhysicalDimension):
    """
    The quantitative property that is transferred to a body or to a physical system, recognizable in the performance of
    work and in the form of heat and light. The unit commonly used in the SI unit system is the joule (J).

    :::{seealso}
    [Wikipedia: Energy](wiki:Energy)
    :::
    """
    strict = False
    dimensionality = '[energy]'


class Entropy(PhysicalDimension):
    """
    A scientific concept, as well as a measurable physical property, that is most commonly associated with a state of
    disorder, randomness, or uncertainty. It has dimensions of energy divided by temperature. In SI units, it is usually
    measured in joules per kelvin (J/K).

    :::{seealso}
    [Wikipedia: Entropy](wiki:Entropy)
    :::
    """
    strict = False
    dimensionality = '[entropy]'


class Fluidity(PhysicalDimension):
    """
    The reciprocal of {py:class}`Viscosity`. In SI units, it is usually reciprocal poise (1/P), sometimes called the
    `rhe`.

    :::{seealso}
    [Wikipedia: Fluidity](wiki:Fluidity)
    :::
    """
    strict = False
    dimensionality = '[fluidity]'


class Force(PhysicalDimension):
    """
    An influence that can change the motion of an object. The unit commonly used in the SI unit system is the newton
    (N).

    :::{seealso}
    [Wikipedia: Force](wiki:Force)
    :::
    """
    strict = False
    dimensionality = '[force]'


class Frequency(PhysicalDimension):
    """
    Number of occurrences of a repeating event per unit of time. The unit commonly used in the SI unit system is the
    hertz (Hz).

    :::{seealso}
    [Wikipedia: Frequency](wiki:Frequency)
    :::
    """
    strict = False
    dimensionality = '[frequency]'


class Illuminance(PhysicalDimension):
    """
    A measure of how much the incident light illuminates the surface, wavelength-weighted by the luminosity function to
    correlate with human brightness perception. The unit commonly used in the SI unit system is the lux (lx).

    :::{seealso}
    [Wikipedia: Illuminance](wiki:Illuminance)
    :::
    """
    strict = False
    dimensionality = '[illuminance]'


class Impulse(PhysicalDimension):
    """
    The integral of a force over a time interval for which it acts. In SI units, it is usually measured in newton-
    seconds (N⋅s).

    :::{seealso}
    [Wikipedia: Impulse (physics)](wiki:Impulse_(physics))
    :::
    """
    strict = False
    dimensionality = '[length] * [mass] / [time]'


class Information(PhysicalDimension):
    """
    A measure for the capacity of some standard data storage system or communication channel. The unit commonly used in
    the SI unit system is the bit.

    :::{seealso}
    [Wikipedia: Units of information](wiki:Units_of_information)
    :::
    """
    strict = False
    dimensionality = '[]'


class InformationRate(PhysicalDimension):
    """
    A measure for the speed of data transmission. In SI units, it is usually measured in bits per second (bit/s).

    :::{seealso}
    [Wikipedia: Bit rate](wiki:Bit_rate)
    :::
    """
    strict = False
    dimensionality = '[frequency]'


class Intensity(PhysicalDimension):
    """
    A measure for the power transferred per unit area, where the area is measured on the plane perpendicular to the
    direction of propagation of the energy. In SI units, it is usually measured in watts per square meter (W/m²).

    :::{seealso}
    [Wikipedia: Intensity (physics)](wiki:Intensity_(physics))
    :::
    """
    strict = False
    dimensionality = '[intensity]'


class IonizingRadiation(PhysicalDimension):
    """
    A measure of the energy that is emitted by certain types of atomic nuclei or subatomic particles, such as alpha
    particles, beta particles, and gamma rays. The units commonly used in the SI unit system are the gray (Gy) and the
    sievert (Sv).

    :::{seealso}
    [Wikipedia: Ionizing radiation](wiki:Ionizing_radiation)
    :::
    """
    strict = False
    dimensionality = '[energy] / [mass]'


class KinematicViscosity(PhysicalDimension):
    """
    A measure of a fluid's resistance to flow. It is defined as the ratio of the dynamic viscosity of a fluid to its
    density. In SI units, it is usually measured in square meters per second (m^2/s).

    :::{seealso}
    [Wikipedia: Kinematic Viscosity](wiki:Viscosity#Kinematic_viscosity)
    :::
    """
    strict = False
    dimensionality = '[kinematic_viscosity]'


class Length(PhysicalDimension):
    """
    A measure of distance. It is one of the seven fundamental physical quantities in both the International System of
    Units (SI) and the International System of Quantities (ISQ). The SI base unit of time is the meter (m).

    :::{seealso}
    [Wikipedia: Length](wiki:Length)
    :::
    """
    strict = False
    dimensionality = '[length]'


class Luminance(PhysicalDimension):
    """
    A photometric measure of the luminous intensity per unit area of light travelling in a given direction. In SI units,
    it is usually measured in candela per square metre (cd/m²).

    :::{seealso}
    [Wikipedia: Luminance](wiki:Luminance)
    :::
    """
    strict = False
    dimensionality = '[luminance]'


class LuminousFlux(PhysicalDimension):
    """
    A measure of the perceived power of light. The unit commonly used in the SI unit system is the lumen (lm).

    :::{seealso}
    [Wikipedia: Luminous flux](wiki:Luminous_flux)
    :::
    """
    strict = False
    dimensionality = '[luminous_flux]'


class LuminousIntensity(PhysicalDimension):
    """
    A measure of the wavelength-weighted power emitted by a light source in a particular direction per unit solid angle,
    based on the luminosity function, a standardized model of the sensitivity of the human eye. It is one of the seven
    fundamental physical quantities in both the International System of Units (SI) and the International System of
    Quantities (ISQ). The SI base unit of time is the candela (cd).

    :::{seealso}
    [Wikipedia: Luminous intensity](wiki:Luminous_intensity)
    :::
    """
    strict = False
    dimensionality = '[luminosity]'


class MagneticFieldStrength(PhysicalDimension):
    """
    A measure of the intensity of a magnetic field. In SI units, it is usually measured in amperes per meter (A/m).

    :::{seealso}
    [Wikipedia: Magnetic field - The H-field](wiki:Magnetic_field#The_H-field)
    :::
    """
    strict = False
    dimensionality = '[magnetic_field_strength]'


class MagneticFlux(PhysicalDimension):
    """
    A measure of how many magnetic field lines are passing through a given surface area, that is, a measure of the
    strength of the magnetic field. The unit commonly used in the SI unit system is the weber (Wb).

    :::{seealso}
    [Wikipedia: Magnetic flux](wiki:Magnetic_flux)
    :::
    """
    strict = False
    dimensionality = '[magnetic_flux]'


class MagneticFluxDensity(PhysicalDimension):
    """
    A measure of the actual magnetic field within a material considered as a concentration of magnetic field lines, or
    flux, per unit cross-sectional area. It is also called the magnitude of the magnetic field. The unit commonly used
    in the SI unit system is the tesla (T).

    :::{seealso}
    [Wikipedia: Magnetic field - The B-field](wiki:Magnetic_field#The_B-field)
    :::
    """
    strict = False
    dimensionality = '[magnetic_field]'


class MagneticPermeability(PhysicalDimension):
    """
    A measure of magnetization that a material obtains in response to an applied magnetic field. In SI units, it is
    usually measured in henries per meter (H/m) or equivalently in newtons per ampere squared (N/A²).

    :::{seealso}
    [Wikipedia: Permeability (electromagnetism)
       ](wiki:Permeability_(electromagnetism))
    :::
    """
    strict = False
    dimensionality = '[inductance] / [length]'


class MagnetomotiveForce(PhysicalDimension):
    """
    The property of certain substances or phenomena that give rise to magnetic fields. The unit commonly used in the SI
    unit system is the ampere (A).

    :::{seealso}
    [Wikipedia: Magnetomotive force](wiki:Magnetomotive_force)
    :::
    """
    strict = False
    dimensionality = '[magnetomotive_force]'


class Mass(PhysicalDimension):
    """
    One of the seven fundamental physical quantities in both the International System of Units (SI) and the
    International System of Quantities (ISQ). The SI base unit of time is the kilogram (kg).

    :::{seealso}
    [Wikipedia: Mass](wiki:Mass)
    :::
    """
    strict = False
    dimensionality = '[mass]'


class MassFlowRate(PhysicalDimension):
    """
    A measure of how much mass of a substance passes per unit of time. In SI units, it is usually measured in kilograms
    per second (kg/s).

    :::{seealso}
    [Wikipedia: Mass flow rate](wiki:Mass_flow_rate)
    :::
    """
    strict = False
    dimensionality = '[mass] / [time]'


class MolarEntropy(PhysicalDimension):
    """
    A measure of entropy per mole. In SI units, it is usually measured in joules per mole per kelvin (J/(mol⋅K)).

    :::{seealso}
    [Wikipedia: Entropy](wiki:Entropy)
    :::
    """
    strict = False
    dimensionality = '[molar_entropy]'


class MomentOfInertia(PhysicalDimension):
    """
    A measure of how much torque is needed for a desired angular acceleration about a rotational axis, similar to how
    mass determines the force needed for a desired acceleration. It is also known as the rotational inertia. In SI
    units, it is usually measured in kilogram-square meters (kg⋅m²).

    :::{seealso}
    [Wikipedia: Moment of inertia](wiki:Moment_of_inertia)
    :::
    """
    strict = False
    dimensionality = '[mass] * [length] ** 2'


class Momentum(PhysicalDimension):
    """
    The product of the mass and velocity of an object. In SI units, it is usually measured in kilogram metre per second
    (kg⋅m/s), which is equivalent to the newton-second (N⋅s).

    :::{seealso}
    [Wikipedia: Momentum](wiki:Momentum)
    :::
    """
    strict = False
    dimensionality = '[momentum]'


class Power(PhysicalDimension):
    """
    The amount of energy transferred or converted per unit time. The unit commonly used in the SI unit system is the
    watt (W).

    :::{seealso}
    [Wikipedia: Power (physics)](wiki:Power_(physics))
    :::
    """
    strict = False
    dimensionality = '[power]'


class Pressure(PhysicalDimension):
    """
    The force applied perpendicular to the surface of an object per unit area over which that force is distributed. The
    unit commonly used in the SI unit system is the pascal (Pa).

    :::{seealso}
    [Wikipedia: Pressure](wiki:Pressure)
    :::
    """
    strict = False
    dimensionality = '[pressure]'


class Radiance(PhysicalDimension):
    """
    A measure of the radiant flux emitted, reflected, transmitted or received by a given surface, per unit solid angle
    per unit projected area. In SI units, it is usually measured in watts per steradian per square metre (W/(sr·m²)).

    :::{seealso}
    [Wikipedia: Radiance](wiki:Radiance)
    :::
    """
    strict = False
    dimensionality = '[power] / [length] ** 2'


class RadiantIntensity(PhysicalDimension):
    """
    A measure of the radiant flux emitted, reflected, transmitted or received, per unit solid angle. In SI units, it is
    usually measured in watts per steradian (W/sr).

    :::{seealso}
    [Wikipedia: Radiant intensity](wiki:Radiant_intensity)
    :::
    """
    strict = False
    dimensionality = '[power]'


class RadiationDoseAbsorbed(PhysicalDimension):
    """
    A measure for the amount of energy deposited per unit of mass. The unit commonly used in the SI unit system is the
    gray (Gy).

    :::{seealso}
    [Wikipedia: Absorbed dose](wiki:Absorbed_dose)
    :::
    """
    strict = False
    dimensionality = '[energy] / [mass]'


class RadiationDoseEffective(PhysicalDimension):
    """
    A measure for the effective dose of radiation received by a human or some other living organism. The unit commonly
    used in the SI unit system is the sievert (Sv).

    :::{seealso}
    [Wikipedia: Effective dose (radiation)](wiki:Effective_dose_(radiation))
    :::
    """
    strict = False
    dimensionality = '[energy] / [mass]'


class Radioactivity(PhysicalDimension):
    """
    A measure for the activity of a radioactive material in which one nucleus decays per unit of time. The unit commonly
    used in the SI unit system is the becquerel (Bq).

    :::{seealso}
    [Wikipedia: Radioactive decay](wiki:Radioactive_decay)
    :::
    """
    strict = False
    dimensionality = '[] / [time]'


class SolidAngle(PhysicalDimension):
    """
    A measure of the amount of the field of view from some particular point that a given object covers. The unit
    commonly used in the SI unit system is the steradian (sr).

    :::{seealso}
    [Wikipedia: Radioactive decay](wiki:Radioactive_decay)
    :::
    """
    strict = False
    dimensionality = '[]'


class SpecificHeatCapacity(PhysicalDimension):
    """
    A measure for the amount of heat energy required to raise the temperature of a substance per unit of mass. In SI
    units, it is usually measured in joules per kelvin per kilogram (J/(kg·K)).

    :::{seealso}
    [Wikipedia: Specific heat capacity](wiki:Specific_heat_capacity)
    :::
    """
    strict = False
    dimensionality = '[energy] / [mass] / [temperature]'


class Speed(PhysicalDimension):
    """
    The magnitude of the change of an object's position over time or the magnitude of the change of the object's
    position per unit of time. Speed is not the same as {py:class}`Velocity`, which is a vector quantity that has both
    magnitude and direction. In SI units, it is usually measured in meters per second (m/s).

    :::{seealso}
    [Wikipedia: Speed](wiki:Speed)
    :::
    """
    strict = False
    dimensionality = '[speed]'


class Temperature(PhysicalDimension):
    """
    A physical quantity that expresses quantitatively the perceptions of hotness and coldness. It is one of the seven
    fundamental physical quantities in both the International System of Units (SI) and the International System of
    Quantities. The SI base unit of time is the kelvin (K).

    :::{seealso}
    [Wikipedia: Temperature](wiki:Temperature)
    :::
    """
    strict = False
    dimensionality = '[temperature]'


class ThermalConductance(PhysicalDimension):
    """
    A measure of how much heat passes in unit time through a plate of particular area and thickness when its opposite
    faces differ in temperature by one kelvin. In SI units, it is usually measured in watts per kelvin (W/K).

    :::{seealso}
    [Wikipedia: Thermal conductivity](wiki:Thermal_conductivity)
    :::
    """
    strict = False
    dimensionality = '[power] / [temperature]'


class ThermalConductivity(PhysicalDimension):
    """
    A measure of a material's ability to conduct heat. In SI units, it is usually measured in watts per meter per kelvin
    (W/(m·K)).

    :::{seealso}
    [Wikipedia: Thermal conductivity](wiki:Thermal_conductivity)
    :::
    """
    strict = False
    dimensionality = '[power] / ([length] * [temperature])'


class ThermalInsulance(PhysicalDimension):
    """
    A measure of how well a two-dimensional barrier, such as a layer of insulation, a window or a complete wall or
    ceiling, resists the conductive flow of heat. In SI units, it is usually measured in square meter-kelvins per watt
    (K·m²/W).

    :::{seealso}
    [Wikipedia: R-value (insulation)](wiki:R-value_%28insulation%29)
    :::
    """
    strict = False
    dimensionality = '[temperature] * [length] ** 2 / [power]'


class ThermalResistance(PhysicalDimension):
    """
    The inverse of thermal conductance. It is a convenient measure to use in multi-component design since thermal
    resistances are additive when occurring in series. In SI units, it is usually measured in kelvins per watt (K/W).

    :::{seealso}
    [Wikipedia: Thermal conductivity](wiki:Thermal_conductivity)
    :::
    """
    strict = False
    dimensionality = '[temperature] / [power]'


class ThermalResistivity(PhysicalDimension):
    """
    The reciprocal of {py:class}`ThermalConductivity`. It is a measure of a material's ability to resists the conductive
    flow of heat. TIn SI units, it is usually measured in kelvin-meters per watt (m·K)/W).

    :::{seealso}
    [Wikipedia: Thermal conductivity](wiki:Thermal_conductivity)
    :::
    """
    strict = False
    dimensionality = '[length] * [temperature] / [power]'


class ThermalTransmittance(PhysicalDimension):
    """
    A measure for the rate of transfer of heat through matter, typically expressed as a U-value. In SI units, it is
    usually measured in watts per square metre per kelvin (W/(m²·K)).

    :::{seealso}
    [Wikipedia: Thermal transmittance](wiki:Thermal_transmittance)
    :::
    """
    strict = False
    dimensionality = '[power] / ([length] ** 2 * [temperature])'


class Time(PhysicalDimension):
    """
    One of the seven fundamental physical quantities in both the International System of Units (SI) and the
    International System of Quantities (ISQ). The SI base unit of time is the second (s).

    :::{seealso}
    [Wikipedia: Time](wiki:Time)
    :::
    """
    strict = False
    dimensionality = '[time]'


class Torque(PhysicalDimension):
    """
    The rotational equivalent of linear {py:class}`Force`. In SI units, it is usually measured in newton-meters (N·m).

    :::{seealso}
    [Wikipedia: Torque](wiki:Torque)
    :::
    """
    strict = False
    dimensionality = '[torque]'


class Velocity(PhysicalDimension):
    """
    The directional speed of an object in motion as an indication of its rate of change in position as observed from a
    particular frame of reference and as measured by a particular standard of time. It is a physical vector quantity.
    Hence, both magnitude and direction are needed to define it. The scalar absolute value (magnitude) of velocity is
    {py:class}`Speed`. In SI units, it is usually measured in meters per second (m/s).

    :::{seealso}
    [Wikipedia: Velocity](wiki:Velocity)
    :::
    """
    strict = False
    dimensionality = '[velocity]'


class Viscosity(PhysicalDimension):
    """
    A measure of a fluid's resistance to deformation at a given rate. The unit commonly used in the SI unit system is
    the poise (P).

    :::{seealso}
    [Wikipedia: Viscosity](wiki:Viscosity)
    :::
    """
    strict = False
    dimensionality = '[viscosity]'


class Volume(PhysicalDimension):
    """
    A measure of three-dimensional space. In SI units, it is usually measured in cubic meters (m3).

    :::{seealso}
    [Wikipedia: Volume](wiki:Volume)
    :::
    """
    strict = False
    dimensionality = '[volume]'


class VolumetricFlowRate(PhysicalDimension):
    """
    The volume of fluid that passes per unit time. It is also known as volume flow rate, or volume velocity. In SI
    units, it is usually measured in cubic metres per second (m3/s).

    :::{seealso}
    [Wikipedia: Volumetric flow rate](wiki:Volumetric_flow_rate)
    :::
    """
    strict = False
    dimensionality = '[volumetric_flow_rate]'


class WaveNumber(PhysicalDimension):
    """
    The spatial frequency of a wave, measured in cycles per unit distance. SI units, it is usually measured in
    reciprocal of meters (1/m).

    :::{seealso}
    [Wikipedia: Wavenumber](wiki:Wavenumber)
    :::
    """
    strict = False
    dimensionality = '[wavenumber]'
