import itertools
import operator
from models import CloseApproach


class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""


class AttributeFilter:
    """A general superclass for filters on comparable attributes.

    An `AttributeFilter` represents the search criteria pattern comparing some
    attribute of a close approach (or its attached NEO) to a reference value. It
    essentially functions as a callable predicate for whether a `CloseApproach`
    object satisfies the encoded criterion.

    It is constructed with a comparator operator and a reference value, and
    calling the filter (with __call__) executes `get(approach) OP value` (in
    infix notation).

    Concrete subclasses can override the `get` classmethod to provide custom
    behavior to fetch a desired attribute from the given `CloseApproach`.
    """

    def __init__(self, op, value):
        """Construct a new `AttributeFilter` from an binary predicate and a reference value.

        The reference value will be supplied as the second (right-hand side)
        argument to the operator function. For example, an `AttributeFilter`
        with `op=operator.le` and `value=10` will, when called on an approach,
        evaluate `some_attribute <= 10`.

        :param op: A 2-argument predicate comparator (such as `operator.le`).
        :param value: The reference value to compare against.
        """
        self.op = op
        self.value = value

    def __call__(self, approach):
        """Invoke `self(approach)`."""
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """Get an attribute of interest from a close approach.

        Concrete subclasses must override this method to get an attribute of
        interest from the supplied `CloseApproach`.

        :param approach: A `CloseApproach` on which to evaluate this filter.
        :return: The value of an attribute of interest, comparable to `self.value` via `self.op`.
        """
        raise UnsupportedCriterionError

    def __repr__(self):
        return f"{self.__class__.__name__} \
        (op=operator.{self.op.__name__}, value={self.value})"


class DateFilter(AttributeFilter):
    """A subclass of AttributeFilter class to filter `CloseApproach` based on date. """

    @classmethod
    def get(cls, approach: CloseApproach):
        """Get a date attribute from a close approach. """
        return approach.time.date()


class DistanceFilter(AttributeFilter):
    """A subclass of AttributeFilter class to filter `CloseApproach` based on distance. """

    @classmethod
    def get(cls, approach: CloseApproach):
        """Get a distance attribute from a close approach. """
        return approach.distance


class VelocityFilter(AttributeFilter):
    """A subclass of AttributeFilter class to filter `CloseApproach` based on velocity. """

    @classmethod
    def get(cls, approach: CloseApproach):
        """Get a velocity attribute from a close approach. """
        return approach.velocity


class DiameterFilter(AttributeFilter):
    """A subclass of AttributeFilter class to filter `CloseApproach` based on diameter. """

    @classmethod
    def get(cls, approach: CloseApproach):
        """Get a diameter attribute from a close approach. """
        return approach.neo.diameter


class HazardousFilter(AttributeFilter):
    """A subclass of AttributeFilter class to filter `CloseApproach` based on hazardous. """

    @classmethod
    def get(cls, approach: CloseApproach):
        """Get a hazardous attribute from a close approach. """
        return approach.neo.hazardous


def create_filters(date=None, start_date=None, end_date=None,
                   distance_min=None, distance_max=None,
                   velocity_min=None, velocity_max=None,
                   diameter_min=None, diameter_max=None,
                   hazardous=None):
    """Create a collection of filters from user-specified criteria.

    Each of these arguments is provided by the main module with a value from the
    user's options at the command line. Each one corresponds to a different type
    of filter. For example, the `--date` option corresponds to the `date`
    argument, and represents a filter that selects close approaches that occured
    on exactly that given date. Similarly, the `--min-distance` option
    corresponds to the `distance_min` argument, and represents a filter that
    selects close approaches whose nominal approach distance is at least that
    far away from Earth. Each option is `None` if not specified at the command
    line (in particular, this means that the `--not-hazardous` flag results in
    `hazardous=False`, not to be confused with `hazardous=None`).

    The return value must be compatible with the `query` method of `NEODatabase`
    because the main module directly passes this result to that method. For now,
    this can be thought of as a collection of `AttributeFilter`s.

    :param date: A `date` on which a matching `CloseApproach` occurs.
    :param start_date: A `date` on or after which a matching `CloseApproach` occurs.
    :param end_date: A `date` on or before which a matching `CloseApproach` occurs.
    :param distance_min: A minimum nominal approach distance for a matching `CloseApproach`.
    :param distance_max: A maximum nominal approach distance for a matching `CloseApproach`.
    :param velocity_min: A minimum relative approach velocity for a matching `CloseApproach`.
    :param velocity_max: A maximum relative approach velocity for a matching `CloseApproach`.
    :param diameter_min: A minimum diameter of the NEO of a matching `CloseApproach`.
    :param diameter_max: A maximum diameter of the NEO of a matching `CloseApproach`.
    :param hazardous: Whether the NEO of a matching `CloseApproach` is potentially hazardous.
    :return: A collection of filters for use with `query`.
    """
    filters = set()
    if date is not None:
        date_filter = DateFilter(operator.eq, date)
        filters.add(date_filter)
    if start_date is not None:
        start_date_filter = DateFilter(operator.ge, start_date)
        filters.add(start_date_filter)
    if end_date is not None:
        end_date_filter = DateFilter(operator.le, end_date)
        filters.add(end_date_filter)
    if distance_min is not None:
        distance_min_filter = DistanceFilter(operator.ge, distance_min)
        filters.add(distance_min_filter)
    if distance_max is not None:
        distance_max_filter = DistanceFilter(operator.le, distance_max)
        filters.add(distance_max_filter)
    if velocity_min is not None:
        velocity_min_filter = VelocityFilter(operator.ge, velocity_min)
        filters.add(velocity_min_filter)
    if velocity_max is not None:
        velocity_max_filter = VelocityFilter(operator.le, velocity_max)
        filters.add(velocity_max_filter)
    if diameter_min is not None:
        diameter_min_filter = DiameterFilter(operator.ge, diameter_min)
        filters.add(diameter_min_filter)
    if diameter_max is not None:
        diameter_max_filter = DiameterFilter(operator.le, diameter_max)
        filters.add(diameter_max_filter)
    if hazardous is not None:
        hazardous_filter = HazardousFilter(operator.eq, hazardous)
        filters.add(hazardous_filter)
    return filters


def limit(iterator, n=None):
    """Produce a limited stream of values from an iterator.

    If `n` is 0 or None, don't limit the iterator at all.

    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :yield: The first (at most) `n` values from the iterator.
    """
    if n is None or n == 0:
        return iterator
    else:
        return itertools.islice(iterator, n)