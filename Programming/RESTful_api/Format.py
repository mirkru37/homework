import Freelancer
import Validation


def name(name_):
    return name_.replace(' ', '').capitalize()


def position(value):
    for i in Validation.positions:
        if i.lower() == value.lower():
            return i
    raise ValueError("Invalid position")


def freelancer_fields(freelancer):
    """returns array of freelancer values from string ["id", "name", "email" ... "salary", "position"]"""
    count_of_fields = Freelancer.Freelancer.count_of_fields
    freelancer = freelancer.replace('\t', " ").split(" ")
    freelancer = [i for i in freelancer if i.strip()]  # remove spaces
    if len(freelancer) - 1 == count_of_fields:
        # case when split as [... "BE", "Developer"]
        freelancer[count_of_fields - 1:len(freelancer)] = \
            [" ".join(freelancer[count_of_fields - 1:len(freelancer)])]
    return freelancer
