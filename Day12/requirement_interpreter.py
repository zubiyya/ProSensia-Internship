
import json
import importlib.util

# Load status_tracker module
spec = importlib.util.spec_from_file_location("status_tracker", "status_tracker.py")
status_tracker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(status_tracker)

def read_client_requirements(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    project = ''
    timeline = ''
    priority = ''
    features = []
    reading_features = False

    for line in lines:
        line = line.strip()
        if line.startswith('Project:'):
            project = line.replace('Project:', '').strip()
        elif line.startswith('Timeline:'):
            timeline = line.replace('Timeline:', '').strip()
        elif line.startswith('Priority:'):
            priority = line.replace('Priority:', '').strip()
        elif line.startswith('Features:'):
            reading_features = True
        elif reading_features:
            if line.startswith('-'):
                features.append(line[1:].strip())
            else:
                reading_features = False

    return project, timeline, priority, features

def generate_report(project, timeline, priority, features):
    report_lines = [
        "📘 Project Summary Report",
        "-------------------------",
        f"Project: {project}",
        f"Timeline: {timeline}",
        f"Priority: {priority}",
        "Features to Implement:"
    ]
    for feature in features:
        report_lines.append(f" - {feature}")
    return '\n'.join(report_lines)

def write_report_to_file(report, filename='project_summary.txt'):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(report)

def export_json(project, timeline, priority, features):
    status_dict = status_tracker.create_status_dict(features)
    summary_data = {
        "Project": project,
        "Timeline": timeline,
        "Priority": priority,
        "Features": status_dict
    }
    with open('project_summary.json', 'w', encoding='utf-8') as json_file:
        json.dump(summary_data, json_file, indent=4)

# Run everything
project, timeline, priority, features = read_client_requirements('client_requirements.txt')
report = generate_report(project, timeline, priority, features)
print(report)
write_report_to_file(report)
export_json(project, timeline, priority, features)

print("\n✅ All files created successfully!")
