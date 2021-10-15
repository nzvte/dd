    @Feature.Command(parent="jsk", name="rtt", aliases=["ping"])
    async def jsk_rtt(self, ctx: commands.Context):
        """
        Calculates Round-Trip Time to the API.
        """

        message = None

        # We'll show each of these readings as well as an average and standard deviation.
        api_readings = []
        # We'll also record websocket readings, but we'll only provide the average.
        websocket_readings = []

        # We do 6 iterations here.
        # This gives us 5 visible readings, because a request can't include the stats for itself.
        for _ in range(6):
            # First generate the text
            text = "Pegging ur dad\n\n"
            text += "\n".join(f"Peg #**{index + 1}** | **{reading * 1000:.2f}ms**" for index, reading in enumerate(api_readings))

            if api_readings:
                average = sum(api_readings) / len(api_readings)

                if len(api_readings) > 1:
                    stddev = math.sqrt(sum(math.pow(reading - average, 2) for reading in api_readings) / (len(api_readings) - 1))
                else:
                    stddev = 0.0

                text += f"\n\nAverage pegs: **{average * 1000:.2f}** | **{stddev * 1000:.2f}ms**"
            else:
                text += "\n\nNo pegs yet."

            if websocket_readings:
                average = sum(websocket_readings) / len(websocket_readings)

                text += f"\nPeg latency: **{average * 1000:.2f}ms**"
            else:
                text += f"\nPeg latency: **{self.bot.latency * 1000:.2f}ms**"

            # Now do the actual request and reading
            if message:
                before = time.perf_counter()
                await message.edit(embed=discord.Embed(color=0x00000, description=text))
                after = time.perf_counter()

                api_readings.append(after - before)
            else:
                before = time.perf_counter()
                message = await ctx.send(embed=discord.Embed(color=0x00000, description=text))
                after = time.perf_counter()
                api_readings.append(after - before)

            # Ignore websocket latencies that are 0 or negative because they usually mean we've got bad heartbeats
            if self.bot.latency > 0.0:
                websocket_readings.append(self.bot.latency)
