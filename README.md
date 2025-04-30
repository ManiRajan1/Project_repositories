## Configuration Mangament by API handlers
The aim of this project is to provide a set of modular and reusable API handler libraries that enable seamless integration and management of projects running on popular CI/CD platforms.
This objective of this project is to provide a solution for developers to update the necessary data for ASPICE assessments during the implementation, also automating the reports with compliance.


The entire project is demonstrated by two sections.
### Section 1:
In this section a samples of a metadata produced by the tools are included by the structure

### Section 2: 

These handlers are designed to interact with services like issue trackers (e.g., JIRA), documentation platforms (e.g., Confluence), and source control tools (e.g. GitLab), allowing for automated retrieval, processing, and analysis of project data.

In addition these API wrappers are created such that the API requests donot stress the infrastructure and aid to generate automated reports — such as test execution summaries, pipeline statuses, and release notes — to support continuous monitoring, traceability, and decision-making in DevOps workflows.

The project_utilities includes a data collector that creates 
    - traceability matrix 
    - defect matrix
    - test execution classified by necessary fields
    - A general overview of the project report

The related files are as below:
``` bash
.
├── libs
│   ├── Confluence_handler.py(./libs/Confluence_handler.py)
│   ├── Gitlab_handler.py(./libs/Confluence_handler.py)
│   ├── Jira_handler.py(./libs/Confluence_handler.py)
│   └── Xray_handler.py(./libs/Confluence_handler.py)
└── project_utilities
    └── project_specific_data_collector.py(./project_utilities/project_specific_data_collector.py)
```


The code repository of interest can be viewed by [PM_Rest_API_handlers](https://github.com/ManiRajan1/Project_repositories/tree/PM_Rest_API_handler) 