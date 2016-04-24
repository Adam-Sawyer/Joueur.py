# Generated by Creer at 03:31AM on April 24, 2016 UTC, git hash: '087b1901032ab5bed5806b24830233eac5c2de55'
# This is a simple class to represent the BroodMother object in the game. You can extend it by adding utility functions here in this file.

from games.spiders.spider import Spider

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add addtional import(s) here
# <<-- /Creer-Merge: imports -->>

class BroodMother(Spider):
    """The class representing the BroodMother in the Spiders game.

    The Spider Queen. She alone can spawn Spiderlings for each Player, and if she dies the owner loses.
    """

    def __init__(self):
        """Initializes a BroodMother with basic logic as provided by the Creer code generator."""
        Spider.__init__(self)

        # private attributes to hold the properties so they appear read only
        self._eggs = 0
        self._health = 0



    @property
    def eggs(self):
        """How many eggs the BroodMother has to spawn Spiderlings this turn.

        :rtype: float
        """
        return self._eggs


    @property
    def health(self):
        """How much health this BroodMother has left. When it reaches 0, she dies and her owner loses.

        :rtype: int
        """
        return self._health



    def consume(self, spiderling):
        """ Consumes a Spiderling of the same owner to regain some eggs to spawn more Spiderlings.

        Args:
            spiderling (Spiderling): The Spiderling to consume. It must be on the same Nest as this BroodMother.

        Returns:
            bool: True if the Spiderling was consumed. False otherwise.
        """
        return self._run_on_server('consume', spiderling=spiderling)


    def spawn(self, spiderlingType):
        """ Spawns a new Spiderling on the same Nest as this BroodMother, consuming an egg.

        Args:
            spiderling_type (str): The string name of the Spiderling class you want to Spawn. Must be 'Spitter', 'Weaver', or 'Cutter'.

        Returns:
            Spiderling: The newly spwaned Spiderling if successful. Null otherwise.
        """
        return self._run_on_server('spawn', spiderlingType=spiderlingType)


    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you want to add any client side logic (such as state checking functions) this is where you can add them
    # <<-- /Creer-Merge: functions -->>
