from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTest(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is availlable"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            """Istead of doint its job, we will mock it to return True and we\
                can monitor that how many times it run"""
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)
    
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError]*5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)

