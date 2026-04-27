from source.utils.db import db
from source.models.plan import Plan

from datetime import datetime, timezone

def seed_plans():
    if Plan.query.first():
        print("Plans already exist")
        return

    plans = [
        Plan("free", 1, 2, 20, 2, 200, 5),
        Plan("starter", 2, 2, 40, 2, 350, 10),
        Plan("growth", 2, 11, 500, 10, 350, 50),
        Plan("pro", 10, 11, 5000, 25, 350, 100),
        Plan("enterprise", 35, 11, 10000, 50, 350, 200),
    ]

    db.session.bulk_save_objects(plans)
    db.session.commit()

    print("Plans seeded succesfully, created at: " + str(datetime.now(timezone.utc)))