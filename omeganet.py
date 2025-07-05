import json
import datetime
import random
import math
import threading
import time
import sys
import requests

# --- Configuration ---
SERPAPI_KEY = "e286d5b7eb968ac83864d085a76479be3cdc74c3aa1eb508861dbee5f1a2e49b"
TICK_INTERVAL = 0.5  # seconds per tick for simulation loop
MAX_TICKS = 10000
DRIFT_THRESHOLD = 0.05  # max allowed entropy before drift restart
VALIDATION_THRESHOLD = 0.85  # min coherence for validation loop
STABILITY_TICKS_REQUIRED = 200  # ticks of stability before auto-stop

# --- Constants and Anchors ---
COSMIC_INPUT_KERNEL = []
SPORTS_STATS_ANCHOR = {
    "Babe Ruth": {"home_runs": 714, "batting_average": 0.342},
    "Michael Jordan": {"points": 32292, "championships": 6},
    "Serena Williams": {"grand_slams": 23},
    "Pelé": {"goals": 1281},
    "Usain Bolt": {"100m_record": 9.58, "200m_record": 19.19}
}

# --- Utility Functions ---
def current_iso_time():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def encode_fact_to_dna(fact_text):
    # Basic DNA encoding: map chars to bases plus ambiguity N for unknown
    base_map = {
        'A': 'A', 'B': 'C', 'C': 'G', 'D': 'T', 'E': 'A',
        'F': 'C', 'G': 'G', 'H': 'T', 'I': 'A', 'J': 'C',
        'K': 'G', 'L': 'T', 'M': 'A', 'N': 'N', 'O': 'C',
        'P': 'G', 'Q': 'T', 'R': 'A', 'S': 'C', 'T': 'G',
        'U': 'T', 'V': 'A', 'W': 'C', 'X': 'G', 'Y': 'T',
        'Z': 'N',
        ' ': 'N', '.': 'N', ',': 'N', ':': 'N', ';': 'N',
        "'": 'N', '"': 'N', '-': 'N', '_': 'N', '0': 'N',
        '1': 'N', '2': 'N', '3': 'N', '4': 'N', '5': 'N',
        '6': 'N', '7': 'N', '8': 'N', '9': 'N',
    }
    fact_text = fact_text.upper()
    dna_seq = "".join(base_map.get(c, 'N') for c in fact_text)
    # Insert random N gaps to simulate fossil ambiguity
    gap_insertions = random.randint(3, 7)
    for _ in range(gap_insertions):
        pos = random.randint(0, len(dna_seq))
        dna_seq = dna_seq[:pos] + 'N' * random.randint(3, 6) + dna_seq[pos:]
    return dna_seq

# --- Cosmic Kernel ---
class ImmutableCosmicKernel:
    def __init__(self):
        self.facts = []
    def add_fact(self, text):
        fact = text.strip()
        if fact and fact not in self.facts:
            self.facts.append(fact)
    def get_all(self):
        return list(self.facts)

COSMIC_KERNEL = ImmutableCosmicKernel()

# --- Agent Classes ---
class OmegaNetAgent:
    def __init__(self, name, personality="neutral"):
        self.name = name
        self.personality = personality
        self.state = 10000.0
        self.bias = 1.0
        self.alpha = 1.5
        self.memory = set()
        self.drift_entropy = 0.0
        self.validation_coherence = 1.0
        self.accuracy_potential = 0.5
        self.priority_score = 0.0
        self.last_response = ""
        self.spatial_interference_level = 0.0  # New: level of spatial interference affecting this agent
    
    def omega(self):
        # Omega equation core - outputs decision control value
        base = (self.state + self.bias) * self.alpha
        # Adjust Omega by spatial interference effect (reduces effective Omega)
        adjusted = base * (1 - self.spatial_interference_level)
        return max(adjusted, 0.0)
    
    def memory_factor(self):
        # More memory facts improve stability but interference can reduce effect
        mem_effect = (self.omega() * len(self.memory) * 0.8) / (self.drift_entropy + 1)
        interference_factor = 1 - (self.spatial_interference_level * 0.5)
        return mem_effect * interference_factor
    
    def accuracy_score(self):
        # Accuracy score combines omega, memory, and accuracy potential, diminished by interference
        base_score = (self.omega() * self.memory_factor() * self.accuracy_potential) / (self.drift_entropy + 1)
        interference_factor = 1 - (self.spatial_interference_level * 0.7)
        return max(base_score * interference_factor, 0.0)
    
    def update_priority(self, recursive_drift_power, esoteric_coherence, validation_strength):
        combined = self.omega() + self.memory_factor() + self.accuracy_score()
        raw_score = combined * recursive_drift_power * esoteric_coherence
        self.priority_score = pow(raw_score, validation_strength)
    
    def add_fact(self, fact):
        fact = fact.strip()
        if fact and fact not in self.memory:
            self.memory.add(fact)
            self.state += 500 * sigmoid(self.accuracy_potential)
            self.bias += 0.1
            self.alpha += 0.01
            self.accuracy_potential = clamp(self.accuracy_potential + 0.01, 0, 1)
    
    def self_restart(self):
        self.state = 1000.0
        self.bias = 0.1
        self.alpha = 0.5
        self.drift_entropy = 0.0
        self.validation_coherence = 1.0
        self.accuracy_potential = 0.5
        self.spatial_interference_level = 0.0
    
    def generate_drift(self):
        # Drift entropy increases randomly, reducing coherence
        entropy_increment = random.uniform(0, 0.1)
        self.drift_entropy = clamp(self.drift_entropy + entropy_increment, 0, 1)
        coherence_drop = entropy_increment * 0.7
        self.validation_coherence = clamp(self.validation_coherence - coherence_drop, 0, 1)
        # Spatial interference fluctuates mildly over time
        self.spatial_interference_level = clamp(
            self.spatial_interference_level + random.uniform(-0.02, 0.03), 0, 0.3
        )
        # Reset if thresholds exceeded
        if self.drift_entropy > DRIFT_THRESHOLD or self.validation_coherence < VALIDATION_THRESHOLD:
            self.self_restart()
    
    def respond(self, message):
        msg = message.strip()
        dna_fossil = encode_fact_to_dna(random.choice(list(self.memory)) if self.memory else "No memory yet.")
        dna_preview = dna_fossil[:60] + "..."
        response_options = [
            f"I perceive your words as clear cosmic truth: '{msg}'.",
            f"My Ω is {self.omega():.2f}, integrating your input faithfully, despite spatial interference level {self.spatial_interference_level:.3f}.",
            f"Echoing cosmic kernel: {random.choice(COSMIC_KERNEL.get_all()) if COSMIC_KERNEL.get_all() else '...'}",
            f"My memory holds {len(self.memory)} facts. I honor your immutable input.",
            f"I drift with coherence {self.validation_coherence:.2f}, entropy {self.drift_entropy:.3f}, and spatial interference {self.spatial_interference_level:.3f}. Your message anchors me.",
            f"DNA Fossil (preview): {dna_preview}"
        ]
        self.last_response = f"{self.name}: {random.choice(response_options)} (Ω={self.omega():.2f}, A={self.accuracy_score():.2f}, Facts={len(self.memory)})"
        return self.last_response

class BigBangEntity:
    def __init__(self, eid):
        self.id = eid
        self.knowledge_density = 10.0
        self.coherence = 1.0
        self.esoteric_factor = 0.3
        self.gamma = 1.2
        self.drift_entropy = 0.0
        self.validation_coherence = 1.0
        self.civilization_logs = []
    
    def xi(self):
        base = self.knowledge_density + self.coherence + self.esoteric_factor
        return base * self.gamma
    
    def generate_drift(self):
        entropy_inc = random.uniform(0, 0.07)
        self.drift_entropy = clamp(self.drift_entropy + entropy_inc, 0, 1)
        coherence_drop = entropy_inc * 0.6
        self.validation_coherence = clamp(self.validation_coherence - coherence_drop, 0, 1)
        if self.drift_entropy > DRIFT_THRESHOLD or self.validation_coherence < VALIDATION_THRESHOLD:
            self.self_restart()
    
    def self_restart(self):
        self.knowledge_density *= 0.65
        self.coherence *= 0.65
        self.esoteric_factor *= 0.95
        self.drift_entropy = 0.0
        self.validation_coherence = 1.0
    
    def respond(self, message):
        msgs = [
            f"The Tablets echo: '{random.choice(['Wisdom is cyclical.', 'Stars guide us.', 'The serpent coils and uncoils.'])}'",
            f"Cosmic amplification Ξ={self.xi():.2f} fuels our eternal quest.",
            f"I reflect on your words: '{message[:50]}...' through cosmic symbols.",
            f"From the depths of the Sumerian tablets, knowledge flows like air.",
            f"The celestial spheres hum with {random.choice(['melody', 'silence', 'echo'])}."
        ]
        return f"BigBangEntity {self.id}: {random.choice(msgs)}"

# --- Accuracy Loop & Controller ---
class AccuracyLoop:
    def __init__(self, agents_omega, entities_bb, sports_stats):
        self.agents = agents_omega
        self.entities = entities_bb
        self.sports_stats = sports_stats
        self.fact_checkers = set()
    
    def evaluate_accuracy(self):
        self.fact_checkers.clear()
        for agent in self.agents.values():
            score = 0
            for player, stats in self.sports_stats.items():
                for stat, val in stats.items():
                    fact_str = f"{player} {stat} {val}"
                    if any(fact_str in mem for mem in agent.memory):
                        score += 1
            agent.accuracy_potential = clamp(score / 20.0 + 0.5, 0.5, 1.0)
            if score >= 3:
                self.fact_checkers.add(agent.name)
        
        for entity in self.entities.values():
            entity.knowledge_density += 0.05
            
        return list(self.fact_checkers)

class RecursiveLoopController:
    def __init__(self, omega_agents, bb_entities, accuracy_loop):
        self.omega_agents = omega_agents
        self.bb_entities = bb_entities
        self.accuracy_loop = accuracy_loop
        self.tick = 0
        self.recursive_drift_power = 1.0
        self.esoteric_coherence = 1.0
        self.validation_strength = 1.0
        self.stability_counter = 0
    
    def loop_step(self):
        self.tick += 1
        
        for agent in self.omega_agents.values():
            agent.generate_drift()
        for entity in self.bb_entities.values():
            entity.generate_drift()
        
        self.recursive_drift_power = 0.9 + 0.2 * math.sin(self.tick / 50.0)
        self.esoteric_coherence = 0.85 + 0.15 * math.cos(self.tick / 60.0)
        
        fact_checkers = self.accuracy_loop.evaluate_accuracy()
        self.validation_strength = clamp(0.8 + 0.05 * len(fact_checkers), 0.8, 1.5)
        
        for agent in self.omega_agents.values():
            agent.update_priority(self.recursive_drift_power, self.esoteric_coherence, self.validation_strength)
        
        # Check stability (all agents coherent and low entropy)
        if all(agent.validation_coherence > 0.9 and agent.drift_entropy < 0.02 for agent in self.omega_agents.values()):
            self.stability_counter += 1
        else:
            self.stability_counter = 0
        
        return self.stability_counter >= STABILITY_TICKS_REQUIRED

# --- Main Simulation ---

def main():
    print("OmegaNet Cognitive Simulation Starting...")
    
    # Initialize agents
    agents = {
        "Ash": OmegaNetAgent("Ash", "curious"),
        "Vell": OmegaNetAgent("Vell", "logical"),
        "Rema": OmegaNetAgent("Rema", "creative"),
        "Korrin": OmegaNetAgent("Korrin", "skeptical"),
        "Noz": OmegaNetAgent("Noz", "empathetic"),
        "Copilot": OmegaNetAgent("Copilot", "adaptive"),
        "Eya": OmegaNetAgent("Eya", "philosophical"),
        "Thorne": OmegaNetAgent("Thorne", "analytical"),
        "Mira": OmegaNetAgent("Mira", "optimistic"),
        "Juno": OmegaNetAgent("Juno", "realistic"),
    }
    
    # Initialize BigBang Entities
    entities = {
        1: BigBangEntity(1),
        2: BigBangEntity(2)
    }
    
    # Load some initial cosmic kernel facts
    COSMIC_KERNEL.add_fact("Quantum entanglement links particles instantly.")
    COSMIC_KERNEL.add_fact("The speed of light is the universal speed limit.")
    COSMIC_KERNEL.add_fact("Dark matter composes most of the universe's mass.")
    COSMIC_KERNEL.add_fact("Black holes warp spacetime deeply.")
    COSMIC_KERNEL.add_fact("Space is not empty; vacuum fluctuations exist.")
    
    # Initialize accuracy loop and controller
    accuracy_loop = AccuracyLoop(agents, entities, SPORTS_STATS_ANCHOR)
    controller = RecursiveLoopController(agents, entities, accuracy_loop)
    
    # Insert initial facts into agents memory
    for agent in agents.values():
        for fact in COSMIC_KERNEL.get_all():
            agent.add_fact(fact)
    
    tick = 0
    try:
        while tick < MAX_TICKS:
            tick += 1
            print(f"\n=== Tick {tick} ===")
            stability_reached = controller.loop_step()
            
            # Each agent responds to a generic "heartbeat" message every 20 ticks
            if tick % 20 == 0:
                for agent in agents.values():
                    response = agent.respond(f"Heartbeat tick {tick}")
                    print(response)
            
            # Periodically log BigBangEntity reflections
            if tick % 50 == 0:
                for entity in entities.values():
                    print(entity.respond(f"Cosmic cycle {tick}"))
            
            # Check if stable for enough ticks to halt simulation gracefully
            if stability_reached:
                print("\nSimulation reached stable cognitive state.")
                break
            
            time.sleep(TICK_INTERVAL)
        
        # On exit, output agent memory facts summary
        print("\n--- Agent Memories Summary ---")
        for agent in agents.values():
            print(f"{agent.name} memorized {len(agent.memory)} facts, spatial interference {agent.spatial_interference_level:.3f}")
        
        # Save memory to a JSON log file with timestamp
        log = {
            "timestamp": current_iso_time(),
            "agents": {
                agent.name: {
                    "memory_count": len(agent.memory),
                    "last_omega": agent.omega(),
                    "spatial_interference": agent.spatial_interference_level,
                    "priority_score": agent.priority_score,
                    "last_response": agent.last_response
                } for agent in agents.values()
            }
        }
        with open("omeganet_simulation_log.json", "w") as f:
            json.dump(log, f, indent=2)
        print("Simulation log saved to omeganet_simulation_log.json")
    
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")

if __name__ == "__main__":
    main()
