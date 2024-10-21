class SolutionAddon:
    def update_settings(self, settings):
        solution = settings.get("SOLUTION", "ai")
        discover = settings.get("SCRAPY_POET_DISCOVER", [])
        discover.append(f"solution.pages.{solution}")
        settings.set("SCRAPY_POET_DISCOVER", discover, "addon")
