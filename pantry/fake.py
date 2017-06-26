import random
import datetime
import faker

fake = faker.Faker()
fake.seed(1234)

rand = random.Random()
rand.seed(1234)


def create_targets(num_targets):
    targets = []
    for _ in range(0, num_targets):
        target = {
            "hostname": fake.domain_word(),
            "nickname": fake.bs(),
            "description": fake.sentence(nb_words=6),
            "maintainer": fake.safe_email(),
            "active": True
        }

        targets.append(target)

    return targets


def create_leases(num_leases):
    leases = []
    for _ in range(0, num_leases):
        created = fake.date_time()
        lease = {
            "length": rand.randint(1, 10),
            "timeout": rand.randint(1, 2),
            "created_at": fake.date_time(),
        }

        leases.append(lease)

    return leases
