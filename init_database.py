from app import db, Address
import zipfile
import io
import os
import csv
from datetime import datetime


HERE = os.path.dirname(os.path.abspath(__file__))


def create_all():
    """Create DB and schema"""
    db.create_all()


def seed():
    """Seed DB with data"""
    seed_path = os.path.join(HERE, 'data/seed/Adressen__Berlin.zip')
    with zipfile.ZipFile(seed_path) as address_zip:
        with io.TextIOWrapper(address_zip.open('Adressen__Berlin.csv', 'r')) as csv_file:
            seed_reader = csv.DictReader(csv_file)
            for row in seed_reader:
                # Convert string to datetime
                added_on = datetime.strptime(
                    row['STR_DATUM'], '%Y-%m-%dT%H:%M:%S')

                # Create object
                address = Address(
                    id=row['OBJECTID'],
                    postcode=row['PLZ'],
                    added_on=added_on)

                # Write it into session
                db.session.add(address)

            # Commit all records to DB
            db.session.commit()


if __name__ == '__main__':
    create_all()
    seed()
