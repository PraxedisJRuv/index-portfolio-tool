import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import modules.extraction as ex

from datetime import datetime

def test_index_extraction():
    result = ex.index_dataframe_extraction("^IPC", datetime(2026,3,15), datetime(2026,3,20))
    assert result is not None

