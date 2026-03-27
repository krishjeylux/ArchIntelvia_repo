# Low Power Architecture Principles
Title: Clock Gating

Concept:
Disables clock signal to inactive modules to save dynamic power.

Effect:
+ Reduces dynamic power
- Adds control logic

Use Case:
Idle or partially used hardware blocks.

Rules:
- Ensure glitch-free gating
- Enable only when safe

Title: Reduce Switching Activity

Concept:
Minimize unnecessary signal transitions on buses and registers.

Effect:
+ Saves dynamic power
- May require additional control logic

Use Case:
All digital designs with frequent transitions.

Rules:
- Avoid toggling unused signals
- Use stable default values

Title: Power vs Performance Tradeoff

Concept:
Adjusting power-saving modes can affect latency or throughput.

Effect:
+ Reduces energy usage
- Can increase latency or reduce throughput

Use Case:
Battery-operated or energy-constrained systems.

Rules:
- Apply selectively
- Prioritize critical paths

Title: Multi-VDD Domains

Concept:
Separate modules operate at different supply voltages to save power.

Effect:
+ Lowers static and dynamic power
- Requires level-shifters and careful design

Use Case:
Complex SoCs with high-performance and low-power blocks.

Rules:
- Isolate voltage domains
- Use level-shifters at interfaces

Title: Power Gating

Concept:
Completely shuts off power to idle modules.

Effect:
+ Eliminates leakage power
- Can cause wake-up latency

Use Case:
Rarely used functional blocks in SoCs.

Rules:
- Control gating carefully
- Manage wake-up sequences

Title: Dynamic Voltage and Frequency Scaling (DVFS)

Concept:
Adjust voltage and clock frequency dynamically based on workload.

Effect:
+ Reduces overall power consumption
- Requires monitoring and control logic

Use Case:
Processors and memory controllers under variable load.

Rules:
- Monitor utilization continuously
- Avoid frequent voltage changes

Title: Low-Power Memory Modes

Concept:
Memory can enter standby, sleep, or retention modes when idle.

Effect:
+ Saves both dynamic and leakage power
- May increase access latency

Use Case:
SRAM, DRAM, and cache memory blocks.

Rules:
- Ensure data retention in sleep mode
- Transition modes safely

Title: Glitch Reduction

Concept:
Reduce spurious transitions caused by combinational logic glitches.

Effect:
+ Reduces unnecessary switching power
- Requires careful logic design

Use Case:
Critical high-frequency logic paths.

Rules:
- Balance path delays
- Use synchronized outputs

Title: Operand Isolation

Concept:
Prevent unnecessary toggling in downstream logic when inputs do not change.

Effect:
+ Saves dynamic power
- Adds gating buffers

Use Case:
ALUs, multipliers, and memory write logic.

Rules:
- Isolate only non-critical signals
- Minimize extra buffers

Title: Bus Encoding for Low Power

Concept:
Reduce transitions on buses using Gray code or other encoding.

Effect:
+ Decreases switching activity
- Adds encoder/decoder overhead

Use Case:
Wide buses in SoCs or memory interfaces.

Rules:
- Use when bus toggling is significant
- Keep encoding logic minimal