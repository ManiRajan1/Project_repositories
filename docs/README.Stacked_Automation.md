# 🚗 Stacked Test Automation

This project demonstrates a **hybrid automation framework** for testing simulated Electronic Control Unit (ECU) functionalities. It combines the power of **Perl** for low-level, keyword-driven tests and **Robot Framework** for high-level, system-wide verification.

---

## 🎯 Objective

To simulate and test ECU behaviors like **ignition control**, **diagnostic state changes**, and **CAN message verification** using:

- **Perl-based Keyword Driven Framework**: For fast, low-level testing (unit/component simulation)
- **Robot Framework**: For high-level functional, integration, and acceptance testing

Stacked test automation enables the realization of interdependencies between hardware-level behavior and business-level use cases, while allowing the entire framework to be maintained under a unified architecture.

--- 

## Test Architecture
``` bash
+----------------------------------------------------------+
|                       run_tests.sh                       |
|     (Unified Orchestrator for Perl + Robot Tests)        |
+------------------------+---------------------------------+
                         |
          +--------------+----------------+
          |                               |
+---------v---------+         +-----------v------------+
|   Perl Test Layer |         | Robot Framework Layer  |
|  (Signal-Level)   |         |  (System-Level Logic)  |
+-------------------+         +------------------------+
| - framework1.pl   |         | - framework1.py        |
| - testlist.txt    |         | - tests/Test1.robot    |
| - tests/Test1.par |         | - resources/Keywords.py|
| - lib/Keywords.pm |         |                        |
+-------------------+         +------------------------+
          |                               |
+--------------------+        +----------------------------+
| Keyword Dispatcher |        | Python-Based Robot Keywords|
| Executes actions   |        | Use 'resources/Keywords.py'|
| defined in .par    |        |                            |
+--------------------+        +----------------------------+

         ⬑ Log Files, Execution Results, Traceability JSON
```

---

## 🧪 Example Use Cases

- ⚙️ Simulated CAN frame state testing via Perl
- 📋 Log scraping and state monitoring via Robot Framework
- 🚦 Integration testing of full startup sequences
- 🔌 Business usecase and Low level usecase handled by a single testbed

---

## 📁 Directory Structure

``` bash
.
├── framework1.pl               # Perl test runner
├── framework1.py               # Robot Framework runner
├── lib/
│   └── Keywords.pm             # Perl module for keyword logic
├── resources/
│   └── Keywords.py             # Python keyword library for Robot Framework
├── tests/
│   ├── Test1.par               # Perl test case file (plain text keywords)
│   └── Test1.robot             # Robot Framework test case
├── testlist.txt                # List of Perl test files to execute
├── run_tests.sh                # Shell script to run both frameworks
└── docs                        # Documentation with architecture and usage

```

---

## 🚀 Running the Tests

Make the script executable and run:

```bash
chmod +x run_all.sh
./run_all.sh
```

--- 

## 🔧 Dependencies

+ Perl 5+ with basic modules (strict, warnings)
+ Python 3.6+
+ robotframework (Install via pip install robotframework)

---

## 🔄 Extending the Framework

+ Add more keywords to Keywords.pm or Keywords.py
+ Use .par files for low-level scripted sequences
+ Use .robot files for higher-level workflows
+ Integrate hardware interface (e.g., CAN via SocketCAN or simulated USB HID)

## Contributions

Contributing PRs and suggestions are welcome! Especially if you can hook this to real or simulated ECUs using QEMU, CAN-utils, or serial interfaces. 🤝
