"""
Logic to decode Intel CPUs
"""
import re
def parse_intel_cpu(cpu):
    """
    Parse the CPU string to figure out some attributes
    Remember the value of cpu has already been sanitised by clean_cpu_string()
    so it won't contain (R), (TM), etc
    """

    cpulabels = {}
    if 'Gen' in cpu:
        # 11th Gen Intel(R) Core(TM) i7-1185G7 @ 3.00GHz
        # 11th Gen Intel(R) Core(TM) i7-11700K @ 3.60GHz
        # 11th Gen Intel(R) Core(TM) i9-11900 @ 2.50GHz
        # 12th Gen Intel(R) Core(TM) i7-1265U
        # 12th Gen Intel(R) Core(TM) i9-12900
        # 12th Gen Intel(R) Core(TM) i9-12900K
        result = re.search(r"(\d{2})th Gen Intel ((Core i\d)-\d{4}0?(\w)?)", cpu)
        cpulabels['cpuModel'] = result.group(2)
        cpulabels['cpuFamily'] = result.group(3)
        cpulabels['cpuGeneration'] = result.group(1)
        cpulabels['cpuLetter'] = result.group(4)

    elif 'Celeron' in cpu or 'Pentium' in cpu:
        # Intel(R) Celeron(R) CPU G1610 @ 2.60GHz
        result = re.search(r"Intel ((\w+) (\w)(\d)\d{3})", cpu)
        cpulabels['cpuModel'] = result.group(1)
        cpulabels['cpuFamily'] = result.group(2)
        cpulabels['cpuGeneration'] = result.group(4)
        cpulabels['cpuLetter'] = result.group(3)

    elif 'Core2' in cpu:
        # Intel(R) Core(TM)2 Quad CPU    Q9550  @ 2.83GHz
        result = re.search(r"Intel ((Core2 \w+) (\w)(\d)\d{3})", cpu)
        cpulabels['cpuModel'] = result.group(1)
        cpulabels['cpuFamily'] = result.group(2)
        cpulabels['cpuGeneration'] = result.group(4)
        cpulabels['cpuLetter'] = result.group(3)

    elif 'Platinum' in cpu or 'Gold' in cpu or 'Silver' in cpu or 'Bronze' in cpu:
        # Intel(R) Xeon(R) Platinum 8167M CPU @ 2.00GHz
        # Intel(R) Xeon(R) Platinum 8358 CPU @ 2.60GHz
        # Intel(R) Xeon(R) Gold 6226R CPU @ 2.90GHz
        # Intel(R) Xeon(R) Gold 6234 CPU @ 3.30GHz
        # Intel(R) Xeon(R) Silver 4110 CPU @ 2.10GHz
        # Intel(R) Xeon(R) Silver 4210R CPU @ 2.40GHz
        # Intel(R) Xeon(R) Bronze 3104 CPU @ 1.70GHz
        result = re.search(r"Intel ((Xeon \w+) (\d)\d{3}(\w)?)", cpu)
        cpulabels['cpuModel'] = result.group(1)
        cpulabels['cpuFamily'] = result.group(2)
        cpulabels['cpuGeneration'] = result.group(3)
        cpulabels['cpuLetter'] = result.group(4)

    elif 'E5' in cpu or 'E3' in cpu:
        # Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz
        # Intel(R) Xeon(R) CPU E5-2430L 0 @ 2.00GHz
        # Intel(R) Xeon(R) CPU E5-2687W 0 @ 3.10GHz
        # Intel(R) Xeon(R) CPU E5-4640 v2 @ 2.20GHz
        # Intel(R) Xeon(R) CPU E5-2630 v3 @ 2.40GHz
        # Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz
        # Intel(R) Xeon(R) CPU E3-1220 v5 @ 3.00GHz
        # Intel(R) Xeon(R) CPU E3-1220 v6 @ 3.00GHz
        result = re.search(r"Intel ((Xeon E\d)-\d{4}(\w)?(?: v(\d))?)", cpu)
        cpulabels['cpuModel'] = result.group(1)
        cpulabels['cpuFamily'] = result.group(2)
        cpulabels['cpuGeneration'] = result.group(4)
        cpulabels['cpuLetter'] = result.group(3)

    elif 'Xeon' in cpu:
        # Intel(R) Xeon(R) CPU           E5405  @ 2.00GHz
        # Intel(R) Xeon(R) CPU           X5460  @ 3.16GHz
        # Intel(R) Xeon(R) E-2286G CPU @ 4.00GHz
        # Intel(R) Xeon(R) W-1350 @ 3.30GHz
        # Intel(R) Xeon(R) W-2125 CPU @ 4.00GHz
        result = re.search(r"Intel ((Xeon \w)-?(\d)\d{3}(\w)?)", cpu)
        cpulabels['cpuModel'] = result.group(1)
        cpulabels['cpuFamily'] = result.group(2)
        cpulabels['cpuGeneration'] = result.group(3)
        cpulabels['cpuLetter'] = result.group(4)

    elif 'Core' in cpu:
        # Intel(R) Core(TM) i7 CPU         920  @ 2.67GHz
        # Intel(R) Core(TM) i7-2600 CPU @ 3.40GHz
        # Intel(R) Core(TM) i7-2600S CPU @ 2.80GHz
        # Intel(R) Core(TM) i5-2410M CPU @ 2.30GHz
        # Intel(R) Core(TM) i5-3470T CPU @ 2.90GHz
        # Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz
        # Intel(R) Core(TM) i7-3770S CPU @ 3.10GHz
        # Intel(R) Core(TM) i5-4590T CPU @ 2.00GHz
        # Intel(R) Core(TM) i3-4150 CPU @ 3.50GHz
        # Intel(R) Core(TM) i7-4790K CPU @ 4.00GHz
        # Intel(R) Core(TM) i5-6300U CPU @ 2.40GHz
        # Intel(R) Core(TM) i5-6500T CPU @ 2.50GHz
        # Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz
        # Intel(R) Core(TM) i7-6900K CPU @ 3.20GHz
        # Intel(R) Core(TM) i3-7100 CPU @ 3.90GHz
        # Intel(R) Core(TM) i7-7800X CPU @ 3.50GHz
        # Intel(R) Core(TM) i3-8100 CPU @ 3.60GHz
        # Intel(R) Core(TM) i7-8665U CPU @ 1.90GHz
        # Intel(R) Core(TM) i7-8086K CPU @ 4.00GHz
        # Intel(R) Core(TM) i3-9100 CPU @ 3.60GHz
        # Intel(R) Core(TM) i9-9900K CPU @ 3.60GHz
        # Intel(R) Core(TM) i7-10700K CPU @ 3.80GHz
        # Intel(R) Core(TM) i9-10900 CPU @ 2.80GHz
        # Intel(R) Core(TM) i9-10900X CPU @ 3.70GHz
        # Intel(R) Core(TM) i9-10980XE CPU @ 3.00GHz
        result = re.search(r"(Core i\d)-(\d)?\d{3,4}(\w)?", cpu)
        cpulabels['cpuModel'] = result.group(0)
        cpulabels['cpuFamily'] = result.group(1)
        cpulabels['cpuGeneration'] = result.group(2)
        cpulabels['cpuLetter'] = result.group(3)

    return cpulabels
