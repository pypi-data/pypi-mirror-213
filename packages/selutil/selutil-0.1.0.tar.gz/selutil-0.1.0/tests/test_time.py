import datetime

from selutil.time import get_timestamp


def test_get_timestamp_default():
    dt = datetime.datetime.now(datetime.timezone.utc)
    gt = datetime.datetime.fromisoformat(get_timestamp())
    assert (dt - gt) <= datetime.timedelta(seconds=1)


def test_get_timestamp_ms_tz():
    tz = datetime.timezone(datetime.timedelta(hours=5))
    dt = datetime.datetime(2000, 3, 14, 16, 21, 32, 5, tzinfo=tz)
    dts = "2000-03-14T16:21:32.000005+05:00"
    assert get_timestamp(dt) == dts


def test_get_timestamp_ms_no_tz():
    dt = datetime.datetime(2000, 3, 14, 16, 21, 32, 5)
    dts = "2000-03-14T16:21:32.000005"
    assert get_timestamp(dt) == dts


def test_get_timestamp_no_ms_no_tz():
    dt = datetime.datetime(2000, 3, 14, 16, 21, 32)
    dts = "2000-03-14T16:21:32"
    assert get_timestamp(dt) == dts


def test_get_timestamp_no_ms_tz():
    dt = datetime.datetime(2000, 3, 14, 16, 21, 32,
                           tzinfo=datetime.timezone.utc)
    dts = "2000-03-14T16:21:32+00:00"
    assert get_timestamp(dt) == dts
