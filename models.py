from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = info['pdes']
        if info['name'] == '':
            self.name = None
        else:
            self.name = info['name']
        if info['diameter'] == '':
            self.diameter = float('nan')
        else:
            self.diameter = float(info['diameter'])
        if info['pha'] == 'Y':
            self.hazardous = True
        else:
            self.hazardous = False
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name is not None:
            return str(self.designation) + ' ' + str(self.name)
        else:
            return str(self.designation)

    def __str__(self):
        """Return `str(self)`."""
        if self.hazardous is False:
            return f"NEO {self.fullname} has a diameter of {self.diameter:.3f} \
            km and is not potentially hazardous"
        elif self.hazardous is True:
            return f"NEO {self.fullname} has a diameter of {self.diameter:.3f} \
            km and is potentially hazardous"
        else:
            f"NEO {self.fullname} has a diameter of {self.diameter:.3f} \
            km and its potential hazardous is unknown"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, \
        name={self.name!r}, "f"diameter={self.diameter:.3f}, \
        hazardous={self.hazardous!r})")


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, info, neo: NearEarthObject = None):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = info[0]
        self.time = cd_to_datetime(info[3])
        self.distance = float(info[4])
        self.velocity = float(info[7])
        self.neo = neo

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return (f"On {self.time} {self.neo.fullname} approaches Earth at a distance of "
                f"{self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s")

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")