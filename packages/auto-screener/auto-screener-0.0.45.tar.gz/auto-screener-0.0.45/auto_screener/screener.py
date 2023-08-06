# screener.py

import os
import warnings
import datetime as dt
import time
from abc import ABCMeta
import threading
from typing import (
    Optional, Union, Dict, Iterable, Any, List
)

import pandas as pd

from represent import BaseModel, Modifiers

from auto_screener.dataset import (
    DATE_TIME, save_dataset, load_dataset
)
from auto_screener.hints import Number
from auto_screener.base import terminate_thread
from auto_screener.collect import validate_symbol

__all__ = [
    "BaseScreener",
    "wait_for_update",
    "wait_for_initialization",
    "WaitingState",
    "DataCollector",
    "collect_screeners",
    "wait_for_dynamic_update",
    "wait_for_dynamic_initialization",
    "BaseMultiScreener",
    "live_screeners",
    "create_market_dataframe"
]

class WaitingState(BaseModel):
    """A class to represent the waiting state of screener objects."""

    modifiers = Modifiers(excluded=["create_screeners"])

    def __init__(
            self,
            screeners: Iterable,
            delay: Number,
            count: int,
            canceled: bool,
            cancel: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param screeners: The screener objects.
        :param delay: The waiting delay.
        :param count: The iterations count.
        :param canceled: The value for the waiting being canceled.
        :param cancel: The time to cancel the waiting.
        """

        self.screeners: Iterable[Union[BaseScreener, BaseMultiScreener]] = screeners

        self.delay = delay
        self.cancel = cancel
        self.count = count

        self.canceled = canceled

        self.time = dt.timedelta(seconds=self.delay * self.count)
    # end __init__
# end WaitingState

class DataCollector(BaseModel, metaclass=ABCMeta):
    """A class to represent an abstract parent class of data collectors."""

    modifiers = Modifiers(**BaseModel.modifiers)
    modifiers.excluded.extend(
        [
            'screening_process', 'timeout_process',
            'saving_process'
        ]
    )

    LOCATION = "datasets"

    DELAY = 0.0
    CANCEL = 0

    def __init__(
            self,
            location: Optional[str] = None,
            cancel: Optional[Union[Number, dt.timedelta]] = None,
            delay: Optional[Union[Number, dt.timedelta]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        """

        self.cancel = cancel or self.CANCEL
        self.delay = delay or self.DELAY

        self.location = location or self.LOCATION

        self.running = False
        self.block = False
        self.saving = False

        self.screening_process = None
        self.timeout_process = None
        self.saving_process = None
    # end __init__

    def __getstate__(self) -> Dict[str, Any]:
        """
        Returns the data of the object.

        :return: The state of the object.
        """

        data = self.__dict__.copy()

        for key, value in data.items():
            if isinstance(value, threading.Thread):
                data[key] = None
            # end if
        # end for

        return data
    # end __getstate__

    def blocking(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self.block
    # end blocking

    def run_loop(self) -> None:
        """Runs the process of the price screening."""
    # end run_loop

    def saving_loop(self) -> None:
        """Runs the process of the price screening."""
    # end saving_loop

    def wait_for_initialization(
            self,
            delay: Optional[Union[Number, dt.timedelta]] = None,
            once: Optional[bool] = False,
            stop: Optional[Union[bool, int]] = False,
            cancel: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
    ) -> WaitingState:
        """
        Waits for all the create_screeners to update.

        :param delay: The delay for the waiting.
        :param once: The value to get data only once.
        :param stop: The value to stop the screener objects.
        :param cancel: The time to cancel the waiting.

        :returns: The total delay.
        """

        self: Union[BaseScreener, BaseMultiScreener]

        return wait_for_initialization(
            self, delay=delay, once=once,
            stop=stop, cancel=cancel or self.cancel
        )
    # end wait_for_initialization

    def wait_for_update(
            self,
            delay: Optional[Union[Number, dt.timedelta]] = None,
            once: Optional[bool] = False,
            stop: Optional[Union[bool, int]] = False,
            cancel: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
    ) -> WaitingState:
        """
        Waits for all the create_screeners to update.

        :param delay: The delay for the waiting.
        :param once: The value to get data only once.
        :param stop: The value to stop the screener objects.
        :param cancel: The time to cancel the waiting.

        :returns: The total delay.
        """

        self: Union[BaseScreener, BaseMultiScreener]

        return wait_for_update(
            self, delay=delay, once=once,
            stop=stop, cancel=cancel or self.cancel
        )
    # end wait_for_update

    def run(
            self,
            save: Optional[bool] = True,
            block: Optional[bool] = False,
            wait: Optional[Union[bool, Number, dt.timedelta, dt.datetime]] = False,
            timeout: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
    ) -> threading.Thread:
        """
        Runs the process of the price screening.

        :param save: The value to save the data.
        :param wait: The value to wait after starting to run the process.
        :param block: The value to block the execution.
        :param timeout: The valur to add a timeout to the process.
        """

        if self.running:
            warnings.warn(f"Screener object {self} is already running.")

            return self.screening_process
        # end if

        self.running = True

        self.screening_process = threading.Thread(target=self.run_loop)

        self.screening_process.start()

        if save:
            self.saving = True

            self.saving_process = threading.Thread(
                target=self.saving_loop
            )

            self.saving_process.start()
        # end if

        if timeout:
            self.timeout(timeout)
        # end if

        if block:
            self.block = block

            while self.blocking():
                pass
            # end while
        # end if

        if isinstance(wait, dt.datetime):
            wait = wait - dt.datetime.now()
        # end if

        if isinstance(wait, dt.timedelta):
            wait = wait.total_seconds()
        # end if

        if isinstance(wait, bool) and wait:
            self.wait_for_initialization()

        elif isinstance(wait, (int, float)):
            time.sleep(wait)
        # end if

        return self.screening_process
    # end run

    def timeout(
            self, duration: Union[Number, dt.timedelta, dt.datetime]
    ) -> threading.Thread:
        """
        Runs a timeout for the process.

        :param duration: The duration of the timeout.

        :return: The timeout process.
        """

        if isinstance(duration, dt.datetime):
            duration = duration - dt.datetime.now()
        # end if

        if isinstance(duration, dt.timedelta):
            duration = duration.total_seconds()
        # end if

        self.timeout_process = threading.Thread(
            target=lambda: (time.sleep(duration), self.terminate())
        )

        self.timeout_process.start()

        return self.timeout_process
    # end timeout

    def terminate(self) -> None:
        """Stops the trading process."""

        self.stop()
    # end terminate

    def stop(self) -> None:
        """Stops the screening process."""

        if self.running and isinstance(self.screening_process, threading.Thread):
            terminate_thread(self.screening_process)

            self.screening_process = None

            self.running = False
        # end if

        if isinstance(self.timeout_process, threading.Thread):
            terminate_thread(self.timeout_process)

            self.timeout_process = None
        # end if

        if self.saving and isinstance(self.saving_process, threading.Thread):
            terminate_thread(self.saving_process)

            self.saving_process = None

            self.saving = False
        # end if
    # end stop
# end DataCollector

def create_market_dataframe(columns: Iterable[str]) -> pd.DataFrame:
    """
    Creates a dataframe for the order book data.

    :param columns: The dataset columns.

    :return: The dataframe.
    """

    market = pd.DataFrame(
        {column: [] for column in columns}, index=[]
    )
    market.index.name = DATE_TIME

    return market
# end create_market_dataframe

class BaseScreener(DataCollector):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - symbol:
        The symbol of an asset to screen.

    - exchange:
        The name of the exchange platform to screen data from.

    - location:
        The saving location for the saved data of the screener.

    - cancel:
        The time to cancel screening process after no new data is fetched.

    - delay:
        The delay to wait between each data fetching.
    """

    modifiers = Modifiers(**DataCollector.modifiers)
    modifiers.excluded.append("market")

    def __init__(
            self,
            symbol: str,
            exchange: str,
            location: Optional[str] = None,
            cancel: Optional[Union[Number, dt.timedelta]] = None,
            delay: Optional[Union[Number, dt.timedelta]] = None,
            market: Optional[pd.DataFrame] = None,
    ) -> None:
        """
        Defines the class attributes.

        :param symbol: The symbol of the asset.
        :param exchange: The exchange to get source data from.
        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        :param market: The data for the market.
        """

        super().__init__(
            location=location, cancel=cancel, delay=delay
        )

        self.exchange = exchange

        self.symbol = self.validate_symbol(exchange=exchange, symbol=symbol)

        if market is None:
            market = create_market_dataframe(())
        # end if

        self.market = market
    # end __init__

    @staticmethod
    def validate_symbol(exchange: str, symbol: Any) -> str:
        """
        Validates the symbol value.

        :param exchange: The exchange name.
        :param symbol: The name of the symbol.

        :return: The validates symbol.
        """

        return validate_symbol(exchange=exchange, symbol=symbol)
    # end validate_symbol

    def dataset_path(self, location: Optional[str] = None) -> str:
        """
        Creates the path to the saving file for the screener object.

        :param location: The saving location of the dataset.

        :return: The saving path for the dataset.
        """

        location = location or self.location

        return (location + "/" if isinstance(location, str) else "") + (
            f"{self.exchange.lower()}/{self.symbol.replace('/', '-')}.csv"
        )
    # end dataset_path

    def save_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        if len(self.market) == 0:
            return
        # end if

        save_dataset(
            dataset=self.market,
            path=self.dataset_path(location=location)
        )
    # end save_dataset

    def load_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        data = load_dataset(path=self.dataset_path(location=location))

        for index, data in zip(data.index[:], data.loc[:]):
            self.market.loc[index] = data
        # end for
    # end load_dataset

    def saving_loop(self) -> None:
        """Runs the process of the price screening."""

        self.saving = True

        delay = self.delay

        if isinstance(self.delay, dt.timedelta):
            delay = delay.total_seconds()
        # end if

        while self.saving:
            start = time.time()

            self.save_dataset()

            end = time.time()

            time.sleep(max(delay - (end - start), 0) or 1)
        # end while
    # end run_loop
# end BaseScreener

class BaseMultiScreener(DataCollector):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - location:
        The saving location for the saved data of the screener.

    - cancel:
        The time to cancel screening process after no new data is fetched.

    - delay:
        The delay to wait between each data fetching.
    """

    modifiers = Modifiers(**DataCollector.modifiers)
    modifiers.excluded.append("market")

    screeners: List[BaseScreener]

    def __init__(
            self,
            screeners: Optional[Iterable[BaseScreener]] = None,
            location: Optional[str] = None,
            cancel: Optional[Union[Number, dt.timedelta]] = None,
            delay: Optional[Union[Number, dt.timedelta]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        """

        super().__init__(location=location, cancel=cancel, delay=delay)

        self.screeners = list(screeners or [])
    # end __init__

    def load_datasets(self, location: Optional[str] = None) -> None:
        """
        Loads the datasets of the create_screeners.

        :param location: The saving or loading path for the dataset.
        """

        for screener in self.screeners:
            if os.path.exists(screener.dataset_path() or location):
                try:
                    screener.load_dataset(
                        location=location or self.location or screener.location
                    )

                except Exception as e:
                    warnings.warn(str(e))
                # end try
            # end if
        # end for
    # end load_datasets

    def save_datasets(self, location: Optional[str] = None) -> None:
        """
        Saves the datasets of the create_screeners.

        :param location: The saving or loading path for the dataset.
        """

        for screener in self.screeners:
            try:
                screener.save_dataset(
                    location=location or self.location or screener.location
                )

            except Exception as e:
                warnings.warn(str(e))
            # end try
        # end for
    # end load_datasets
# end BaseScreener

def collect_screeners(
        symbol: str,
        exchange: str,
        screeners: Iterable[BaseScreener]
) -> List[BaseScreener]:
    """
    Finds the create_screeners with the given source exchange and symbol.

    :param symbol: The symbol of the screener.
    :param exchange: The exchange name of the screener.
    :param screeners: The create_screeners to search in.

    :return: A list of the matching create_screeners.
    """

    found = []

    for screener in screeners:
        if (screener.exchange == exchange) and (screener.symbol == symbol):
            found.append(screener)
        # end if
    # end for

    return found
# end collect_screeners

def wait_for_dynamic_initialization(
        screeners: Iterable[Union[BaseScreener, BaseMultiScreener]],
        delay: Optional[Union[Number, dt.timedelta]] = None,
        once: Optional[bool] = False,
        stop: Optional[Union[bool, int]] = False,
        cancel: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
) -> WaitingState:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param once: The value to get data only once.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.

    :returns: The total delay.
    """

    if cancel == 0:
        cancel = None
    # end if

    if isinstance(cancel, (int, float)):
        cancel = dt.timedelta(seconds=cancel)
    # end if

    current_time = dt.datetime.now()

    if isinstance(cancel, dt.timedelta):
        cancel = current_time + cancel
    # end if

    if isinstance(delay, dt.timedelta):
        delay = delay.total_seconds()
    # end if

    delay = delay or 0
    count = 0

    saved_screeners = screeners
    checked_screeners = []

    while True:
        for screener in saved_screeners:
            if isinstance(screener, BaseScreener):
                checked_screeners.append(screener)

            elif isinstance(screener, BaseMultiScreener):
                checked_screeners.extend(screener.screeners)
            # end if
        # end for

        if (
            (
                not any(
                    len(screener.market) == 0
                    for screener in checked_screeners
                )
            ) or
            (
                (cancel is not None) and
                ((current_time := dt.datetime.now()) > cancel)
            )
        ):
            break
        # end if

        count += 1

        if isinstance(delay, (int, float)) and (count > 0):
            time.sleep(delay)
        # end if
    # end while

    if stop and ((stop == count) or once):
        for screener in checked_screeners:
            screener.stop()
        # end for
    # end if

    return WaitingState(
        screeners=screeners, delay=delay, count=count,
        cancel=cancel, canceled=(cancel is None) or (current_time > cancel)
    )
# end wait_for_dynamic_initialization

def wait_for_initialization(
        *screeners: Union[BaseScreener, BaseMultiScreener],
        delay: Optional[Union[Number, dt.timedelta]] = None,
        once: Optional[bool] = False,
        stop: Optional[Union[bool, int]] = False,
        cancel: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
) -> WaitingState:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param once: The value to get data only once.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.

    :returns: The total delay.
    """

    return wait_for_dynamic_initialization(
        screeners, delay=delay, once=once,
        stop=stop, cancel=cancel
    )
# end wait_for_initialization

def wait_for_dynamic_update(
        screeners: Iterable[Union[BaseScreener, BaseMultiScreener]],
        delay: Optional[Union[Number, dt.timedelta]] = None,
        once: Optional[bool] = False,
        stop: Optional[Union[bool, int]] = False,
        cancel: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
) -> WaitingState:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param once: The value to get data only once.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.

    :returns: The total delay.
    """

    if cancel == 0:
        cancel = None
    # end if

    if isinstance(cancel, (int, float)):
        cancel = dt.timedelta(seconds=cancel)
    # end if

    current_time = dt.datetime.now()

    if isinstance(cancel, dt.timedelta):
        cancel = current_time + cancel
    # end if

    if isinstance(delay, dt.timedelta):
        delay = delay.total_seconds()
    # end if

    delay = delay or 0
    count = 0

    if screeners:
        wait_for_dynamic_initialization(
            screeners, delay=delay, once=once
        )

        saved_screeners = screeners
        checked_screeners = []

        for screener in saved_screeners:
            if isinstance(screener, BaseScreener):
                checked_screeners.append(screener)

            elif isinstance(screener, BaseMultiScreener):
                checked_screeners.extend(screener.screeners)
            # end if
        # end for

        indexes = [
            screener.market.index[-1]
            for screener in checked_screeners
        ]

        new_indexes = indexes

        length = len(tuple(checked_screeners))

        while True:
            for screener in saved_screeners:
                if isinstance(screener, BaseScreener):
                    checked_screeners.append(screener)

                elif isinstance(screener, BaseMultiScreener):
                    checked_screeners.extend(screener.screeners)
                # end if
            # end for

            if (
                all(
                    indexes[i] != new_indexes[i]
                    for i in range(length)
                ) or
                (
                    (cancel is not None) and
                    ((current_time := dt.datetime.now()) > cancel)
                )
            ):
                break
            # end if

            count += 1

            new_indexes = [
                screener.market.index[-1]
                for screener in checked_screeners
            ]

            if isinstance(delay, (int, float)) and (count > 0):
                time.sleep(delay)
            # end if
        # end while

        if stop and ((stop == count) or once):
            for screener in checked_screeners:
                screener.stop()
            # end for
        # end if
    # end if

    return WaitingState(
        screeners=screeners, delay=delay, count=count, cancel=cancel,
        canceled=(cancel is None) or (current_time > cancel)
    )
# end wait_for_dynamic_update

def wait_for_update(
        *screeners: Union[BaseScreener, BaseMultiScreener],
        delay: Optional[Union[Number, dt.timedelta]] = None,
        once: Optional[bool] = False,
        stop: Optional[Union[bool, int]] = False,
        cancel: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
) -> WaitingState:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param once: The value to get data only once.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.

    :returns: The total delay.
    """

    return wait_for_dynamic_update(
        screeners, delay=delay, once=once,
        stop=stop, cancel=cancel
    )
# end wait_for_update

def live_screeners(
        screeners: Iterable[Union[BaseScreener, BaseMultiScreener]]
) -> List[Union[BaseScreener, BaseMultiScreener]]:
    """
    Returns a list of all the live create_screeners.

    :param screeners: The create_screeners to search from.

    :return: A list the live create_screeners.
    """

    return [
        screener for screener in screeners
        if (
            screener.running and (
                isinstance(screener, BaseMultiScreener) or
                len(screener.market) > 0
            )
        )
    ]
# end live_screeners