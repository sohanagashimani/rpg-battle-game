from classes.game import person, bcolors
from classes.magic import spell
from classes.inventory import item
import random

# create black magic
fire = spell("Fire", 25, 600, "black")
thunder = spell("Thunder", 25, 600, "black")
blizzard = spell("Blizzard", 25, 600, "black")
meteor = spell("Meteor", 40, 1200, "black")
quake = spell("Quake", 14, 140, "black")
# create white magic
cure = spell("Cure", 25, 620, "White")
cura = spell("Cura", 32, 1500, "White")
curaga = spell("Curaga", 50, 6000, "White")
# Create some items
potion = item("Potion", "potion", "Heals 50 HP", 50)
hipotion = item("Hi- Potion", "potion", "Heals 100 HP", 100)
superpotion = item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = item("Megaelixer", "elixer", "Fully restores party's HP/MP ", 9999)

grenade = item("grenade", "attack", "deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, curaga]
player_items = [{"item": potion, "quantity": 15, }, {"item": hipotion, "quantity": 5},
				{"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
				{"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]
# Instantiate People
player1 = person("Valos:", 3260, 132, 300, 34, player_spells, player_items)
player2 = person("Nick :", 4160, 188, 311, 34, player_spells, player_items)
player3 = person("Robot:", 3089, 174, 288, 34, player_spells, player_items)
enemy2 = person("Imp    ", 1250, 130, 560, 325, enemy_spells, [])
enemy1 = person("Magus", 11200, 701, 525, 25, enemy_spells, [])
enemy3 = person("Imp    ", 1250, 130, 560, 325, enemy_spells, [])
players = [player1, player2, player3]
enemies = [enemy2, enemy1, enemy3]
running = True
i = 0
print(bcolors.FAIL + bcolors.BOLD + "An enemy attacks!" + bcolors.ENDC)
while running:
	print("=================")
	print("\n\n")
	print("NAME                HP                                   MP")

	for player in players:
		player.get_stats()

	print("\n")
	for enemy in enemies:
		enemy.get_enemy_stats()

	for player in players:
		player.choose_action()
		choice = input("    choose action:")
		index = int(choice) - 1
		if index == 0:
			dmg = player.generate_damage()
			enemy = player.choose_target(enemies)
			enemies[enemy].take_damage(dmg)
			print("You attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg, "points of damage.")
			if enemies[enemy].get_hp() == 0:
				print(enemies[enemy].name.replace(" ", "") + " has died.")
				del enemies[enemy]
		elif index == 1:
			player.choose_magic()
			magic_choice = int(input("    Choose Magic:")) - 1
			if magic_choice == -1:
				continue
			spell = player.magic[magic_choice]
			magic_dmg = player.magic[magic_choice].generate_damage()

			current_mp = player.get_mp()
			if spell.cost > current_mp:
				print(bcolors.FAIL + "\nNot enough MP" + bcolors.ENDC)
				continue
			player.reduce_mp(spell.cost)
			if spell.type == "White":
				player.heal(magic_dmg)
				print(bcolors.OKBLUE + spell.name + "Heals for"  + str(magic_dmg),
					  "HP." + bcolors.ENDC)
			elif spell.type == "black":
				enemy = player.choose_target(enemies)
				enemies[enemy].take_damage(magic_dmg)
				print(bcolors.OKBLUE + "\n" + spell.name + "deals", str(magic_dmg),
					  "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)
				if enemies[enemy].get_hp() == 0:
					print(enemies[enemy].name.replace(" ", "") + " has died.")
					del enemies[enemy]


		elif index == 2:
			player.choose_item()
			item_choice = int(input("    Choose item:")) - 1

			if item_choice == -1:
				continue
			item = player.items[item_choice]["item"]
			if player.items[item_choice]["quantity"] == 0:
				print(bcolors.FAIL + "\n" + "None Left..." + bcolors.ENDC)
				continue
			player.items[item_choice]["quantity"] -= 1

			if item.type == "potion":
				player.heal(item.prop)
				print(bcolors.OKGREEN + "\n" + item.name + "Heals for", str(item.prop), bcolors.ENDC)
			elif item.type == "elixer":
				if item.name == "Megaelixer":
					for i in players:
						i.hp = i.maxhp
						i.mp = i.maxmp
				else:
					player.hp = player.maxhp
					player.mp = player.maxmp
				print(bcolors.OKGREEN + "\n" + item.name + "fully restores HP/MP" + bcolors.ENDC)
			elif item.type == "attack":
				enemy = player.choose_target(enemies)
				enemies[enemy].take_damage(item.prop)
				print(bcolors.FAIL + "\n" + item.name + "deals", str(item.prop),
					  "points of damage to" + enemies[enemy].name + bcolors.ENDC)
				if enemies[enemy].get_hp() == 0:
					print(enemies[enemy].name.replace(" ", "") + "has died")
					del enemies[enemy]
	# check if battle is over
	defeated_enemies = 0
	defeated_players = 0
	for enemy in enemies:
		if enemy.get_hp() == 0:
			defeated_enemies += 1
	for player in players:
		if player.get_hp() == 0:
			defeated_players += 1
	# check if player won
	if defeated_enemies == 2:
		print(bcolors.OKGREEN + " Win!" + bcolors.ENDC)
		running = False
	# check if enemy won
	elif defeated_players == 2:
		print(bcolors.FAIL + "Your Enemies has defeated you" + bcolors.ENDC)
		running = False
	print("\n")
	# enemy attack phase
	for enemy in enemies:
		enemy_choice = random.randrange(0, 2)
		if enemy_choice == 0:
			# chose attack
			target = random.randrange(0, 3)
			enemy_dmg = enemies[0].generate_damage()
			players[target].take_damage(enemy_dmg)
			print(enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "") + "for", enemy_dmg)
		elif enemy_choice == 1:
			spell, magic_dmg = enemy.choose_enemy_spell()
			enemy.reduce_mp(spell.cost)
			if spell.type == "White":
				enemy.heal(magic_dmg)
				print(bcolors.OKBLUE + spell.name + "Heals" + enemy.name + "for", str(magic_dmg),
					  "HP." + bcolors.ENDC)
			elif spell.type == "black":
				target = random.randrange(0, 3)
				players[target].take_damage(magic_dmg)
				print(bcolors.OKBLUE + "\n"+ enemy.name.replace(" ","" ) + "'s" + spell.name + " deals", str(magic_dmg),
				  "points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)
				if players[target].get_hp() == 0:
					print(players[target].name.replace(" ", "") + " has died.")
					del players[player]
			#print("Enemy chose", spell, "damage is", magic_dmg)
