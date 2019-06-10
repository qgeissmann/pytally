import logging
import time


class BaseInterface(object):
    def __init__(self, do_warm_up = True):
        if do_warm_up:
            self._warm_up()

    def _warm_up(self):
        raise NotImplementedError

    def send(self, **kwargs):
        raise NotImplementedError


class WrongSerialPortError(Exception):
    pass


class NoValidPortError(Exception):
    pass


class YRouletteController(BaseInterface):
    _baud = 115200

    def __init__(self, port=None, *args, **kwargs):
        import serial
        logging.info("Connecting to arduino serial port...")

        self._serial = None
        if port is None:
            self._port = self._find_port()
        else:
            self._port = port

        self._serial = serial.Serial(self._port, self._baud, timeout=2)
        time.sleep(2)
        self._test_serial_connection()
        super(YRouletteController, self).__init__(*args, **kwargs)

    def _find_port(self):
        from serial.tools import list_ports
        # import serial
        import os
        all_port_tuples = list_ports.comports()
        logging.info("listing serial ports")
        all_ports = set()
        for ap, _, _ in all_port_tuples:
            p = os.path.basename(ap)
            if p.startswith("ttyUSB") or p.startswith("ttyACM"):
                all_ports |= {ap}
                logging.info("\t%s", str(ap))

        if len(all_ports) == 0:
            logging.error("No valid port detected!. Possibly, device not plugged/detected.")
            raise NoValidPortError()

        elif len(all_ports) > 2:
            logging.info("Several port detected, using first one: %s", str(all_ports))
        return all_ports.pop()

    def __del__(self):
        if self._serial is not None:
            self._serial.close()

    def _test_serial_connection(self):
        return

    def send(self, *args, **kwargs):
        self._serial.write(b'S\r\n')
        pass

    def _warm_up(self):
        self._serial.write(b'W\r\n')
        pass
