# :car: Stacked Test Automation

This project demonstrates a **hybrid automation framework** for testing simulated Electronic Control Unit (ECU) functionalities. It combines the power of **Perl** for low-level, keyword-driven tests and **Robot Framework** for high-level, system-wide verification.

---

## :dart: Objective

To simulate and test ECU behaviors like **ignition control**, **diagnostic state changes**, and **CAN message verification** using:

- **Perl-based Keyword Driven Framework**: For fast, low-level testing (unit/component simulation)
- **Robot Framework**: For high-level functional, integration, and acceptance testing

Stacked test automation enables the realization of interdependencies between hardware-level behavior and business-level use cases, while allowing the entire framework to be maintained under a unified architecture.

--- 

## Architecture

The test architecture includes only the Perl and Robot tests and will be adapated to include the pytest framework in future

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
| - framework1.pl   |         | - <Robot Framework>    |
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

## :test_tube: Example Use Cases

- :toolbox: Simulated CAN frame state testing via Perl
- :clipboard: Log scraping and state monitoring via Robot Framework
- :vertical_traffic_light: Integration testing of full startup sequences
- :electric_plug: Business usecase and Low level usecase handled by a single testbed

---

## :file_folder: Directory Structure

``` bash
├── framework_perl_automation/  # Framework specific files using perl
│   ├── libraries/              # Perl module files
│   └── tests/                  # Perl test parameter files
├── framework_pytest/           # Pytest framework (specific to unit testing)
├── framework_robot/            # Robot framework files
│   ├── config/                 # Configuration for multiple variants
│   ├── __init__.robot          # Initialization steps (E.g. global setup, teardown)
│   ├── libraries/              # Library files (*.py)
│   ├── outputs/                # logs (export ROBOT_OPTIONS="--outputdir")
│   ├── resources/              # user-defined keywords
│   └── tests/                  # test files
├── requirements.txt            # dependencies for python
├── run_tests.sh                # orchestrator
├── simulator/                  # mocks to test the framework
├── testlist.txt                # testlist for perl automation framework
└── docs/                       # Documentation of the 
```

---

## :rocket: Running the Tests

Make the script executable and run:

```bash
chmod +x run_all.sh
./run_all.sh
```

--- 

## :link: Dependencies

+ Perl 5+ with basic modules (strict, warnings)
+ Python 3.6+
+ robotframework (Install via pip install robotframework)

---

## :arrows_counterclockwise: Extending the Framework

+ Add more keywords to Keywords.pm or Keywords.py
+ Use .par files for low-level scripted sequences
+ Use .robot files for higher-level workflows
+ Integrate hardware interface (e.g., CAN via SocketCAN or simulated USB HID)

## :black_nib: Contributions

Contributing PRs and suggestions are welcome! Especially if you can hook this to real or simulated ECUs using QEMU, CAN-utils, or serial interfaces. 🤝
