from mahjong.tiles import Faces


LUT_DORA = {
    Faces.MAN1: Faces.MAN2,
    Faces.MAN2: Faces.MAN3,
    Faces.MAN3: Faces.MAN4,
    Faces.MAN4: Faces.MAN5,
    Faces.MAN5: Faces.MAN6,
    Faces.MAN6: Faces.MAN7,
    Faces.MAN7: Faces.MAN8,
    Faces.MAN8: Faces.MAN9,
    Faces.MAN9: Faces.MAN1,

    Faces.PIN1: Faces.PIN2,
    Faces.PIN2: Faces.PIN3,
    Faces.PIN3: Faces.PIN4,
    Faces.PIN4: Faces.PIN5,
    Faces.PIN5: Faces.PIN6,
    Faces.PIN6: Faces.PIN7,
    Faces.PIN7: Faces.PIN8,
    Faces.PIN8: Faces.PIN9,
    Faces.PIN9: Faces.PIN1,

    Faces.SOU1: Faces.SOU2,
    Faces.SOU2: Faces.SOU3,
    Faces.SOU3: Faces.SOU4,
    Faces.SOU4: Faces.SOU5,
    Faces.SOU5: Faces.SOU6,
    Faces.SOU6: Faces.SOU7,
    Faces.SOU7: Faces.SOU8,
    Faces.SOU8: Faces.SOU9,
    Faces.SOU9: Faces.SOU1,

    Faces.HAKU: Faces.HATSU,
    Faces.HATSU: Faces.CHUN,
    Faces.CHUN: Faces.HAKU,

    Faces.EAST: Faces.SOUTH,
    Faces.SOUTH: Faces.WEST,
    Faces.WEST: Faces.NORTH,
    Faces.NORTH: Faces.EAST,

    Faces.MAN5_AKA: Faces.MAN6,
    Faces.PIN5_AKA: Faces.PIN6,
    Faces.SOU5_AKA: Faces.SOU6,
}


def dora(indicators):
    dora = []
    for indicator in indicators:
        dora.append(LUT_DORA[indicator.face])
    return dora
