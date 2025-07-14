import matplotlib.pyplot as plt
import math
import random


class Voter:
    """Represents a voter with coordinates and party affiliation."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coordinates = (x, y)
        self.party = None
        self.color = None
    
    def find_nearest_party(self, party_list):
        """Find the closest party to this voter."""
        if not party_list:
            return None
            
        distances = [(self._distance_to_party(party), party) for party in party_list]
        return min(distances)[1]
    
    def find_nth_party(self, party_list, n):
        """Find the nth closest party to this voter (1-indexed)."""
        if n < 1 or n > len(party_list):
            raise ValueError(f"n={n} is out of range for {len(party_list)} parties")
        
        sorted_parties = sorted(party_list, key=lambda p: self._distance_to_party(p))
        return sorted_parties[n - 1]
    
    def _distance_to_party(self, party):
        """Calculate distance to a party."""
        return math.sqrt((self.x - party.x)**2 + (self.y - party.y)**2)
    
    def set_party(self, party):
        """Assign this voter to a party."""
        self.party = party
        self.color = party.color


class Party:
    """Represents a political party with position and color."""
    
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.coordinates = (x, y)
        self.color = color
        self.voters = []
    
    def add_voter(self, voter):
        """Add a voter to this party."""
        self.voters.append(voter)
        voter.set_party(self)
    
    def clear_voters(self):
        """Remove all voters from this party."""
        self.voters.clear()
    
    def get_voter_count(self):
        """Get the number of voters for this party."""
        return len(self.voters)


class VotingSimulation:
    """Main class for running voting simulations."""
    
    def __init__(self, num_voters, num_parties):
        self.num_voters = num_voters
        self.num_parties = num_parties
        self.voters = []
        self.parties = []
        self._initialize_simulation()
    
    def _initialize_simulation(self):
        """Initialize voters and parties."""
        self.voters = self._create_voters(self.num_voters)
        self.parties = self._create_parties(self.num_parties)
        self._assign_voters_to_parties()
    
    def _create_voters(self, count):
        """Create random voters within the coordinate space."""
        voters = []
        for _ in range(count):
            x = random.uniform(-100, 100)
            y = random.uniform(-100, 100)
            voters.append(Voter(x, y))
        return voters
    
    def _create_parties(self, count):
        """Create parties with random positions and colors."""
        parties = []
        for _ in range(count):
            x = random.uniform(-100, 100)
            y = random.uniform(-100, 100)
            color = self._generate_random_color()
            parties.append(Party(x, y, color))
        return parties
    
    def _generate_random_color(self):
        """Generate a random hex color."""
        hex_chars = "0123456789ABCDEF"
        return "#" + "".join(random.choice(hex_chars) for _ in range(6))
    
    def _assign_voters_to_parties(self):
        """Assign each voter to their nearest party."""
        # Clear existing assignments
        for party in self.parties:
            party.clear_voters()
        
        # Assign voters to nearest parties
        for voter in self.voters:
            nearest_party = voter.find_nearest_party(self.parties)
            if nearest_party:
                nearest_party.add_voter(voter)
    
    def get_voter_rankings(self):
        """Generate a dictionary with voter rankings of all parties.
        
        Returns:
            dict: Dictionary where keys are voter indices and values are lists
                  of parties ordered by preference (closest to farthest)
        """
        voter_rankings = {}
        
        for i, voter in enumerate(self.voters):
            # Sort parties by distance to this voter
            ranked_parties = sorted(self.parties, key=lambda p: voter._distance_to_party(p))
            voter_rankings[i] = ranked_parties
            
        return voter_rankings
    
    def print_voter_rankings(self, num_voters_to_show=5):
        """Print rankings for a sample of voters.
        
        Args:
            num_voters_to_show (int): Number of voters to display rankings for
        """
        rankings = self.get_voter_rankings()
        
        print(f"\n=== Sample Voter Rankings (showing {min(num_voters_to_show, len(self.voters))} voters) ===")
        
        for i in range(min(num_voters_to_show, len(self.voters))):
            voter = self.voters[i]
            ranked_parties = rankings[i]
            
            print(f"\nVoter {i} at ({voter.x:.1f}, {voter.y:.1f}):")
            for rank, party in enumerate(ranked_parties, 1):
                distance = voter._distance_to_party(party)
                party_idx = self.parties.index(party) + 1
                print(f"  {rank}. Party {party_idx} at ({party.x:.1f}, {party.y:.1f}) - Distance: {distance:.2f}")

    def get_nth_choice_results(self, n):
        """Get voting results for nth choice preferences."""
        if n < 1 or n > self.num_parties:
            raise ValueError(f"Choice {n} is out of range for {self.num_parties} parties")
        
        choice_counts = {}
        
        for voter in self.voters:
            try:
                nth_party = voter.find_nth_party(self.parties, n)
                color = nth_party.color
                choice_counts[color] = choice_counts.get(color, 0) + 1
            except ValueError:
                continue  # Skip if nth choice doesn't exist
        
        return choice_counts
    
    def plot_results(self):
        """Create comprehensive visualization of voting results."""
        # Calculate number of subplot rows needed
        num_charts = self.num_parties + 1  # Position plot + n choice charts
        rows = math.ceil(num_charts / 2) if num_charts > 2 else num_charts
        cols = 2 if num_charts > 2 else 1
        
        fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))
        
        # Ensure axes is always a list for consistent indexing
        if num_charts == 1:
            axes = [axes]
        elif rows == 1 and cols > 1:
            axes = axes.flatten()
        elif rows > 1:
            axes = axes.flatten()
        
        # Plot 1: Voter positions and party locations
        ax_pos = axes[0]
        self._plot_voter_positions(ax_pos)
        
        # Plot 2+: Pie charts for each choice preference
        chart_idx = 1
        for choice in range(1, self.num_parties + 1):
            if chart_idx < len(axes):
                self._plot_choice_pie_chart(axes[chart_idx], choice)
                chart_idx += 1
        
        # Hide any unused subplots
        for i in range(chart_idx, len(axes)):
            axes[i].axis('off')
        
        plt.tight_layout()
        plt.show()
    
    def _plot_voter_positions(self, ax):
        """Plot voter positions colored by party affiliation."""
        ax.spines['left'].set_position('center')
        ax.spines['bottom'].set_position('center')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title("Voter Positions and Party Locations")
        
        # Make the plot square
        ax.set_xlim(-100, 100)
        ax.set_ylim(-100, 100)
        ax.set_aspect('equal', adjustable='box')
        
        # Plot voters by party
        for party in self.parties:
            if party.voters:
                x_coords = [voter.x for voter in party.voters]
                y_coords = [voter.y for voter in party.voters]
                ax.scatter(x_coords, y_coords, c=party.color, alpha=0.6, s=20)
        
        # Plot party positions
        party_x = [party.x for party in self.parties]
        party_y = [party.y for party in self.parties]
        ax.scatter(party_x, party_y, marker="X", c='black', s=200, linewidth=2)
    
    def _plot_choice_pie_chart(self, ax, choice_num):
        """Plot pie chart for nth choice preferences."""
        try:
            choice_results = self.get_nth_choice_results(choice_num)
            
            if choice_results:
                values = list(choice_results.values())
                colors = list(choice_results.keys())
                
                ax.pie(values, colors=colors, autopct='%1.1f%%')
                ax.set_title(f"{self._ordinal(choice_num)} Choice Preferences")
            else:
                ax.text(0.5, 0.5, f'No {self._ordinal(choice_num)} choice data', 
                       ha='center', va='center', transform=ax.transAxes)
                ax.set_title(f"{self._ordinal(choice_num)} Choice Preferences")
        
        except ValueError as e:
            ax.text(0.5, 0.5, str(e), ha='center', va='center', transform=ax.transAxes)
            ax.set_title(f"{self._ordinal(choice_num)} Choice Preferences")
    
    def _ordinal(self, n):
        """Convert number to ordinal string (1st, 2nd, 3rd, etc.)."""
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return f"{n}{suffix}"
    
    def print_summary(self):
        """Print a summary of the simulation results."""
        print(f"\n=== Voting Simulation Summary ===")
        print(f"Total Voters: {self.num_voters}")
        print(f"Total Parties: {self.num_parties}")
        print(f"\nFirst Choice Results:")
        
        for i, party in enumerate(self.parties, 1):
            percentage = (party.get_voter_count() / self.num_voters) * 100
            print(f"  Party {i}: {party.get_voter_count()} votes ({percentage:.1f}%)")


def fptp(voting_information):
    """First-Past-The-Post voting system implementation."""
    party_votes = {}
    
    for voter in voting_information.values():
        first_choice = voter[0]  # Assume first choice is the most preferred
        party_votes[first_choice] = party_votes.get(first_choice, 0) + 1
    
    for party, votes in party_votes.items():
        print(f"Party {party.color} received {votes} votes.")
    


def main():
    """Main function to run the voting simulation."""
    # Configuration - easily adjustable parameters
    NUM_VOTERS = 1000
    NUM_PARTIES = 5
    
    print("Starting Voting Simulation...")
    print(f"Creating {NUM_VOTERS} voters and {NUM_PARTIES} parties...")
    
    # Create and run simulation
    simulation = VotingSimulation(NUM_VOTERS, NUM_PARTIES)
    
    # Display results
    simulation.print_summary()
    
    # Generate and optionally display voter rankings
    voter_rankings = simulation.get_voter_rankings()
    print(f"\nGenerated complete rankings for all {NUM_VOTERS} voters")
    
    fptp(voter_rankings)


    # Show sample rankings
    #simulation.print_voter_rankings(num_voters_to_show=3)
    
    # Display plots
    simulation.plot_results()


if __name__ == "__main__":
    main()