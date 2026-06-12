import extraction as ex
from datetime import datetime

def test_index_extraction():
    result = ex.index_dataframe_extraction("^IPC", datetime(2026,3,15), datetime(2026,3,20))
    assert result is not None

