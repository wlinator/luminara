import random


def load_level_message(level):
    if level in [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]:
        return f"Congratulations! You've reached **Level {level}** and earned a new level role!"
    elif level < 10:
        return random.choice(level_under_10).format(level)
    elif 10 < level < 20:
        return random.choice(level_10_to_20).format(level)
    elif 20 < level < 40:
        return random.choice(level_20_to_40).format(level)
    elif 40 < level < 60:
        return random.choice(level_40_to_60).format(level)
    elif level == 100:
        return level_100.format(level)
    else:
        return random.choice(level_above_60).format(level)


level_100 = "YOU HAVE REACHED **LEVEL {}**!!I know you have something to say and I know you're eager to say it so I'll " \
            "get right to the point: Shut " \
            "the fuck up. Nobody wants to hear it. Nobody will ever want to hear it. Nobody cares. And the fact that " \
            "you thought someone might care is honestly baffling to me. I've actually pulled the entire world. Here's " \
            "a composite of the faces of everybody who wants you to shut the fuck up. It seems as if this is a " \
            "composite of every human being on the planet. Interesting. Now for a composite of the faces that want " \
            "you to keep talking: Interesting, it seems as if nothing has happened. Here's the world map. Now here's " \
            "the text: Shut the fuck up. That's what you should do. But you know what? Maybe I am being a little too " \
            "harsh here. I actually do have it on good authority thanks to my pulling data that there is as at least " \
            "1 person who actually wants to hear you speak. It's a little child in Mozambique and he oh? He's dead? " \
            "Well sorry man I guess nobody wants to hear you talk anymore. Please shut the fuck up."


level_under_10 = [
    "Wow, look who finally managed to crawl their way to **Level {}**! Congrats, I guess.",
    "You're like a **Level {}** pebble in the vast ocean of talent. Keep striving!",
    "**Level {}**? That's cute. Maybe one day you'll reach mediocrity.",
    "Congratulations on **Level {}**! You must be so proud of yourself... or not.",
    "A wild **Level {}** appears! Brace yourself for mild amusement.",
    "Oh, **Level {}**! That's like a participation trophy, right?",
    "Achievement unlocked: **Level {}**! Your parents must be thrilled.",
    "Breaking news: **Level {}** has entered the chat! Prepare for underwhelming feats.",
    "Welcome to **Level {}**, where average is the new extraordinary.",
    "**Level {}**! Slow and steady wins the race... except when it comes to leveling up.",
    "Congratulations on **Level {}**. Your progress is... mildly amusing.",
    "Breaking news: **Level {}** has unlocked the 'Barely Trying' achievement!",
    "Attention, **Level {}**! Your achievement is about as significant as a grain of sand.",
    "Behold! **Level {}** has emerged from the shadows of insignificance.",
    "You've unlocked the 'Bare Minimum' achievement at **Level {}**. Bravo!",
    "Welcome to the realm of **Level {}**. Prepare for mild excitement.",
    "Congratulations on your ascent to **Level {}**. It's a small step for mankind.",
    "At **Level {}**, you're like a firework that fizzles out before it even begins.",
    "**Level {}** has been reached! Commence the average dance of mild enthusiasm.",
    "Alert! **Level {}** has been activated. Don't expect any fireworks.",
    "Congratulations on reaching **Level {}**. Let the underwhelming festivities commence!",
    "Rumor has it that reaching **Level {}** unlocks the ability to slightly impress others.",
    "**Level {}** has been achieved! Brace yourself for a lukewarm round of applause.",
    "You've made it to **Level {}**. Prepare for a dose of lukewarm recognition.",
    "At **Level {}**, you're one step closer to the realm of mild accomplishment.",
    "Rejoice! **Level {}** has been conquered, ushering in an era of moderate achievement.",
    "**Level {}** is here! Your accomplishment might raise an eyebrow or two.",
    "Congratulations on reaching **Level {}**. It's a humble feat, to say the least.",
    "Behold, **Level {}**! Let the celebration be as mild as the achievement itself.",
    "You've reached **Level {}**, where average becomes the new extraordinary.",
    "Prepare to be mildly impressed. It's **Level {}**, the master of slight accomplishments.",
    "Congratulations on unlocking the 'Just Getting Started' achievement at **Level {}**!",
    "Welcome to **Level {}**. It's like a lukewarm bath for your achievements.",
]


level_10_to_20 = [
    "Congratulations motherfucker you leveled the fuck up to **Level {}**.",
    "levle **{}** cmoning in! Let's celbraet!",
    "yay you reach the level **{}** waw you are so cool many time",
    "omg senpai you weach wevew **{}**",
    "reached **Level {}** but you'll never get on MY level HAAHAHAHAHA",
    "*elevator music* Welcome to **level {}**.",
    "Oh, look who's managed to crawl their way up to **Level {}**. Prepare for disappointment.",
    "Congratulations on reaching the underwhelming heights of **Level {}**. Your achievements astound no one.",
    "Ah, **Level {}**, where the bar is set so low even you can stumble over it.",
    "Bravo on reaching **Level {}**. It must be exhausting exerting such minimal effort.",
    "Welcome to the world of **Level {}**, where mediocrity is celebrated with empty enthusiasm.",
    "You've unlocked the dubious achievement of **Level {}**. Prepare for the resounding sound of indifference.",
    "Kudos on reaching **Level {}**. I'm sure the world will pause to celebrate this momentous occasion... just as "
    "soon as it remembers you exist.",
    "Prepare for the overwhelming roar of applause as you reach **Level {}**. Just kidding, it's more like the sound "
    "of crickets chirping in disappointment."
    "Behold, the prodigious talent of **Level {}**. Just kidding, there's nothing impressive about it.",
    "Well, well, well, **Level {}**. Your accomplishments are as impressive as a deflated balloon.",
    "Prepare for the parade in your honor, oh illustrious **Level {}**. Just kidding, no one cares.",
    "Ah, **Level {}**, where dreams come to die a slow and painful death. Enjoy your stay.",
    "Congratulations on reaching **Level {}**. Your insignificance knows no bounds.",
]

level_20_to_40 = [
    "Oh my god! Did you set up a macro for this? You're **level {}**!",
    "**Level {}**. If you don't stop leveling up... **I am going to commit a fucking war crime.**",
    "**Level {}** 👍",
    "Wow you're **level {}**. I regret not just using Tatsumaki bot for this.",
    "**Level {}**. If you don't stop leveling up, I might have to stage an intervention. Discord addiction is real!",
    "**Level {}**. Are you sure your life isn't just an elaborate Discord role-playing game?",
    "Look who's slacking off work to level up on Discord. **Level {}** and counting!",
    "**Level {}**? Have you considered that there might be an entire world outside of Discord?",
    "Congratulations on reaching **level {}**. Your dedication to Discord is truly unparalleled.",
    "Wow, you've climbed to **level {}**. Is Discord your full-time job now?",
    "**Level {}**. I bet your parents are so proud of the countless hours you've spent on Discord.",
    "Oh look, it's **level {}**! Are you sure you're not secretly a Discord bot in disguise?",
    "Achievement unlocked: **level {}**! You must have broken Discord's leveling algorithm by now.",
    "You've reached **level {}**. I hope you're using your Discord powers for good and not just spamming memes.",
    "**Level {}** and still going strong. Who needs a social life when you have Discord, right?",
    "Oh, **level {}**. I'm starting to think you might actually be a sentient Discord notification.",
    "Congratulations on leveling up to **level {}**. I hope Discord gives you a lifetime supply of virtual cookies.",
    "**Level {}**. At this rate, you'll surpass even the Discord founders in Discord addiction.",
    "Look who's made it to **level {}**. I'm starting to think you're more Discord than human.",
    "Wow, **level {}**! Do you ever wonder if Discord should be paying you a salary at this point?",
    "Congratulations on reaching **level {}**. Your dedication to Discord is both awe-inspiring and mildly concerning.",
    "You've unlocked the 'Master of Procrastination' achievement at **level {}**. Your parents must be so proud.",
    "**Level {}**? I bet you have more Discord badges than real-life achievements.",
    "Well, well, well, **level {}**. Your Discord addiction is reaching legendary status.",
]


level_40_to_60 = [
    "You've reached **Level {}**. Stop. Just stop. You've had enough of this app. Go away.",
    "TOUCH GRASS. You didn't deserve **Level {}** but here it is I guess..",
    "I'm so tired of giving you levels. I'm not even going to say which level you just reached. Just kidding it's **Level {}**."
    "Oh, look who's flexing their **Level {}** status. Don't strain a muscle.",
    "Congratulations on reaching **Level {}**. Are you trying to make the rest of us feel inadequate?",
    "Breaking news: **Level {}** has officially mastered the art of pressing buttons. Amazing.",
    "Hats off to **Level {}**. Your dedication is truly admirable... or slightly concerning.",
    "Are you okay...? **Level {}** is seriously unhealthy bro. Sleep.",
    "STOP. LEVELING. LEAVE. ME. ALONE. Here's your damn level: **{}**"
    "HAS REACHED **LEVEL {}**, FUCK YEAH."
    "**Level {}**. The second-hand embarrassment is real."
]

level_above_60 = [
    "You've weached **W-Wevew {}**. stawp. Just stawp. Y-Y-You've had enyough of this a-app. Go a-away.",
    "TOUCH GWASS. Y-You didn't d-desewve **W-Wevew {}** but h-hewe it is I guess..",
    "I'm so tiwed of giving you w-wevews. I'm nyot even going to say which wevew you just weached. Just kidding it's **{}**."
    "Oh, wook who's fwexing theiw **W-Wevew {}** status. Don't stwain a muscwe.",
    "Congwatuwations on weaching **W-Wevew {}**. Awe you twying to make the w-west of us feew inyadequate?",
    "Bweaking nyews: **W-Wevew {}** has officiawwy wiciawwy mastewed the awt of pwessing buttons. Amazing.",
    "Hats o-o-off to **W-Wevew {}**. Youw dedication is twuwy wuwy admiwabwe... ow swightwy wightwy concewnying.",
    "Awe you okay...? **W-Wevew {}** i-is s-s-sewiouswy wewiouswy unheawthy weawthy bwo. Sweep.",
    "STAWP. WEVEWING. WEAVE. ME. AWONYE. Hewe's youw dawn wevew: **{}**"
    "HAS WEACHED **WEVEW {}**, FWICK YEAH."
    "**Wevew {}**. The second-hand embawwassment is w-w-weaw."
]

