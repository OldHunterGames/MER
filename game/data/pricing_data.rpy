init python:
    # basic price for slave in sparks
    # key: max of allure, hardiness, succulence
    # calculating function is Person.get_price
    slave_pricing = {
        0: 5,
        1: 10,
        2: 25,
        3: 50,
        4: 150,
        5: 500
    }
    # key: max of exotic or purity
    slave_price_modifiers = {
        0: 1.0,
        1: 1.1,
        2: 1.25,
        3: 1.5,
        4: 2.5,
        5: 5.0
    }