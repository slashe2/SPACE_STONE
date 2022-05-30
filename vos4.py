import discord
from discord.http import Route

bot = discord.Client()
voted_data = {}
default_components = [
    {
        "type": 1,
        "components": [
            {
                "type": 2,
                "label": "Python",
                "style": 2,
                "custom_id": "python",
                "emoji": {
                    "id": "847876880257908757",
                    "name": "python"
                }
            }, {
                "type": 2,
                "label": "Kotlin",
                "style": 2,
                "custom_id": "kotlin",
                "emoji": {
                    "id": "847876848662216714",
                    "name": "kotlin"
                }
            }, {
                "type": 2,
                "label": "C언어",
                "style": 2,
                "custom_id": "c"
            }, {
                "type": 2,
                "label": "C++",
                "style": 2,
                "custom_id": "cpp",
                "emoji": {
                    "id": "847876987778629722",
                    "name": "cpp"
                }
            }, {
                "type": 2,
                "label": "Java",
                "style": 2,
                "custom_id": "java",
                "emoji": {
                    "id": "847876915619954708",
                    "name": "java"
                }
            }
        ]

    }
]
http = bot.http


@bot.event
async def on_ready():
    print("On Ready")


@bot.event
async def on_message(msg: discord.Message):
    if msg.content == "!프로그래밍":
        embed = discord.Embed(
            title="최고의 프로그래밍 언어",
            description="""<:python:847876880257908757> Python: 0표
                <:kotlin:847876848662216714> Kotlin: 0표
                C언어: 0표
                <:cpp:847876987778629722> C++: 0표
                <:java:847876915619954708> Java: 0표""",
            colour=0x0080ff
        )

        component1 = {
            "embed": embed.to_dict(),
                "components": default_components
        }

        response = await http.request(
            Route('POST', '/channels/{channel_id}/messages', channel_id=msg.channel.id), json=component1
        )
        print(response)
        voted_data[response.get("id")] = {
            "python": 0, "kotlin": 0, "java": 0, "cpp": 0, "c": 0
        }


@bot.event
async def on_socket_response(payload: dict):
    print(payload)
    if payload.get("t", "") == "INTERACTION_CREATE":
        d = payload.get("d", {})
        message = d.get("message", {})

        custom_id = d.get("data", {}).get("custom_id")

        voted_data[message.get("id", 0)][custom_id] += 1

        embed = discord.Embed(
            title="최고의 프로그래밍 언어",
            description="""<:python:847876880257908757> Python: {}표
                        <:kotlin:847876848662216714> Kotlin: {}표
                        C언어: {}표
                        <:cpp:847876987778629722> C++: {}표
                        <:java:847876915619954708> Java: {}표""".format(
                voted_data[message.get("id", 0)]['python'], voted_data[message.get("id", 0)]['kotlin'],
                voted_data[message.get("id", 0)]['c'], voted_data[message.get("id", 0)]['cpp'],
                voted_data[message.get("id", 0)]['java']),
            colour=0x0080ff
        )

        component2 = {
            "embed": embed.to_dict(),
            "components": default_components
        }

        await http.request(
            Route('PATCH', '/channels/{channel_id}/messages/{message_id}',
                  channel_id=message.get("channel_id"), message_id=message.get('id')), json=component2
        )

        interaction_id = d.get("id")
        interaction_token = d.get("token")
        await bot.http.request(
            Route("POST", f"/interactions/{interaction_id}/{interaction_token}/callback"),
            json={"type": 4, "data": {
                "content": "당신은 {}를 고르셨군요!".format(custom_id),
                "flags": 64
            }},
        )


bot.run("ODc2MDI1NTMzMzUwMTU4MzQ3.YReEWg.KZhXBpyJlHyTnE75ouvLeD2tB60")