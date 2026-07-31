from __future__ import annotations

import asyncio
import datetime as dt
import time

import pytest
import time_machine

from fixtures.devkit import DevKit, Flash

# Mock version. Fetch during runtime in real-world
HEX_VER = "v23.7.99-debug+127"

@pytest.mark.usefixtures("read_bootstatus")
class TestBootReport:
    @pytest.mark.xfail(reason="simulate device get stuck in reset loop")
    def test_boot_status(self, request, revive_on_failure):
        try:
            assert False
        except AssertionError:
            request.node.fw_ver = HEX_VER
            raise

    def test_boot_banner(self, flash: Flash, console: DevKit):
        flash("build/boot/zephyr/zephyr.hex")
        line = console.readline().decode(errors="replace")
        assert "Booting Zephyr" in line

    async def test_shell_awake(self, console: DevKit, mocker):
        mocker.patch.object(console, "readline", return_value=b"uart:~$\n")
        with time_machine.travel(dt.datetime(2026, 7, 31, 12, 0, 0), tick=False) as clock:
            line = console.readline()
            print(f"[{time.strftime('%H:%M:%S')}] {line.decode().strip()}")
            assert b"uart:~$" in line
            assert time.strftime("%H:%M:%S", time.gmtime()) == "12:00:00"

            await asyncio.sleep(0)
            clock.shift(dt.timedelta(seconds=5))

            line = console.readline()
            assert b"uart:~$" in line
            assert time.strftime("%H:%M:%S", time.gmtime()) == "12:00:05"
            print(f"[{time.strftime('%H:%M:%S')}] {line.decode().strip()}")
