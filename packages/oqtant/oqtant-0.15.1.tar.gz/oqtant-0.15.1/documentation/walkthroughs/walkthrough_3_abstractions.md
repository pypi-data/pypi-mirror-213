## Imports


```python
%matplotlib inline
from bert_schemas import job as JobSchema
```

## Oqtant jobs and their constituent primitives

In this walkthrough, we will explore the structure of jobs that you submit to Oqtant. In an earlier walkthrough, we saw that a basic BEC job could be defined by a dictionary structure like

```python
default_bec_job_data = {
    "name": "Example BEC Job",
    "job_type": "BEC",
    "inputs": [
        {
            "values": {
                "time_of_flight_ms": 8.0,
                "image_type": "TIME_OF_FLIGHT",
                "end_time_ms": 0.0,
                "rf_evaporation": {
                    "frequencies_mhz": [17.0, 8.0, 4.0, 1.2, 0.045],
                    "powers_mw": [500.0, 500.0, 475.0, 360.0, 220.0],
                    "interpolation": "LINEAR",
                    "times_ms": [-1600, -1200, -800, -400, 0]
                },
                "optical_barriers": None,
                "optical_landscape": None,
                "lasers": None
            }
        }
    ]
}
```

We could then feed the above data structure to the API's _generate_oqtant_job()_ function to create the job object. Here, we would like to explore the contents of the underlying job data structure more in depth. The fields that control the behavior of the quantum matter machine are contained as _values_ in the _inputs_ list ([]). For now, we will only discuss cases where the _inputs_ list contains a single element. When this list's length is greater than one, it signifies a so-called _batch_ job, which will be discussed in a later walkthrough.

The contents of *values* includes directives on the type of imaging to perform (*image_type* etc.) and how long to run the experiment (*end_time_ms*) after evaporation to BEC is complete.  Also included are various job primitives that can be created and edited as programmable objects in their own right.  These primitives include *rf_evaporation*, *optical_barriers*, *optical_landscape*, and *lasers*.  Much like an *OqtantJob* itself, these constituent primitives are programmatic objects in their own right and can be instantiated and manipulated outside of a job object.  Although not shown explicitly in our simple job data structure above, both *optical_barriers* and *lasers* are lists containing *Barrier* and *Laser* objects, respectively.  These objects will be explored below.  You are likely already familiar with the structure of the *rf_evaporation* data and how defining that data controls the evaporation to BEC in the experiment.  The *optical_landscape* data is a bit more complicated and will be explored in more detail below in a dedicated section.       

Not all job types support every one of these data structures.  For the basic BEC-type job above, we did not have data entries for barriers, the landscape, or lasers.  BEC jobs, for instance, only support the rf_evaporation primitive.  After all, the purpose of a BEC job is to keep things simple and just focus on the ability to tune the creation of the condensate.  At the next level of complexity, BARRIER jobs support both *rf_evaporation* and *optical_barriers* but not "optical_landscape" or "lasers".  What data structures are supported by different job types will become clear as those job types are created/used/submitted.  As a preview, please refer to the following table.

| Job type   | Supports       |                  |                   |        |
|------------|----------------|------------------|-------------------|--------|
|            | rf_evaporation | optical_barriers | optical_landscape | lasers |
| BEC        |                |                  |                   |        |
| BARRIER    | X              | X                |                   |        |
| TRANSISTOR | X              | X                | X                 | X      |
| PAINT_1D   | X              | X                | X                 | X      |

Please note that not all these job types are yet available at the time of this writing.

## The RfEvaporation Object

Every job input has exactly one constituent RfEvaporation object defined by the "rf_evaporation" data shown above.  The behavior of this object controls the RF knife evaporation from an ultracold gas to Bose-Einstein condensate (BEC), as well as providing flexibility for applying RF fields during the experiment phase after the initial evaporation is complete.  The evaporation stage results in a tradeoff between final atom number and temperature -- evaporating more deeply, signified by RF detuning values closer to 0, produces less atoms but at colder temperature (and correspondingly higher condensate fraction).  Applying RF radiation during the experiment phase allows for hot atoms above some temperature, produced for example by rapid manipulation of optical barries or landscape potentials (explored below), to be removed the experiment -- a so-called "RF shield". 

It is important to note here that we adopt the convention that time = 0 refers to the *end* of the evaporation period.  As such, the initial evaporation to BEC, as defined by the object under current inspection, will involve negative (relative) times.  In our trap, the entire evaporation cycle takes on the order of a second, and times are specified in ms, so we should see negative times as large as a few thousand ms.   

### Construction

Let us begin by constructing a stand-alone RfEvaporation object completely independently of any specific Oqtant job.  We can create this object by either calling the constructor directly with the required data fields:


```python
evap = JobSchema.RfEvaporation(
        times_ms = [-1600, -1200, -800, -400, 0],
        frequencies_mhz = [17.0, 8.0, 4.0, 1.2, 0.045],
        powers_mw = [500.0, 500.0, 475.0, 360.0, 220.0],
        interpolation = "LINEAR"
)
```

or by placing the underlying data in a dictionary and unpacking that dictionary in order to pass it to the constructor:


```python
evap = JobSchema.RfEvaporation(**{
        "times_ms": [-1600, -1200, -800, -400, 0],
        "frequencies_mhz": [17.0, 8.0, 4.0, 1.2, 0.045],
        "powers_mw": [500.0, 490.0, 475.0, 360.0, 220.0],
        "interpolation": "LINEAR"
})
```

Inherent to the RfEvaporation object are three lists, *times_ms*, *frequencies_mhz*, and *powers_mw*.  The key prefix corresponds to the parameter being controlled, while the suffix refers to the associated units.  In this case, we specify a list of times in milliseconds (ms), frequencies in MHz (mhz), and powers in milliwatts (mw).  Note that all units are lower case, which can cause confusion if taken out of context.  All three lists must share the same length as each time element is paired with the corresponding element of the frequencies/powers list(s).  The specified behavior of the RF evaporation stage defind by the above data is as follows: At -1.6 seconds the RF power is set at 500 mW and the frequency (detuning) at 17 MHz.  By the end of the evaporation period, defined by t=0, the frequency/detuning has decreased to 0.045 MHz = 45 kHz and the power has been reduced to 220 mW.  Intermediate values of frequency and power are adopted between those two points in time, with the full time dependence being a result of the given data and chosen interpolation type, which controls how the RF fields behave between the given data points.      

Frequencies are given as a detuning with respect to the energetic trap bottom, so RF fields at a frequency/detuning of 0 would eliminate all atoms from the trap.  Achieving final BEC temperatures on the order of 100 nK usually corresponds to final RF frequencies of a few tens of kHz.  Powers refer to the amount of power delivered to an antenna that bathes the ultracold atoms with RF radiation.  The actual local RF field experienced by the atoms depends on system losses and the exact geometry of the antenna.      

### Time-dependent evaporation parameters

We can explore the time-dependence of the RFEvaporation object frequency and power, as defined by the data structure above, using some useful functions included with oqtant.  For example, we can query the object for the instantaneous power or frequency at any point in time.  Recall that the units of power are mW and the units of frequency are MHz.


```python
print(evap.get_power(time = -100))
print(evap.get_frequency(time = -750))
```

If we request the power or frequency for a time value outside the range of the underlying data, which would require extrapolation, we get 0.0:


```python
print(evap.get_power(time = 100))           # request after last defined object time of 0 ms -> 0.0
print(evap.get_frequency(time = -1800))     # request before first defined object time of -1600 ms -> 0.0
```

This behavior is generic to most objects in oqtant -- any temporal or spatial extrapolation requests yield 0.0.  

There are also functions that extract the time-dependent parameters for a list of input times:


```python
print(evap.get_powers(times = [-1600, -1000, -500, 0]))
print(evap.get_frequencies(times = [-1600, -1000, -600, 0]))
```

There are even useful plotting functions for visualizing these parameters over time.


```python
evap.plot_power()
evap.plot_frequency()
```

## Barrier Objects

  

### Construction

First, let us demonstrate the construction of a Barrier object, which represents a one-dimensional optical potential barrier to the BEC.  A barrier is characterized by a shape, a time-dependent position, height, and width, and information on how to interpolate over the underlying data in time.  For example, let us construct a Barrier object named *barr* for which the center scans from 1-11 microns in the first 10 ms of an experiment.  Over this same time period, the barrier height will increase from 1 kHz to 11 kHz.  The width will remain constant at 1 micron throughout, as will the (fixed) Gaussian shape.  In this case, the width parameter corresponds to the Gaussian width of the barrier.


```python
barr = JobSchema.Barrier(
    times_ms = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
    positions_um = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    heights_khz = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    widths_um = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    interpolation = 'LINEAR',
    shape = 'GAUSSIAN'
)
```

Alternatively, as above, we can create the same object by generating the underlying data in a dictionary and then unpacking that dictionary (using the ** prefix) when we pass it to the Barrier class constructor:


```python
barr = JobSchema.Barrier(**{
    "times_ms": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
    "positions_um": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 
    "heights_khz": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 
    "widths_um": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
    "interpolation": "LINEAR", 
    "shape": "GAUSSIAN"
})
```

The lists of time-dependent quantities (position, height, and width) used to define *barr* must have the same length as the corresponding list of times.  In this case, the ordered pairs consisting of a list of, e.g., [times, positions], will be linearly interpolated in time.  

### Time-dependent barrier parameters

We can explore the time-dependence of the barrier parameters using some in-built functions in pyubert.  For example, we can retrieve and/or plot the barriers positions over time:


```python
print(barr.get_position(time = 2))
print(barr.get_positions(times = [1,2,3]))
```

Similarly, there are native functions for extracting a Barrier objects height and width at specified time(s).  In our case, the width evolution is trivial (constant).


```python
print(barr.get_height(1.5))
print(barr.get_heights([1.5, 2.5, 3.5]))

print(barr.get_width(1.5))
print(barr.get_widths([1.5, 2.5, 3.5]))
```

As well as methods for extracting the time-dependent parameters of the barrier, we can also use some in-built plotting functions.  In the examples below, you can see the underlying data points (that we used to define the Barrier object) as points, with the full dynamics of the barrier parameters over time determined by the interpolation style and indicated by a solid line. In an actual experiment, the barrier positions are updated every 100 microseconds, so the time-dependent barrier parameters will only approximately follow the idealized interpolated line.   


```python
barr.plot_position()
barr.plot_height()
barr.plot_width()
```

### Plotting the potential energy for a barrier  

There are also methods native to oqtant for plotting Barrier object potential energies at different times of the experiment.  Here, we will explicitly specify the positional range of the plot (x-axis domain) in order to better be able to see the barrier displacement. 


```python
xlim = [-5, 15]
ylim = [0, 12.5]
barr.plot_potential(time = 1, x_limits = xlim, y_limits = ylim)
barr.plot_potential(time = 5, x_limits = xlim, y_limits = ylim)
barr.plot_potential(time = 9, x_limits = xlim, y_limits = ylim)
```

### Exploring Barrier shape options

Supported Barrier shape options include GAUSSIAN, SQUARE, and LORENTZIAN.  In all three cases, the "width_um" parameter list means something slightly different.  For the GAUSSIAN case, the functional form of the barrier potential $U(x)$ follows the standard Gaussian formula
$$
U(x) = H e^{-\frac{(x - x_0)^2}{2 w^2}} \quad \textrm{(GAUSSIAN)}
$$
where $H=H(t)$, $x_{0} = x_{0}(t)$, and $w = w(t)$ represent the time-dependent barrier height, center position, and width, respectively.  In this case, our width parameter corresponds to the traditional definition of the Gaussian width, often denoted as $\sigma$.    

For the LORENTZIAN case, the potential follows
$$
U(x) = \frac{H}{1 + (x - x_0)^{2} / w^{2}} \quad \textrm{(LORENTZIAN)},
$$
i.e. our width parameter w(t) corresponds to the half-width half-max of the Lorentzian.

For the SQUARE case, the potential is simple a flat-topped potential-energy hill of height H(t) and *full* width w(t).  


```python
barr.shape = JobSchema.ShapeType.SQUARE
barr.plot_potential(time = 5, x_limits = [-25,25])

barr.shape = JobSchema.ShapeType.LORENTZIAN
barr.plot_potential(time = 5, x_limits = [-25,25])
```

Note that the resolution of the projected light optical system is on the order of 2 microns.  Thus, *Barrier* objects with small widths will all appear similar in reality (the experiment) even if they have different *shape* settings.

### Exploring Barrier interpolation options

A Barrier object's 'interpolation' style determines how the time-dependent position, height, and width are determined for intermediate times between the provided data points in the 'times_ms' list class member. At this time, the interpolation choice is *shared* for all three time-dependent barrier parameters.  Let us explore the effects of different interpolation choices by altering the time-dependent position of our barrier, to make it a little more interesting, and then plot the position over time for a few different interpolation choices.  


```python
barr.positions_um = [2, 4, 6, 8, 10, 2, 4, 6, 8, 6, 4]

barr.interpolation = JobSchema.InterpolationType.STEP
barr.plot_position()

barr.interpolation = JobSchema.InterpolationType.CUBIC
barr.plot_position()
```

As you can see above, 'STEP' style interpolation gives a "jumpy" barrier that changes position at discrete times.  Other interpolation options, like 'SMOOTH' (which is functionally equivalent to 'CUBIC'), give rise to a continually varying barrier position (and height/width).  The full list of interpolation options is as follows:


```python
print([e.value for e in JobSchema.InterpolationType])
```

## The Optical Landscape Object

Another Oqtant job primitive is the (singular) 'OpticalLandscape' object.  This construct is similar to the optical barriers list in the sense that it instructs the experiment to apply 1D optical potentials, in the form of painted blue-detuned light, to the condensate over the course of the experiment.  However, now the user (you!) is free to specify a list of positions and corresponding potential energies at specified times, instead of being limited to the concept of a singular barrier or combination of multiple barriers.    

The OpticalLandscape object consists of a list of individual potential-energy landscapes and an interpolation option on how those landscapes connect together *in time* (if there exists more than one underlying landscape).  Let us begin by constructing a couple Landscape objects, from which we will compose the OpticalLandscape container object.   

### Construction

We can directly compose an *OpticalLandscape* object, as above with the *Barrier* object(s), or we can compose the constituent Landscape objects and then compose the full *OpticalLandscape* object accordingly:


```python
landscape_1 = JobSchema.Landscape(
    time_ms = 1.0,
    positions_um = [-50, -25, 0, 25, 50],
    potentials_khz = [100, 50, 0, 50, 100],
    spatial_interpolation = 'LINEAR'
)

landscape_2 = JobSchema.Landscape(
    time_ms = 10.0,
    positions_um = [-50, -25, 0, 25, 50],
    potentials_khz = [25, 12.5, 0, 12.5, 25],
    spatial_interpolation = 'LINEAR'
)

optical_landscape = JobSchema.OpticalLandscape(
    interpolation = 'LINEAR',
    landscapes = [landscape_1, landscape_2]
)
```

### Inspecting consituent 'Landscape' objects


```python
print(landscape_1.get_potential_at_position(10))
print(landscape_2.get_potential_at_positions([-75, -50, -25, 0, 25, 50, 75]))
```


```python
landscape_1.plot_potential()
landscape_2.plot_potential(y_limits = [-1, 101])
```

In the plots above, you can see the potential energy profile specified by our two Landscape objects.  The underlying data shows up as points, with the overall profile determined by the values of these points and the chosen value for *spatial_interpolation*.  The same values are available here as were for (temporal) interpolation options for Barrier objects.  

### Understanding the time dependence of the composed OpticalLandscape object

The time-dependence of the overall optical potential-energy landscape, as derived from the individual *landscapes[]* list, is somewhat complicated.  As for *Barrier* and other similar objects, any temporal extrapolation (behavior for data outside the defined time period, i.e. before the first or after the last elements of the *landscapes[]* list) results in zero potential  (in the absence of any other sources, such as Barriers).  Therefore, the only way to get a non-zero painted potential optical landscape is to define at least two landscapes that can be interpolated between.  To hold a static (unchanging) potential during a period of the experiment, one would define two elements of the *landscapes[]* list with identical potential energy profiles but differing times, with the potential being applied between those two times.  If one desires the potential to change dynamically, then adjacent elements of the *landscapes[]* list (elements with the nearest *time_ms* values) should define the snapshots of the desired potential at the temporal endpoints.  In between these endpoints the potential landscape is interpolated point-by-point (in position) according to the user-specified value for *interpolation*.  This process continues so that, at the specified times of the elements of *landscapes[]*, the overall optical potential energy landscape instantaneously equal to those individual landscapes.  

In our example above, with linear interpolation, this means that there will be a period of no optical potential between 0 and 1 ms, our *landscape_1* potential will start being applied at 1 ms, this potential will smoothly (linearly, in this case) morph into the *landscape_2* potential between 1 and 10 ms, and then this potential landscape will be held until the end of the experiment.  Let us use oqtant's visualization functions to inspect this behavior to make it clear.       


```python
optical_landscape.plot_potential(time = 0.9)
optical_landscape.plot_potential(time = 1)
optical_landscape.plot_potential(time = 3)
optical_landscape.plot_potential(time = 5)
optical_landscape.plot_potential(time = 7)
optical_landscape.plot_potential(time = 9)
optical_landscape.plot_potential(time = 11)
```

As descibed above, we can see zero overall potential both before the first and after the last times of the individual Landscape objects.  At 1 ms, the first Landscape is assumed.  The potential landscape then morphs into our second Landscape object at t = 10 ms.  

## Laser Objects 

The last data structure to explore here is the *lasers[]* list in the job data.  This is a list of *Laser* objects.  Currently, the user is limited to a single element/laser.  

### Construction

Let us begin by constructing a *Laser* object, which gives the user control over near-resonant laser light applied to the atoms over the course of the experiment.  This differs from the painted potential laser, which is far off-resonance in order to apply potential energy landscapes and barriers to the trapped condensate.  Resonant or near-resonant light, on the other hand, results in scattering of photons from the light field by the atoms.  This is useful, for example, in TRANSISTOR jobs where we want to remove atoms from some spatial region of the trap using a so-called TERMINATOR laser.  

A *Laser* object gives the user control of the time-dependence of laser light applied to the atomic ensemble, including the time-dependent intensity and detuning given by a series of *pulse* objects specified by a *pulses[]* list.  We can construct such an object as follows:


```python
pulse_1 = JobSchema.Pulse(
    times_ms = [1, 1.5, 2, 3],
    intensities_mw_per_cm2 = [0, 10, 2, 0],
    detuning_mhz = 5,
    interpolation = 'SMOOTH'
)

pulse_2 = JobSchema.Pulse(
    times_ms = [5, 6, 7],
    intensities_mw_per_cm2 = [10, 5, 0],
    detuning_mhz = -10,
    interpolation = 'LINEAR'
)

pulse_3 = JobSchema.Pulse(
    times_ms = [9, 10, 11, 12],
    intensities_mw_per_cm2 = [0, 2.5, 2.5, 0],
    detuning_mhz = -5,
    interpolation = 'STEP'
)

laser = JobSchema.Laser(
    type = 'TERMINATOR',
    pulses = [pulse_1, pulse_2, pulse_3]
)
```


```python
laser.plot_intensity()
```
