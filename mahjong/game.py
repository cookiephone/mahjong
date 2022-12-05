import mahjong.rules as rules
from mahjong.tiles import Faces
from mahjong.seats import Seat
from mahjong.wall import Wall
from mahjong.players import Player


class GameState:

    def __init__(self, seed=None, ruleset="default"):
        self.rule_context = rules.get_ruleset_context(ruleset)
        self.wall = Wall(seed, akadora=self.rule_context.aka_dora)
        self.round_wind = Faces.EAST
        self.players = []
        for seat in [Seat.EAST, Seat.SOUTH, Seat.WEST, Seat.NORTH]:
            player = Player(self.rule_context, seat)
            self.players.append(player)
        self.dealer = self.players[0]
        self.history = []

    def visualization_string(self):
        VIS_STR_SEAT = {Seat.EAST: "E", Seat.SOUTH: "S", Seat.WEST: "W", Seat.NORTH: "N"}
        VIS_STR_FACES = {
            Faces.MAN1: "1m", Faces.MAN2: "2m", Faces.MAN3: "3m", Faces.MAN4: "4m", Faces.MAN5: "5m", Faces.MAN6: "6m", Faces.MAN7: "7m", Faces.MAN8: "8m", Faces.MAN9: "9m",
            Faces.PIN1: "1p", Faces.PIN2: "2p", Faces.PIN3: "3p", Faces.PIN4: "4p", Faces.PIN5: "5p", Faces.PIN6: "6p", Faces.PIN7: "7p", Faces.PIN8: "8p", Faces.PIN9: "9p",
            Faces.SOU1: "1s", Faces.SOU2: "2s", Faces.SOU3: "3s", Faces.SOU4: "4s", Faces.SOU5: "5s", Faces.SOU6: "6s", Faces.SOU7: "7s", Faces.SOU8: "8s", Faces.SOU9: "9s",
            Faces.HAKU: "W ", Faces.HATSU: "G ", Faces.CHUN: "R ",
            Faces.EAST: "e ", Faces.SOUTH: "s ", Faces.WEST: "w ", Faces.NORTH: "n ",
            Faces.MAN5_AKA: "am", Faces.PIN5_AKA: "ap", Faces.SOU5_AKA: "as",
        }
        tiles_to_strs = lambda tiles: [VIS_STR_FACES[tile.face] for tile in tiles]
        pad = lambda lst, sz: lst + ["  "] * (sz - len(lst))
        seat = [VIS_STR_SEAT[player.seat] for player in self.players]
        hands = [pad(tiles_to_strs(player.hand), 14) for player in self.players]
        discs = [pad(tiles_to_strs(player.discards), 24) for player in self.players]
        dora = pad([VIS_STR_FACES[face] for face in self.wall.dora()], 5)
        uradora = pad([VIS_STR_FACES[face] for face in self.wall.uradora()], 5)
        return (
            f"SEAT            PLAYER 1 ({seat[0]})            PLAYER 2 ({seat[1]})            PLAYER 3 ({seat[2]})            PLAYER 4 ({seat[3]})            \n"
            f"DISCARDS        {discs[0][ 0]} {discs[0][ 1]} {discs[0][ 2]} {discs[0][ 3]} {discs[0][ 4]} {discs[0][ 5]}       {discs[1][ 0]} {discs[1][ 1]} {discs[1][ 2]} {discs[1][ 3]} {discs[1][ 4]} {discs[1][ 5]}       {discs[2][ 0]} {discs[2][ 1]} {discs[2][ 2]} {discs[2][ 3]} {discs[2][ 4]} {discs[2][ 5]}       {discs[3][ 0]} {discs[3][ 1]} {discs[3][ 2]} {discs[3][ 3]} {discs[3][ 4]} {discs[3][ 5]}       \n"
            f"                {discs[0][ 6]} {discs[0][ 7]} {discs[0][ 9]} {discs[0][ 9]} {discs[0][10]} {discs[0][11]}       {discs[1][ 6]} {discs[1][ 7]} {discs[1][ 9]} {discs[1][ 9]} {discs[1][10]} {discs[1][11]}       {discs[2][ 6]} {discs[2][ 7]} {discs[2][ 9]} {discs[2][ 9]} {discs[2][10]} {discs[2][11]}       {discs[3][ 6]} {discs[3][ 7]} {discs[3][ 9]} {discs[3][ 9]} {discs[3][10]} {discs[3][11]}       \n"
            f"                {discs[0][12]} {discs[0][13]} {discs[0][14]} {discs[0][15]} {discs[0][16]} {discs[0][17]}       {discs[1][12]} {discs[1][13]} {discs[1][14]} {discs[1][15]} {discs[1][16]} {discs[1][17]}       {discs[2][12]} {discs[2][13]} {discs[2][14]} {discs[2][15]} {discs[2][16]} {discs[2][17]}       {discs[3][12]} {discs[3][13]} {discs[3][14]} {discs[3][15]} {discs[3][16]} {discs[3][17]}       \n"
            f"                {discs[0][18]} {discs[0][19]} {discs[0][20]} {discs[0][21]} {discs[0][22]} {discs[0][23]}       {discs[1][18]} {discs[1][19]} {discs[1][20]} {discs[1][21]} {discs[1][22]} {discs[1][23]}       {discs[2][18]} {discs[2][19]} {discs[2][20]} {discs[2][21]} {discs[2][22]} {discs[2][23]}       {discs[3][18]} {discs[3][19]} {discs[3][20]} {discs[3][21]} {discs[3][22]} {discs[3][23]}       \n"
            f"                                                                                                                \n"
            f"HAND            {hands[0][ 0]} {hands[0][ 1]} {hands[0][ 2]} {hands[0][ 3]} {hands[0][ 4]} {hands[0][ 5]} {hands[0][ 6]}    {hands[1][ 0]} {hands[1][ 1]} {hands[1][ 2]} {hands[1][ 3]} {hands[1][ 4]} {hands[1][ 5]} {hands[1][ 6]}    {hands[2][ 0]} {hands[2][ 1]} {hands[2][ 2]} {hands[2][ 3]} {hands[2][ 4]} {hands[2][ 5]} {hands[2][ 6]}    {hands[3][ 0]} {hands[3][ 1]} {hands[3][ 2]} {hands[3][ 3]} {hands[3][ 4]} {hands[3][ 5]} {hands[3][ 6]}    \n"
            f"                {hands[0][ 7]} {hands[0][ 8]} {hands[0][ 9]} {hands[0][10]} {hands[0][11]} {hands[0][12]} {hands[0][13]}    {hands[1][ 7]} {hands[1][ 8]} {hands[1][ 9]} {hands[1][10]} {hands[1][11]} {hands[1][12]} {hands[1][13]}    {hands[2][ 7]} {hands[2][ 8]} {hands[2][ 9]} {hands[2][10]} {hands[2][11]} {hands[2][12]} {hands[2][13]}    {hands[3][ 7]} {hands[3][ 8]} {hands[3][ 9]} {hands[3][10]} {hands[3][11]} {hands[3][12]} {hands[3][13]}    \n"
            f"                                                                                                                \n"
            f"CALLED MELDS    xx xx xx xx             xx xx xx xx             xx xx xx xx             xx xx xx xx             \n"
            f"                xx xx xx xx             xx xx xx xx             xx xx xx xx             xx xx xx xx             \n"
            f"                xx xx xx xx             xx xx xx xx             xx xx xx xx             xx xx xx xx             \n"
            f"                xx xx xx xx             xx xx xx xx             xx xx xx xx             xx xx xx xx             \n"
            f"                                                                                                                \n"
            f"DORA            {dora[0]} {dora[1]} {dora[2]} {dora[3]} {dora[4]}                                                                                  \n"
            f"URADORA         {uradora[0]} {uradora[1]} {uradora[2]} {uradora[3]} {uradora[4]}                                                                                  \n"
        )
