from reddit_secrets import *
from discord_secrets  import *


reddit = praw.Reddit(client_id=RedditClientID,
                     client_secret=RedditClientSecret,
                     user_agent=RedditClientAgent,
                     username = RedditUsername,
                     password = RedditPassword)
                     
client = discord.Client()
bot = commands.Bot(command_prefix= botPrefix)                   




@bot.command()
async def random_post(ctx, args):

    red = discord.Colour.red() 
    blue = discord.Colour.blue()
    
    async with ctx.channel.typing(): # Shows that the bot is typing
        rp_result = discord.Embed(title= "Random Reddit Post", colour=red)

        sub = reddit.subreddit(args) # get the subreddit from the command arguments

        if not sub.over18:
            post = list(sub.hot(limit=60)) # Retrieve 60 hot submissions from the subreddit.
            re = random.choice(post) # get one of them

            while re.over_18:
                re = random.choice(post) #pick another random submission if the one we have is NSFW

            rp_result.title = re.title  # embed title is same as reddit post title
            rp_result.url = re.url  # add link to the submission in case people want to check it out
            rp_result.set_footer(text="\nPosted by u/" + str(re.author))  # credit to post author

            if not re.is_self: # Text posts have is_self = True
                rp_result.set_image(url=re.url) # Now that we've determined it's an image post, include image in discord embed

            else:
                rp_result.description = re.selftext # Now that we've determined it's a text post, include text in discord embed

        else:
            #sub over 18
            rp_result.title="Sorry, I can't share that!"
            rp_result.description="That's an NSFW subreddit."

    await ctx.send(embed=rp_result)
    
    
bot.run(discordToken)
