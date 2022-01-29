from ....constant.colors import GOLD, GREEN, WHITE, RARITY_COLORS
from ....function.util import checkpoint
from ....object.items import get_item

__all__ = ['grandma_wolf']


@checkpoint
def grandma_wolf(player, /):
    for index, pet in enumerate(player.pets):
        if pet.name == 'grandma_wolf_pet':
            break
    else:
        item = get_item('grandma_wolf_pet', rarity='common')
        player.pets.append(item)
        player.npc_speak('grandma_wolf', [
            ("Oh adventurer! I'm having a conundrum! There's so much to kill,"
             " and so little time."),
            (f"I've added the {GREEN}Grandma Wolf Pet {WHITE}to your"
             f" {GREEN}Pets Menu{WHITE}."),
            ("The Grandma Wolf is particularly adept at combos."
             " The more mobs you kill in quick succession the better!"),
            (f"If you reach high enough {GOLD}Bestiary Milestones{WHITE},"
             f" I will increase the rarity of this pet!"),
            ("The pet does not need to be spawned for combos to work!"
             " Happy hunting!"),
        ])
        return

    rarity = pet.rarity
    bestiary_ms = player.get_bestiary_milestone()
    if rarity == 'common':
        if bestiary_ms < 2:
            player.npc_speak('grandma_wolf', [
                (f"Come back when you've reached {GOLD}Bestiary Milestone II"
                 f" {WHITE}to upgrade it to {RARITY_COLORS['uncommon']}"
                 f"Uncommon{WHITE}."),
            ])
        else:
            player.pets[index].rarity = 'uncommon'
            player.npc_speak('grandma_wolf', [
                (f"There you go! I've upgraded your {RARITY_COLORS['uncommon']}"
                 f"Grandma Wolf Pet {WHITE}to {RARITY_COLORS['uncommon']}"
                 f"Uncommon{WHITE}!"),
                (f"Come back when you've reached {GOLD}Bestiary Milestone IV"
                 f" {WHITE}to upgrade it to {RARITY_COLORS['rare']}"
                 f"Rare{WHITE}."),
            ])
    elif rarity == 'uncommon':
        if bestiary_ms < 4:
            player.npc_speak('grandma_wolf', [
                (f"Come back when you've reached {GOLD}Bestiary Milestone IV"
                 f" {WHITE}to upgrade it to {RARITY_COLORS['rare']}"
                 f"Rare{WHITE}."),
            ])
        else:
            player.pets[index].rarity = 'rare'
            player.npc_speak('grandma_wolf', [
                (f"There you go! I've upgraded your {RARITY_COLORS['rare']}"
                 f"Grandma Wolf Pet {WHITE}to {RARITY_COLORS['rare']}"
                 f"Uncommon{WHITE}!"),
                (f"Come back when you've reached {GOLD}Bestiary Milestone VI"
                 f" {WHITE}to upgrade it to {RARITY_COLORS['epic']}"
                 f"Epic{WHITE}."),
            ])
    elif rarity == 'rare':
        if bestiary_ms < 6:
            player.npc_speak('grandma_wolf', [
                (f"Come back when you've reached {GOLD}Bestiary Milestone VI"
                 f" {WHITE}to upgrade it to {RARITY_COLORS['epic']}"
                 f"Epic{WHITE}."),
            ])
        else:
            player.pets[index].rarity = 'epic'
            player.npc_speak('grandma_wolf', [
                (f"There you go! I've upgraded your {RARITY_COLORS['epic']}"
                 f"Grandma Wolf Pet {WHITE}to {RARITY_COLORS['epic']}"
                 f"Epic{WHITE}!"),
                (f"Come back when you've reached {GOLD}Bestiary Milestone VIII"
                 f" {WHITE}to upgrade it to {RARITY_COLORS['legendary']}"
                 f"Legendary{WHITE}."),
            ])
    elif rarity == 'epic':
        if bestiary_ms < 8:
            player.npc_speak('grandma_wolf', [
                (f"Come back when you've reached {GOLD}Bestiary Milestone VIII"
                 f" {WHITE}to upgrade it to {RARITY_COLORS['legendary']}"
                 f"Legendary{WHITE}."),
            ])
        else:
            player.pets[index].rarity = 'legendary'
            player.npc_speak('grandma_wolf', [
                (f"There you go! I've upgraded your {RARITY_COLORS['legendary']}"
                 f"Grandma Wolf Pet {WHITE}to {RARITY_COLORS['legendary']}"
                 f"Legendary{WHITE}!"),
                (f"I'm afraid that's all I can do for you."
                 " Thank you for helping this little old Grandma!"),
            ])
    elif rarity == 'legendary':
        player.npc_speak('grandma_wolf', [
            ("I've already upgraded your pet to the maximum tier!"
             " Leave this little old Grandma alone!"),
        ])
