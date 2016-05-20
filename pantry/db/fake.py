import random
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
            "health_percent": rand.randint(0, 100),
            "state": "ready"
            }

        targets.append(target)

    return targets
