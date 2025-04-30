import json
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from collections import defaultdict, Counter

class TestUtils:
    @staticmethod
    def load_json_file(file_path):
        """Load and parse a JSON file."""
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return {}

class RequirementsTraceability:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.sw_requirements = {}
        self.components = {}
        self.interfaces = {}
        self.unit_specs = {}
        self.test_cases = {
            'unit': [],
            'component': [],
            'interface': [],
            'integration': [],
            'sw_requirement': []
        }
        self.test_executions = {}
        self.releases = {}
        
        # Load all metadata
        self.load_all_data()
        
        # Process traceability
        self.traceability_matrix = self.build_traceability_matrix()
        
    def load_all_data(self):
        """Load all JSON files from the data directory structure."""
        # Load requirements metadata
        req_dir = os.path.join(self.data_dir, 'requirement_data')
        self.sw_requirements = TestUtils.load_json_file(os.path.join(req_dir, 'SW_requirements_metadata.json'))
        self.components = TestUtils.load_json_file(os.path.join(req_dir, 'component_metadata.json'))
        self.interfaces = TestUtils.load_json_file(os.path.join(req_dir, 'Interfaces_metadata.json'))
        self.unit_specs = TestUtils.load_json_file(os.path.join(req_dir, 'Unit_spec_meta_data.json'))
        
        # Load test case data
        test_case_dir = os.path.join(self.data_dir, 'test_case_data')
        self.test_cases['unit'] = TestUtils.load_json_file(os.path.join(test_case_dir, 'unit_tests.json')).get('unit_tests', [])
        self.test_cases['component'] = TestUtils.load_json_file(os.path.join(test_case_dir, 'component_tests.json')).get('component_tests', [])
        self.test_cases['interface'] = TestUtils.load_json_file(os.path.join(test_case_dir, 'interface_tests.json')).get('interface_tests', [])
        self.test_cases['integration'] = TestUtils.load_json_file(os.path.join(test_case_dir, 'integration_tests.json')).get('integration_tests', [])
        self.test_cases['sw_requirement'] = TestUtils.load_json_file(os.path.join(test_case_dir, 'sw_requirements_tests.json')).get('rq_based_tests', [])
        
        # Load test execution data
        exec_dir = os.path.join(self.data_dir, 'test_execution_data')
        for file_name in os.listdir(exec_dir):
            if file_name.startswith('release_') and file_name.endswith('.json'):
                release_id = file_name.split('.')[0]
                self.test_executions[release_id] = TestUtils.load_json_file(os.path.join(exec_dir, file_name))
        
        # Load release information
        releases_dir = os.path.join(self.data_dir, 'releases')
        release_info = TestUtils.load_json_file(os.path.join(releases_dir, 'release_info.json'))
        if 'releases' in release_info:
            for release in release_info['releases']:
                self.releases[release['release_id']] = release

    def build_traceability_matrix(self):
        """Build a traceability matrix connecting requirements to tests and components."""
        matrix = defaultdict(lambda: {
            'components': set(),
            'interfaces': set(),
            'unit_tests': set(),
            'component_tests': set(),
            'interface_tests': set(),
            'integration_tests': set(),
            'sw_requirement_tests': set()
        })
        
        # Map requirements to components
        for req_id, req_info in self.sw_requirements.items():
            if 'components' in req_info:
                matrix[req_id]['components'].update(req_info['components'])
            if 'interfaces' in req_info:
                matrix[req_id]['interfaces'].update(req_info['interfaces'])
                
        # Map requirements to tests
        for test_type, tests in self.test_cases.items():
            for test in tests:
                if 'linked_to' in test:
                    for req_id in test['linked_to']:
                        if test_type == 'unit':
                            matrix[req_id]['unit_tests'].add(test['id'])
                        elif test_type == 'component':
                            matrix[req_id]['component_tests'].add(test['id'])
                        elif test_type == 'interface':
                            matrix[req_id]['interface_tests'].add(test['id'])
                        elif test_type == 'integration':
                            matrix[req_id]['integration_tests'].add(test['id'])
                        elif test_type == 'sw_requirement':
                            matrix[req_id]['sw_requirement_tests'].add(test['id'])
                            
        # Convert sets to lists for JSON serialization
        for req_id, mappings in matrix.items():
            for key, value in mappings.items():
                matrix[req_id][key] = list(value)
                
        return matrix
    
    def calculate_coverage(self):
        """Calculate test coverage metrics."""
        coverage = {
            'requirements': {
                'total': len(self.sw_requirements),
                'covered': 0,
                'percentage': 0
            },
            'components': {
                'total': len(self.components),
                'covered': 0,
                'percentage': 0
            },
            'test_types': {}
        }
 
        # Calculate SW requirement coverage
        for req_id, mappings in self.traceability_matrix.items():
            has_tests = False
            for test_type in ['sw_requirement_tests']:
                if mappings[test_type]:
                    has_tests = True
                    break
            if has_tests:
                coverage['requirements']['covered'] += 1
       
        
        if coverage['requirements']['total'] > 0:
            coverage['requirements']['percentage'] = (coverage['requirements']['covered'] / coverage['requirements']['total']) * 100
            
        # Calculate component coverage
        components_with_tests = set()
        for test in self.test_cases['component']:
            if 'component_id' in test:
                components_with_tests.add(test['component_id'])
        
        coverage['components']['covered'] = len(components_with_tests)
        if coverage['components']['total'] > 0:
            coverage['components']['percentage'] = (coverage['components']['covered'] / coverage['components']['total']) * 100
            
        # Calculate coverage per test type
        test_types = ['unit', 'component', 'interface', 'integration', 'sw_requirement']
        for test_type in test_types:
            coverage['test_types'][test_type] = {
                'total': len(self.test_cases[test_type]),
                'covered_requirements': set()
            }
            
            for test in self.test_cases[test_type]:
                if 'linked_to' in test:
                    coverage['test_types'][test_type]['covered_requirements'].update(test['linked_to'])
                    
            coverage['test_types'][test_type]['covered_requirements'] = len(coverage['test_types'][test_type]['covered_requirements'])
            
        return coverage

    def calculate_pass_rates(self, release_id):
        """Calculate pass rates for a specific release."""
        if release_id not in self.test_executions:
            return None
            
        execution_data = self.test_executions[release_id]
        
        # Standardize keys - some files have spaces, others have underscores
        if 'component tests' in execution_data:
            execution_data['component_tests'] = execution_data.pop('component tests')
        if 'interface tests' in execution_data:
            execution_data['interface_tests'] = execution_data.pop('interface tests')
        if 'software requirement based tests' in execution_data:
            execution_data['software_requirement_based_tests'] = execution_data.pop('software requirement based tests')
            
        pass_rates = {}
        test_types = ['component_tests', 'interface_tests', 'software_requirement_based_tests']
        
        for test_type in test_types:
            if test_type in execution_data:
                total = len(execution_data[test_type])
                passed = sum(1 for test in execution_data[test_type] if test['test_execution_status'] == 'PASS')
                failed = sum(1 for test in execution_data[test_type] if test['test_execution_status'] == 'FAILED' or test['test_execution_status'] == 'FAIL')
                skipped = sum(1 for test in execution_data[test_type] if test['test_execution_status'] == 'SKIPPED')
                error = sum(1 for test in execution_data[test_type] if test['test_execution_status'] == 'ERROR_IN_TEST')
                executing = sum(1 for test in execution_data[test_type] if test['test_execution_status'] == 'EXECUTING')
                
                pass_rates[test_type] = {
                    'total': total,
                    'passed': passed,
                    'failed': failed,
                    'skipped': skipped,
                    'error': error,
                    'executing': executing,
                    'pass_rate': (passed / total * 100) if total > 0 else 0
                }
        
        return pass_rates


class DefectMetricsAnalyzer:
    def __init__(self, requirements_traceability):
        self.rt = requirements_traceability
        
    def get_defect_metrics(self):
        """Analyze defect metrics for all releases."""
        defect_metrics = {}
        
        for release_id, execution_data in self.rt.test_executions.items():
            defect_metrics[release_id] = {
                'by_component': defaultdict(int),
                'by_requirement': defaultdict(int),
                'total_defects': 0,
                'defect_list': []
            }

            # Standardize keys
            execution_data_normalized = self._normalize_execution_data(execution_data)
            
            # Analyze defects for each test type
            for test_type, tests in execution_data_normalized.items():
                for test in tests:
                    if 'defects' in test and test['defects']:
                        # Count defects
                        defect_metrics[release_id]['total_defects'] += len(test['defects'])
                        defect_metrics[release_id]['defect_list'].extend(test['defects'])
                        
                        # Map test to components and requirements
                        test_id = test['test_id']
                        components, requirements = self._map_test_to_components_and_requirements(test_id)
                        
                        # Increment defect counts
                        for component in components:
                            defect_metrics[release_id]['by_component'][component] += len(test['defects'])
                        
                        for requirement in requirements:
                            defect_metrics[release_id]['by_requirement'][requirement] += len(test['defects'])
            
            # Convert defaultdicts to regular dicts for serialization
            defect_metrics[release_id]['by_component'] = dict(defect_metrics[release_id]['by_component'])
            defect_metrics[release_id]['by_requirement'] = dict(defect_metrics[release_id]['by_requirement'])
        
        return defect_metrics
    
    def _normalize_execution_data(self, execution_data):
        """Normalize keys in execution data."""
        normalized = {}
        key_mapping = {
            'component tests': 'component_tests',
            'interface tests': 'interface_tests',
            'software requirement based tests': 'software_requirement_based_tests'
        }
        
        for key, value in execution_data.items():
            normalized_key = key_mapping.get(key, key)
            normalized[normalized_key] = value
            
        return normalized
    
    def _map_test_to_components_and_requirements(self, test_id):
        """Map a test ID to associated components and requirements."""
        components = set()
        requirements = set()
        
        # Check component tests
        for test in self.rt.test_cases['component']:
            if test.get('id') == test_id:
                if 'component_id' in test:
                    components.add(test['component_id'])
                if 'linked_to' in test:
                    requirements.update(test['linked_to'])
                break
        
        # Check other test types
        for test_type in ['unit', 'interface', 'integration', 'sw_requirement']:
            for test in self.rt.test_cases[test_type]:
                if test.get('id') == test_id:
                    if 'linked_to' in test:
                        requirements.update(test['linked_to'])
                    break
        
        # If no direct component mapping, try to find via requirements
        if not components:
            for req_id in requirements:
                if req_id in self.rt.sw_requirements and 'components' in self.rt.sw_requirements[req_id]:
                    components.update(self.rt.sw_requirements[req_id]['components'])
        
        return list(components), list(requirements)


class AutomationStatusAnalyzer:
    def __init__(self, requirements_traceability):
        self.rt = requirements_traceability
    
    def get_automation_status(self):
        """Analyze test automation status across all test types."""
        automation_status = {
            'total_tests': 0,
            'automated_tests': 0,
            'manual_tests': 0,
            'automation_rate': 0,
            'by_test_type': {}
        }
        
        executed_by_counter = Counter()
        
        # Combine all test executions to get the most complete picture
        all_executions = {}
        for release_id, release_executions in self.rt.test_executions.items():
            # for release_execution in release_executions.values():
            execution_data_normalized = self._normalize_execution_data(release_executions)
            for test_type, tests in execution_data_normalized.items():
                if test_type not in all_executions:
                    all_executions[test_type] = {}
                
                for test in tests:
                    test_id = test['test_id']
                    all_executions[test_type][test_id] = test
            
        # Calculate automation statistics
        for test_type, tests in all_executions.items():
            automation_status['by_test_type'][test_type] = {
                'total': len(tests),
                'automated': 0,
                'manual': 0,
                'automation_rate': 0
            }
            
            automation_status['total_tests'] += len(tests)
            
            for test_id, test in tests.items():
                if 'executed_by' in test:
                    executed_by = test['executed_by']
                    executed_by_counter[executed_by] += 1
                    
                    is_automated = 'Automation' in executed_by or 'automation' in executed_by
                    if is_automated:
                        automation_status['automated_tests'] += 1
                        automation_status['by_test_type'][test_type]['automated'] += 1
                    else:
                        automation_status['manual_tests'] += 1
                        automation_status['by_test_type'][test_type]['manual'] += 1
            
            # Calculate automation rate per test type
            if automation_status['by_test_type'][test_type]['total'] > 0:
                automation_status['by_test_type'][test_type]['automation_rate'] = (
                    automation_status['by_test_type'][test_type]['automated'] / 
                    automation_status['by_test_type'][test_type]['total'] * 100
                )
        
        # Calculate overall automation rate
        if automation_status['total_tests'] > 0:
            automation_status['automation_rate'] = (
                automation_status['automated_tests'] / 
                automation_status['total_tests'] * 100
            )
        
        # Add executor information
        automation_status['executors'] = dict(executed_by_counter)
        
        return automation_status
    
    def _normalize_execution_data(self, execution_data):
        """Normalize keys in execution data."""
        normalized = {}
        key_mapping = {
            'component tests': 'component_tests',
            'interface tests': 'interface_tests',
            'software requirement based tests': 'software_requirement_based_tests'
        }
        
        for key, value in execution_data.items():
            normalized_key = key_mapping.get(key, key)
            normalized[normalized_key] = value
            
        return normalized


class ReleaseInfoAnalyzer:
    def __init__(self, requirements_traceability):
        self.rt = requirements_traceability
    
    def get_release_info(self):
        """Get general information about software releases."""
        release_info = {}
        
        for release_id, release_data in self.rt.releases.items():
            release_info[release_id] = {
                'name': release_data.get('release_name', ''),
                'date': release_data.get('release_date', ''),
                'components': release_data.get('components', []),
                'requirements': release_data.get('software_requirements', []),
                'teams_involved': set(),
                'test_execution': {}
            }
            # Get test execution details if available
            if release_id in self.rt.test_executions.keys():
                execution_data = self.rt.test_executions[release_id]
                execution_data_normalized = self._normalize_execution_data(execution_data)
                
                # Count test statuses
                test_stats = {
                    'total': 0,
                    'passed': 0,
                    'failed': 0,
                    'skipped': 0,
                    'error': 0,
                    'executing': 0
                }
                for test_type, tests in execution_data_normalized.items():
                    for test in tests:
                        test_stats['total'] += 1
                        
                        # Collect teams involved
                        if 'executed_by' in test:
                            release_info[release_id]['teams_involved'].add(test['executed_by'])
                        
                        # Count statuses
                        status = test.get('test_execution_status', '').upper()
                        if status == 'PASS':
                            test_stats['passed'] += 1
                        elif status in ['FAIL', 'FAILED']:
                            test_stats['failed'] += 1
                        elif status == 'SKIPPED':
                            test_stats['skipped'] += 1
                        elif status == 'ERROR_IN_TEST':
                            test_stats['error'] += 1
                        elif status == 'EXECUTING':
                            test_stats['executing'] += 1
                
                release_info[release_id]['test_execution'] = test_stats
                release_info[release_id]['pass_rate'] = (
                    test_stats['passed'] / test_stats['total'] * 100 if test_stats['total'] > 0 else 0
                )
            
            # Convert set to list for serialization
            release_info[release_id]['teams_involved'] = list(release_info[release_id]['teams_involved'])
        
        return release_info
    
    def _normalize_execution_data(self, execution_data):
        """Normalize keys in execution data."""
        normalized = {}
        key_mapping = {
            'component tests': 'component_tests',
            'interface tests': 'interface_tests',
            'software requirement based tests': 'software_requirement_based_tests'
        }
        
        for key, value in execution_data.items():
            normalized_key = key_mapping.get(key, key)
            normalized[normalized_key] = value
            
        return normalized


class ReportGenerator:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.rt = RequirementsTraceability(data_dir)
        self.defect_analyzer = DefectMetricsAnalyzer(self.rt)
        self.automation_analyzer = AutomationStatusAnalyzer(self.rt)
        self.release_analyzer = ReleaseInfoAnalyzer(self.rt)
        
    def generate_report_data(self):
        """Generate all data needed for the report."""
        report_data = {
            'generated_on': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'traceability_matrix': self.rt.traceability_matrix,
            'coverage': self.rt.calculate_coverage(),
            'pass_rates': {},
            'defect_metrics': self.defect_analyzer.get_defect_metrics(),
            'automation_status': self.automation_analyzer.get_automation_status(),
            'release_info': self.release_analyzer.get_release_info()
        }
        
        # Calculate pass rates for each release
        for release_id in self.rt.test_executions:
            report_data['pass_rates'][release_id] = self.rt.calculate_pass_rates(release_id)
        
        return report_data
    
    def render_report(self, template_path='templates', output_file='test_report.html'):
        """Render the report using Jinja2."""
        env = Environment(loader=FileSystemLoader(template_path))
        template = env.get_template('report_template.html')
        
        report_data = self.generate_report_data()
        rendered_report = template.render(**report_data)
        
        with open(output_file, 'w') as f:
            f.write(rendered_report)
        
        print(f"Report generated successfully: {output_file}")


if __name__ == "__main__":
    # Create directories if they don't exist
    os.makedirs('data/releases', exist_ok=True)
    os.makedirs('data/requirement_data', exist_ok=True)
    os.makedirs('data/test_case_data', exist_ok=True)
    os.makedirs('data/test_execution_data', exist_ok=True)
    os.makedirs('report_templates', exist_ok=True)
    os.makedirs('temp', exist_ok=True)
    # Copy JSON files to appropriate directories
    # This would be needed in a real-world scenario where files are being loaded from different sources
    
    # Generate the report
    generator = ReportGenerator()
    generator.generate_report_data()
    generator.render_report(template_path = 'report_templates', output_file='test_report.html')