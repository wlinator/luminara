import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from data.BlackJackStats import BlackJackStats
from data.Currency import Currency
from handlers.ItemHandler import ItemHandler
from main import economy_config, strings
from sb_tools import economy_embeds, economy_functions, universal, interaction, embeds

load_dotenv('.env')

active_blackjack_games = {}
special_balance_name = os.getenv("SPECIAL_BALANCE_NAME")
cash_balance_name = os.getenv("CASH_BALANCE_NAME")


class BlackJackCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

    @commands.slash_command(
        name="blackjack",
        description="Start a game of blackjack.",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def blackjack(self, ctx, *, bet: discord.Option(int)):

        # check if the player already has an active blackjack going
        if ctx.author.id in active_blackjack_games:
            await ctx.respond(embed=economy_embeds.already_playing("BlackJack"))
            return

        # Currency handler
        ctx_currency = Currency(ctx.author.id)

        # check if the user has enough cash
        player_cash_balance = ctx_currency.cash
        if bet > player_cash_balance or bet <= 0:
            await ctx.respond(embed=economy_embeds.not_enough_cash())
            return

        # check if the bet exceeds the bet limit
        bet_limit = int(economy_config["bet_limit"])
        if abs(bet) > bet_limit:
            message = strings["bet_limit"].format(ctx.author.name, Currency.format_human(bet_limit))
            return await ctx.respond(content=message)

        active_blackjack_games[ctx.author.id] = True

        try:

            player_hand = []
            dealer_hand = []
            deck = economy_functions.blackjack_get_new_deck()
            multiplier = float(economy_config["blackjack"]["reward_multiplier"])

            # deal initial cards (player draws two & dealer one)
            player_hand.append(economy_functions.blackjack_deal_card(deck))
            player_hand.append(economy_functions.blackjack_deal_card(deck))
            dealer_hand.append(economy_functions.blackjack_deal_card(deck))

            # calculate initial hands
            player_hand_value = economy_functions.blackjack_calculate_hand_value(player_hand)
            dealer_hand_value = economy_functions.blackjack_calculate_hand_value(dealer_hand)

            status = "game_start" if player_hand_value != 21 else "player_blackjack"
            view = interaction.BlackJackButtons(ctx) if status == "game_start" else None

            await ctx.respond(embed=economy_embeds.blackjack_show(ctx, Currency.format_human(bet), player_hand,
                                                                  dealer_hand, player_hand_value,
                                                                  dealer_hand_value, status=status), view=view,
                              content=ctx.author.mention)

            while status == "game_start":
                await view.wait()

                if view.clickedHit:
                    # player draws a card & value is calculated
                    player_hand.append(economy_functions.blackjack_deal_card(deck))
                    player_hand_value = economy_functions.blackjack_calculate_hand_value(player_hand)

                    if player_hand_value > 21:
                        status = "player_busted"
                    elif player_hand_value == 21:
                        status = "player_won_21"

                elif view.clickedStand:
                    # player stands, dealer draws cards until he wins OR busts
                    while dealer_hand_value <= player_hand_value:
                        dealer_hand.append(economy_functions.blackjack_deal_card(deck))
                        dealer_hand_value = economy_functions.blackjack_calculate_hand_value(dealer_hand)

                    if dealer_hand_value > 21:
                        status = "dealer_busted"
                    else:
                        status = "dealer_won"

                else:
                    status = "timed_out"
                    break

                # edit the embed, disable view if game is over.
                if status == "game_start":
                    view = interaction.BlackJackButtons(ctx)
                else:
                    view = None

                await ctx.edit(embed=economy_embeds.blackjack_show(ctx, bet, player_hand,
                                                                   dealer_hand, player_hand_value,
                                                                   dealer_hand_value, status=status), view=view,
                               content=ctx.author.mention)

            # change balance
            if status == "player_busted" or status == "dealer_won":
                ctx_currency.take_cash(bet)
                ctx_currency.push()

                # push stats (low priority)
                stats = BlackJackStats(
                    user_id=ctx.author.id,
                    is_won=False,
                    bet=bet,
                    payout=0,
                    hand_player=player_hand,
                    hand_dealer=dealer_hand
                )
                stats.push()

            elif status == "timed_out":
                await ctx.send(embed=economy_embeds.out_of_time(), content=ctx.author.mention)
                ctx_currency.take_cash(bet)
                ctx_currency.push()

            else:
                # bet multiplier
                payout = bet * multiplier if not status == "player_blackjack" else bet * 2
                ctx_currency.add_cash(payout)
                ctx_currency.push()

                item_reward = ItemHandler(ctx)
                await item_reward.rave_coin(is_won=True, bet=bet)
                await item_reward.bitch_coin(status=status)

                # push stats (low priority)
                stats = BlackJackStats(
                    user_id=ctx.author.id,
                    is_won=True,
                    bet=bet,
                    payout=payout,
                    hand_player=player_hand,
                    hand_dealer=dealer_hand
                )
                stats.push()

        except Exception as e:
            await ctx.respond(embed=embeds.command_error_1())
            print("Something went wrong in the gambling command:\n", e)

        finally:
            # remove player from active games list
            del active_blackjack_games[ctx.author.id]


def setup(sbbot):
    sbbot.add_cog(BlackJackCog(sbbot))
