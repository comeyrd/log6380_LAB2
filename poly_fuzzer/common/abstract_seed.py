class AbstractSeed:
    """Represent an seed with additional attributes, such as energy.
    It is necessary to create a power schedule that assigns energy to seeds.
    """

    def __init__(self, data: str,coverage=0,energy=0.0,execution_time=0) -> None:
        """Initialize from seed data"""
        self.data = data

        self.coverage = coverage
        self.energy = energy
        self.execution_time = execution_time

    def __str__(self) -> str:
        """Returns data as string representation of the seed"""
        return self.data
