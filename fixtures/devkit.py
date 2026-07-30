import hashlib
from collections.abc import Callable, Generator

import pytest

type Flash = Callable[[str], str]

class DevKit:
    """MOCK DK. NOT REAL!!!"""
    def __init__(self):
        self.firmware = None
        self.buffer = b""
    # J-Link
    def erase_all(self):
        self.firmware = None
    def program_file(self, hx):
         self.firmware = hx
    def reset(self):
        if self.firmware:
            self.buffer += b"*** Booting Zephyr OS ***\n"
    # serial comm
    def flush(self):
        self.buffer = b""
    def readline(self):
        line, _, self.buffer = self.buffer.partition(b"\n")
        return line + b"\n"
    def read(self, n):
        out, self.buffer = self.buffer[:n], self.buffer[n:]
        return out
    def write(self, data):
        self.buffer += b"Zephyr version 3.X.X\n" if b"kernel version" in data else b"uart:~$ "

# shared data
@pytest.fixture(scope="session")
def target():
    return {"family": "nRF00X00", "vcom": "/dev/ttyACM0", "baud": 115200}

# setup + teardown: J-Link
@pytest.fixture(scope="session")
def jlink(target):
    board = DevKit()
    print(f"\n[setup]   J-Link connected ({target['family']}) [SIM]")
    yield board
    print("\n[teardown] J-Link closed")

# setup + teardown: serial console
@pytest.fixture
def console(target, jlink):
    jlink.flush()
    print(f"\n  [setup]   console open on {target['vcom']} @ {target['baud']}")
    yield jlink
    print("\n  [teardown] console closed")


# flash factory
@pytest.fixture
def flash(jlink, request) -> Generator[Flash]:
    cache = request.config.cache
    flashed = []

    def _flash(hex_path: str) -> str:
        key = "flash/" + hashlib.sha1(hex_path.encode()).hexdigest()
        prev = cache.get(key, None)
        if prev == hex_path: # cache hit
            print(f"  [cache] skip flashing {hex_path} (already flashed)")
            # simulate that the previous firmware is intact
            jlink.firmware = f"{hex_path}"
        else:
            jlink.erase_all()
            jlink.program_file(hex_path)
            print(f"  [factory] flashed {hex_path}")
            cache.set(key, hex_path) # cache missed before, thus caching now
            print(f"  [cache]  stored {key}")
        # reset in case flashing was not needed
        jlink.reset()
        flashed.append(hex_path)
        return hex_path

    yield _flash

    jlink.erase_all()
    print(f"  [factory] erased target")
