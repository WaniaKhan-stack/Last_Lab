import random

# ==========================================
# 1. ENCAPSULATION & DATA HIDING
# ==========================================
class Environment:
    """Represents the world/room the agent interacts with."""
    def __init__(self, initial_temp: float , motion_detected : bool ):
        # Private attributes (encapsulation) preventing direct outside tampering
        self.__temperature = initial_temp
        self.__ac_on = False
        self.__motion_detected = motion_detected

    def get_motion_status(self) -> bool:
        return self.__motion_detected

    def set_motion_status(self, status: bool):
        self.__motion_detected = status

    # Getters and Setters to control access safely
    def get_temperature(self) -> float:
        return self.__temperature

    def set_temperature(self, value: float):
        self.__temperature = round(value, 2)

    def is_ac_on(self) -> bool:
        return self.__ac_on

    def set_ac_status(self, status: bool):
        self.__ac_on = status

    def simulate_weather(self):
        """Simulates environment changes over time."""
        # Randomly fluctuates temperature up or down
        change = random.choice([0.5, 1.0, -0.5])
        self.set_temperature(self.__temperature + change)

    def simulate_intruder(self) :
        select = random.choice([True, False])
        self.set_motion_status(select)


# ==========================================
# 2. BASE AGENT CLASS (Abstraction)
# ==========================================
class Agent:
    """A generic blueprint for a Software Agent."""
    def __init__(self, name: str):
        self.name = name

    def perceive(self, environment: Environment) -> float:
        """Senses the environment data."""
        raise NotImplementedError("Subclasses must implement perceive().")

    def think(self, perception_data: float) -> str:
        """Processes data and determines an action."""
        raise NotImplementedError("Subclasses must implement think().")

    def act(self, action: str, environment: Environment):
        """Executes the chosen action on the environment."""
        raise NotImplementedError("Subclasses must implement act().")

class SmartSecurityAgent(Agent):
    def __init__(self,name:str , alarm_triggered: bool = False ):
        super().__init__(name)
        self.__alarm_triggered = alarm_triggered

    def get_alarm_status(self) -> bool:
        return self.__alarm_triggered

    def set_alarm_status(self, status: bool):
        self.__alarm_triggered = status

    def perceive(self, environment: Environment) -> bool:
    
        motion = environment.get_motion_status()
        print(f"[{self.name}] Motion Detected: {motion}")
        return motion

    def think(self, motion_detected: bool) -> str:
        if motion_detected:
            return "TRIGGER_ALARM"
        return "STANDBY"

    def act(self, action: str, environment: Environment):
        if action == "TRIGGER_ALARM":
            self.set_alarm_status(True)
            print(f"[{self.name}] ALERT! Intruder detected! Alarm sounding! ")
        elif action == "STANDBY":
            self.set_alarm_status(False)
            print(f"[{self.name}] Room is secure.")

# ==========================================
# 3. INHERITANCE & POLYMORPHISM
# ==========================================
class SmartACAgent(Agent):
    """A specialized reflex agent inheriting from the base Agent class."""
    def __init__(self, name: str, threshold_temp: float):
        super().__init__(name)
        self.threshold = threshold_temp  # Target temperature trigger

    # Polymorphism: Overriding the base class methods with agent logic
    def perceive(self, environment: Environment) -> float:
        current_temp = environment.get_temperature()
        print(f"[{self.name}] Sensed Room Temperature: {current_temp}°C")
        return current_temp

    def think(self, current_temp: float) -> str:
        if current_temp > self.threshold:
            return "TURN_ON_AC"
        elif current_temp < (self.threshold - 2.0):
            return "TURN_OFF_AC"
        return "DO_NOTHING"

    def act(self, action: str, environment: Environment):
        if action == "TURN_ON_AC":
            if not environment.is_ac_on():
                environment.set_ac_status(True)
                print(f"[{self.name}] Action: 🟢 Turning ON the AC.")
            # AC lowers the room temperature
            environment.set_temperature(environment.get_temperature() - 1.5)
        
        elif action == "TURN_OFF_AC":
            if environment.is_ac_on():
                environment.set_ac_status(False)
                print(f"[{self.name}] Action: 🔴 Turning OFF the AC.")
                
        else:
            print(f"[{self.name}] Action: 💤 Maintaining status quo.")


# ==========================================
# 4. EXECUTION LOOP (Simulation)
# ==========================================
if __name__ == "__main__":
    living_room = Environment(initial_temp=26.0 , motion_detected=False) 
    # Instantiate both agents (Polymorphism in action!)

    climate_agent = SmartACAgent(name="ThermoAgent", threshold_temp=25.0)
    security_agent = SmartSecurityAgent(name="GuardAgent") # <-- Your new class
    print(f"--- Starting Multi-Agent Simulation ---")
    for step in range(1, 6):
        print(f"\n--- Hour {step} ---")
        # Simulate environment changes
        living_room.simulate_weather()
        living_room.simulate_intruder()
        # 1. Run Climate Agent Cycle
        temp_reading = climate_agent.perceive(living_room)
        ac_decision = climate_agent.think(temp_reading)
        climate_agent.act(ac_decision, living_room)
        # 2. Run Security Agent Cycle (Your Task)
        motion_reading = security_agent.perceive(living_room)
        sec_decision = security_agent.think(motion_reading)
        security_agent.act(sec_decision, living_room)

        print(
    f"Room Status -> AC On: {living_room.is_ac_on()}, "
    f"Real Temp: {living_room.get_temperature()}°C, "
    f"Alarm Triggered: {security_agent.get_alarm_status()}"
)