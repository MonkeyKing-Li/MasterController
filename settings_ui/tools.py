import multiprocessing


class StoppableProcess(multiprocessing.Process):
    """Process class with a stop() method. The process itself has to check
    regularly for the running() condition.
    """

    def __init__(self, *args, **kwargs):
        super(StoppableProcess, self).__init__(*args, **kwargs)
        self._stopper = multiprocessing.Event()

    def stop(self):
        """Stop the process."""
        self._stopper.set()

    def running(self):
        """Test if the process is currently running."""
        return not self._stopper.is_set()

    def stopped(self):
        """Test if the process is stopped."""
        return self._stopper.is_set()
