import m5
from m5.objects import *

# Create the system
system = System()

# Clock and voltage
system.clk_domain = SrcClockDomain(
    clock="1GHz",
    voltage_domain=VoltageDomain()
)

# Memory configuration
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MiB")]

# Create the CPU (MIPS pipelined CPU)
system.cpu = MipsMinorCPU()

# Create memory bus
system.membus = SystemXBar()

# Create instruction and data caches
system.icache = Cache(
    size="16kB",
    assoc=2,
    tag_latency=2,
    data_latency=2,
    response_latency=2,
    mshrs=4,
    tgts_per_mshr=20
)

system.dcache = Cache(
    size="16kB",
    assoc=2,
    tag_latency=2,
    data_latency=2,
    response_latency=2,
    mshrs=4,
    tgts_per_mshr=20
)

# Connect CPU to caches
system.cpu.icache_port = system.icache.cpu_side
system.cpu.dcache_port = system.dcache.cpu_side

# Connect caches to memory bus
system.icache.mem_side = system.membus.cpu_side_ports
system.dcache.mem_side = system.membus.cpu_side_ports

# Connect memory
system.system_port = system.membus.cpu_side_ports
system.memory = SimpleMemory(
    range=system.mem_ranges[0],
    latency="30ns"
)
system.memory.port = system.membus.mem_side_ports

# Configure MIPS program
import os
binary = os.path.join(os.path.dirname(os.path.abspath(__file__)), "program.elf")
system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

# Create interrupt controller
system.cpu.createInterruptController()

# Run simulation
root = Root(full_system=False, system=system)
m5.instantiate()

print("Starting MIPS pipeline simulation...")
exit_event = m5.simulate(10000000)

print("Simulation finished:", exit_event.getCause())
print("Simulated ticks:", m5.curTick())
