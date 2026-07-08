def ai_color(rsrp):

    if rsrp > -80:
        return "green"

    elif rsrp > -95:
        return "orange"

    else:
        return "red"