"""
Logic to decode AMD CPUs
"""
import re
def parse_amd_cpu(cpu):
    """
    Parse the CPU string to figure out some attributes
    Remember the value of cpu has already been sanitised by clean_cpu_string()
    so it won't contain (R), (TM), etc
    """

    cpulabels = {}
    if 'Ryzen' in cpu:
        # AMD Ryzen 7 5700G with Radeon Graphics
        # AMD Ryzen 7 PRO 5850U with Radeon Graphics
        # AMD Ryzen 7 5825U with Radeon Graphics
        # AMD Ryzen 9 7950X 16-Core Processor
        # AMD Ryzen Threadripper 3990X 64-Core Processor
        result = re.search(r"AMD ((\w+ \w+(?: PRO)?) (\d)\d+([A-Z]?))", cpu)
        cpulabels['cpuModel'] = result.group(1)
        cpulabels['cpuFamily'] = result.group(2)
        cpulabels['cpuGeneration'] = result.group(3)
        cpulabels['cpuLetter'] = result.group(4)
    elif 'EPYC' in cpu:
        # AMD EPYC 7J13 64-Core Processor
        # AMD EPYC 7742 64-Core Processor
        # AMD EPYC 7551P 32-Core Processor
        result = re.search(r"AMD ((\w+ \d) (\d)\w{3}([A-Z]?))", cpu)
        cpulabels['cpuModel'] = result.group(1)
        cpulabels['cpuFamily'] = result.group(2)
        cpulabels['cpuGeneration'] = result.group(3)
        cpulabels['cpuLetter'] = result.group(4)
    elif 'Opteron' in cpu:
        # AMD Opteron(tm) Processor 4133
        # AMD Opteron(tm) Processor 4310 EE
        # AMD Opteron(tm) Processor 6366 HE
        # Quad-Core AMD Opteron(tm) Processor 8356
        # Six-Core AMD Opteron(tm) Processor 8431
        result = re.search(r"AMD ((\w+) (\d{4}) ?([A-Z]{1,2}?)))", cpu)
        cpulabels['cpuModel'] = result.group(1)
        cpulabels['cpuFamily'] = result.group(2)
        cpulabels['cpuGeneration'] = result.group(3)
        cpulabels['cpuLetter'] = result.group(4)
    elif 'APU' in cpu:
        # AMD Athlon(tm) 5350 APU with Radeon(tm) R3
        result = re.search(r"AMD (((\w+) (\d)\d+) APU)", cpu)
        cpulabels['cpuModel'] = result.group(1)
        cpulabels['cpuFamily'] = result.group(2)
        cpulabels['cpuGeneration'] = result.group(3)
    return cpulabels