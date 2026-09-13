def calculate_score(cost, delivery_days, carbon):
    score = (
        cost * 0.5
        + delivery_days * 1000 * 0.3
        + carbon * 100 * 0.2
    )

    return score


def rank_options(options):
    for option in options:

        option["score"] = calculate_score(
            option["cost"],
            option["delivery_days"],
            option["carbon"]
        )

    options.sort(key=lambda x: x["score"])

    return options


def choose_best_option(options):

    ranked_options = rank_options(options)

    return ranked_options[0]