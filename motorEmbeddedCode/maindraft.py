import piece


piece = piece.Piece("BP", 5, 6, 15, 20)

print(piece.name)
print(piece.row)

piece.update_row(6)
print(piece.row)
