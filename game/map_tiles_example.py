from domain.map import MapTile

#map_string = [
#     "............",
#     "..#......#..",
#     "..###..###..",
#     "..#......#..",
#     ".#...##...#.",
#     "...#.##.#...",
#     ".###....###.",
#     ".....##.....",
#     "..#..##..#..",
#     ".##.####.##.",
#     ".#...##...#.",
#     "............"
# ]
from domain.position import Position

# map_string = [
#     ".....",
#     ".#.#.",
#     ".#*#.",
#     "*....",
#     ".###.",
# ]

# map_string = [
#     ".**.*",
#     "*#.#*",
#     ".#*#.",
#     "*.*.*",
#     ".###*",
# ]

map_string = [
    ".****",
    "*#*#*",
    "*#*#*",
    "*****",
    "*###*",
]

map_tiles_example = []
available_points_example = []

for y in range(len(map_string)):
    tiles = []
    for x in range(len(map_string[0])):
        if map_string[y][x] == '#':
            tiles.append(MapTile.WALL)
        elif map_string[y][x] == '*':
            tiles.append(MapTile.EMPTY)
            available_points_example.append(Position(x, y))
        else:
            tiles.append(MapTile.EMPTY)
    map_tiles_example.append(tiles)
