from collections import deque
import multiprocessing as mp
from sys import version_info
import time
import os

if not os.name == 'nt':
    mp.set_start_method("fork")


class BSPObject:
    """The main BSP object that enables use of BSP

    This class keeps track of communication lines, its pid and the total cores
    it also enables the use of BSP functions through these variables. This is
    a low level object which the end user should not need to call directly.

    Parameters
    ----------
    cores : int
        The total number of cores in this BSP instance.
    pid : int
        This processor's id. It always holds that 0 <= pid < cores.
    processor_queues : List[mp.Queue]
        A connection to every other processor. Should be given
        through the run() function.
    barrier : barrier
        The barrier object all processors adhere to.

    Attributes
    ----------
    cores : int
        The total number of cores in this BSP instance (run).
    pid : int
        This processor's id. It always holds that 0 <= pid < cores"""

    def __init__(self, cores, pid, processor_queues, barrier):
        # These should be static
        self._queues = processor_queues
        self._barrier = barrier

        self.cores = cores
        self.pid = pid

        # This is expected to be dynamic and change.
        self._to_send_queues = [deque() for _ in range(cores)]

    def _clear_to_send(self):
        """Clears the _to_send dictionary.

        Should not be used by the end user in normal operation.

        Returns
        -------
        out : None"""
        for queue in self._to_send_queues:
            queue.clear()

    def _clear_receive_queue(self):
        while not self._queues[self.pid].empty():
            self._queues[self.pid].get()

    def sync(self):
        """sync()

        Starts the synchronisation defined in the BSP model. A synchronisation
        consists of 3 distinct steps:
        1) Wait for all processing nodes to finish computing
        2) Send all messages that have queued up since the last sync
        3) Receive all messages that have been sent in the previous step.
        After sync() has completed, every processor will have access to the data that
        has been sent to it.

        Returns
        -------
        out : None"""

        # Ensure every processor is done doing what it was doing before
        self._barrier.wait()

        # Flush existing data from receive queues
        self._clear_receive_queue()
        self._barrier.wait()

        # Send all data
        for i, send_queue in enumerate(self._to_send_queues):
            # Pick the right communication line
            comm_line = self._queues[i]

            # Until the send_queue is empty
            while send_queue:
                # Pop the first message in send_queue, and send it.
                message = send_queue.popleft()
                comm_line.put(message)

        # Clear _to_send_dict
        self._clear_to_send()

        # Ensure getting is done
        self._barrier.wait()
        # Everyone is released and the _barrier reset.

    def send(self, message, pid):
        """
        Sends a message to the processor identified with pid.

        Parameters
        ----------
        message : literally anything
            Whatever data you wish to transfer between processors
        pid : int
            The processor id to which you wish to send a message.

        Returns
        -------
        out : None"""

        # Add message to send_queue
        self._to_send_queues[pid].append(message)

    def move(self):
        """
        Acquires the first message stored in the receiving queue.

        Used to grab data from the receiving queue. This is a pop-like function
        and previously returned data cannot be returned a second time.
        returns None if queue is empty.

        Returns
        -------
        out : queue data
            The first element in the processor's "receive" queue."""
        return self._queues[self.pid].get()

    @staticmethod
    def time():
        """Records the current Unix time in seconds of the system as a float.

        Returns
        -------
        out : float
            Current Unix time in seconds"""

        if version_info >= (3, 7):
            return time.time_ns() / (10 ** 9)  # Convert to floating-point seconds
        else:
            return time.time()

    def nprocs(self):
        """Finds number of available processors in BSP instance.

        Returns
        -------
        out : int
            Number of processors participating in the current BSP instance."""
        return self.cores


def run(function, cores=0, *args):
    """Execute function on number of cores specified.

    This is how a BSP program is launched. Function needs to be of the form func(BSP:BSPObject).
    run() needs to be nested in an if __name__ = '__main__' statement.

    Parameters
    ----------
    function : callable
        A callable function to run in BSP.
    cores : int, optional
        The amount of cores you wish to use
        Defaults to all available cores
    *args : optional
        Any arguments you wish to pass on to your function.

    Returns
    -------
    out : None"""
    try:
        # If cores isn't given or is 0, then set to maximum
        if not cores:
            cores = mp.cpu_count()
        # Core exception handling
        if type(cores) != int:
            raise TypeError("Cores must be an int")
        if cores < 0:
            raise ValueError("Cores must be positive")

        # Function exception handling
        if not callable(function):
            raise TypeError("Function must be callable")

        # First open all communication channels and create a shared barrier
        processor_queues = [mp.SimpleQueue() for _ in range(cores)]
        barrier = mp.Barrier(cores)

        # Start all processes one after the other.
        for i in range(cores):
            # Create a BSP data object
            bsp = BSPObject(cores=cores, pid=i, processor_queues=processor_queues, barrier=barrier)

            # Send BSP object
            p = mp.Process(target=function, args=(bsp, *args))
            p.start()

    except RuntimeError:
        raise RuntimeError('''
        An attempt has been made to start a new process before the
        current process has finished its bootstrapping phase.

        This probably means that you tried to use the run function
        but have forgotten to use the proper safeguard:

            if __name__ == '__main__':
                run(function, cores)

        This is essential for the program to run properly.''')


def max_cores():
    """Finds number of available processors of the system.

    Returns
    ----------
    out : int
        Maximum number of available processors."""
    return mp.cpu_count()
