"""Evolutionary histories, events and costs."""


class GeneEvent:
    pass


class SegmentEvent:
    genes: list[str]


class Event(Enum):
    """Types of evolutionary events acting on genes or segments of genes."""

    # Sentinel event for leaves
    Extant = auto()

    # Gene or segment follows the speciation of its host
    Speciation = auto()

    # Gene or segment is duplicated into two copies
    Duplication = auto()

    # Segment is cut into two segments
    Cut = auto()

    # Gene or segment is transfered towards a foreign genome
    Transfer = auto()

    # Part of a segment is cut towards a foreign genome
    TransferCut = auto()

    # New gene or gene segment appears
    Gain = auto()

    # Gene or segment is lost
    Loss = auto()
