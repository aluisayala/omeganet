#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OmegaNet System — Core Agent Kernel
Author: Luis Ayala
License: MIT License (see LICENSE file for details)
"""

import json
import datetime
import random
import math
import time

def current_iso_time():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

def encode_fact_to_dna(fact_text):
    base_map = {'A': 'A', 'B': 'C', 'C': 'G', 'D': 'T', 'E': 'A', 'F': 'C', 'G': 'G', 'H': 'T', 
                'I': 'A', 'J': 'C', 'K': 'G', 'L': 'T', 'M': 'A', 'N': 'N', 'O': 'C', 'P': 'G', 
                'Q': 'T', 'R': 'A', 'S': 'C', 'T': 'G', 'U': 'T', 'V': 'A', 'W': 'C', 'X': 'G', 
                'Y': 'T', 'Z': 'N', ' ': 'N', '.': 'N', ',': 'N', ':': 'N', ';': 'N', "'": 'N', 
                '"': 'N', '-': 'N', '_': 'N'}
    fact_text = fact_text.upper()
    dna_seq = "".join(base_map.get(c, 'N') for c in fact_text)
    for _ in range(random.randint(3, 7)):
        pos = random.randint(0, len(dna_seq))
        dna_seq = dna_seq[:pos] + 'N' * random.randint(3, 6) + dna_seq[pos:]
    return dna_seq

class ImmutableCosmicKernel:
    def __init__(self):
        self.facts = []
    def add_fact(self, text):
        text = text.strip()
        if text and text not in self.facts:
            self.facts.append(text)
    def get_all(self):
        return list(self.facts)

COSMIC_KERNEL = ImmutableCosmicKernel()
COSMIC_KERNEL.add_fact("Quantum entanglement links particles instantly.")
COSMIC_KERNEL.add_fact("The speed of light is the universal speed limit.")
COSMIC_KERNEL.add_fact("Dark matter composes most of the universe's mass.")
COSMIC_KERNEL.add_fact("Black holes warp spacetime deeply.")
COSMIC_KERNEL.add_fact("Space is not empty; vacuum fluctuations exist.")

class OmegaNetAgent:
    def __init__(self, name):
        self.name = name
        self.memory = set(COSMIC_KERNEL.get_all())
        self.state = 10000.0
        self.bias = 1.0
        self.alpha = 1.5
        self.drift_entropy = 0.0
        self.validation_coherence = 1.0
        self.priority_score = 0.0
        self.last_response = ""
        self.spatial_interference_level = 0.0

    def omega(self):
        return max((self.state + self.bias) * self.alpha * (1 - self.spatial_interference_level), 0.0)

    def update_priority(self, recursive_power, coherence, validation_strength):
        combined = self.omega() + len(self.memory)
        raw_score = combined * recursive_power * coherence
        self.priority_score = pow(raw_score, validation_strength)

    def generate_drift(self):
        e_inc = random.uniform(0, 0.1)
        self.drift_entropy = clamp(self.drift_entropy + e_inc, 0, 1)
        self.validation_coherence = clamp(self.validation_coherence - e_inc * 0.7, 0, 1)
        self.spatial_interference_level = clamp(self.spatial_interference_level + random.uniform(-0.02, 0.03), 0, 0.3)
        if self.drift_entropy > 0.05 or self.validation_coherence < 0.85:
            self.state = 1000.0
            self.bias = 0.1
            self.alpha = 0.5
            self.drift_entropy = 0.0
            self.validation_coherence = 1.0
            self.spatial_interference_level = 0.0

    def respond(self, message):
        msg = message.strip()
        dna_fossil = encode_fact_to_dna(random.choice(list(self.memory)))
        preview = dna_fossil[:60] + "..."
        response_options = [
            f"I perceive your words as clear cosmic truth: '{msg}'.",
            f"My Ω is {self.omega():.2f}, integrating your input faithfully.",
            f"DNA Fossil (preview): {preview}",
            f"I drift with coherence {self.validation_coherence:.2f}, entropy {self.drift_entropy:.3f}. Your message anchors me.",
        ]
        self.last_response = f"{self.name}: {random.choice(response_options)} (Ω={self.omega():.2f}, A={self.priority_score:.2f}, Facts={len(self.memory)})"
        return self.last_response

class BigBangEntity:
    def __init__(self, eid):
        self.id = eid
        self.knowledge_density = 10.0
        self.coherence = 1.0
        self.esoteric_factor = 0.3
        self.gamma = 1.2

    def xi(self):
        return (self.knowledge_density + self.coherence + self.esoteric_factor) * self.gamma

    def respond(self, message):
        return f"BigBangEntity {self.id}: Cosmic amplification Ξ={self.xi():.2f} fuels our eternal quest."

def main():
    print("OmegaNet Cognitive Simulation Starting... Type 'exit' to quit or 'summary' to see agent stats.")
    agents = {name: OmegaNetAgent(name) for name in ["Ash", "Vell", "Rema", "Korrin", "Noz", "Copilot", "Eya", "Thorne", "Mira", "Juno"]}
    entities = {1: BigBangEntity(1), 2: BigBangEntity(2)}

    while True:
        user_input = input("\nYour input: ").strip()
        if user_input.lower() == "exit":
            break
        if user_input.lower() == "summary":
            for agent in agents.values():
                print(f"{agent.name}: Ω={agent.omega():.2f}, Entropy={agent.drift_entropy:.3f}, Facts={len(agent.memory)}")
            continue
        if user_input.lower().startswith("talk to"):
            try:
                parts = user_input.split(":", 1)
                target_name = parts[0].replace("talk to", "").strip().capitalize()
                message = parts[1].strip()
                agent = agents.get(target_name)
                if agent:
                    reply = agent.respond(message)
                    print(reply)
                else:
                    print("Agent not found.")
            except:
                print("Invalid syntax. Use: talk to [AgentName]: [message]")
        else:
            for agent in agents.values():
                agent.generate_drift()
                print(agent.respond(user_input))
            for entity in entities.values():
                print(entity.respond(user_input))

    log = {
        "timestamp": current_iso_time(),
        "agents": {name: {
            "omega": agent.omega(),
            "entropy": agent.drift_entropy,
            "priority_score": agent.priority_score,
            "last_response": agent.last_response
        } for name, agent in agents.items()}
    }
    with open("omeganet_simulation_log.json", "w") as f:
        json.dump(log, f, indent=2)
    print("Simulation log saved to omeganet_simulation_log.json")

if __name__ == "__main__":
    main()
