# System Boot Loader
from slick.core import SystemInitializer
from slick.memory import initialize_memory, apply_memory_bias, MEMORY_BANK
from slick.engine import SlickLogicEngine

def boot_system():
    # Initialize core systems
    initializer = SystemInitializer()
    init_status = initializer.initialize()
    
    # Initialize memory with bias
    mem_status = initialize_memory()
    apply_memory_bias()
    
    # Create logic engine
    engine = SlickLogicEngine()
    
    # Welcome message
    profile = initializer.profile
    welcome = f"{profile['name']} AI Online | Interests: {', '.join(profile['interests'])}"
    
    return f"{init_status} | {mem_status} | {welcome}"