"""核对演练资料的公开输入约定。"""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from inspect_packet import read_packet


class PacketTest(unittest.TestCase):
    def test_related_records(self):
        doc = read_packet(Path("资料/演练.json"))
        lots={row['lot'] for row in doc['lots']}
        self.assertTrue(len(lots)==len(doc['lots']))
        self.assertTrue({row['lot'] for row in doc['sample']+doc['lab']+doc['followups']} <= lots)
        self.assertTrue(doc['policy']['attribution_lot'] in lots)
        self.assertTrue(any(row['p'] is None for row in doc['sample']))
        self.assertTrue(any(len(row['possible_sellers'])==2 for row in doc['lots']))
        self.assertTrue({row['event'] for row in doc['invites']} <= {row['event'] for row in doc['events']})

    def test_reject_wrong_container(self):
        with TemporaryDirectory() as folder:
            packet = Path(folder) / "unexpected.json"
            packet.write_text(json.dumps({"invalid": 3}), encoding="utf-8")
            with self.assertRaises(ValueError):
                read_packet(packet)
