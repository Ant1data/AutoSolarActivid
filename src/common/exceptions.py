class NoDataFoundError(Exception):
    """Exception class raised when no data for Solar Activity or Particle Flux Graph is found."""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        print('tacos')