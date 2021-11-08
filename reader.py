import gofish2 as gf

def handle_file(infilename, handicap, black, white):

	with open(infilename, encoding="utf8") as infile:
		lines = infile.read().split("\n")

	node = gf.Node()

	node.set("CA", "UTF-8")
	node.set("GM", 1)
	node.set("FF", 4)
	node.set("RU", "Japanese")
	node.set("PB", black)
	node.set("PW", white)

	if handicap > 1:
		node.set("HA", handicap)
		stones = gf.handicap_stones(handicap, 19, 19)
		for stone in stones:
			node.add_value("AB", stone)

	# ---------------------------------------------------------------

	comment = ""
	movenum = 0

	for line in lines:

		line = line.strip()

		if len(line) < 2:

			comment += "\n"

		elif len(line) <= 4 and line[0].isnumeric() and line[-1] == ".":

			if comment.strip():
				node.set("C", comment.strip())
				comment = ""

			node = gf.Node(node)

			movenum = int(line[0:-1])

		elif line[0] in "ABCDEFGHJKLMNOPQRST" and line[1] == " ":

			mv = line[0] + line.split(".")[0].split(" ")[1]

			x, y = gf.english_to_xy(mv)
			s = gf.xy_to_s(x, y)

			if not node.make_board().legal_move(s):
				print("Illegal, move {}: {}".format(movenum, mv))
				raise ValueError

			# node = node.make_move(s)

			if (movenum % 2 == 1 and handicap) or (movenum % 2 == 0 and not handicap):
				node.set("W", s)
			else:
				node.set("B", s)

			c = line[line.index(".") + 1:].strip()

			if c:
				comment += c + "\n"

		else:

			comment += line + "\n"


	if comment.strip():
		node.set("C", comment.strip())

	gf.save(infilename + ".sgf", node)


handle_file("game1.txt", 2, "Tsutsuki Yoneko", "Iwasa Kei")
handle_file("game2.txt", 0, "Uchigaki Sutekichi", "Murase Shuho")
handle_file("game3.txt", 0, "Ito Kotaro", "Karigane Junichi")
handle_file("game4.txt", 2, "Nagano Keijiro", "Hirose Heijiro")
handle_file("game5.txt", 5, "Unknown", "Unknown")