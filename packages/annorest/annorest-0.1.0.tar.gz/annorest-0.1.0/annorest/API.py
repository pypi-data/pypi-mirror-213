import requests
BASE_URL  = ''
TOKEN = ''

# ========================
# Project相關
# ========================
def get_all_project():
    # headers = {
    #     # 'Content-Type': 'application/json',
    # }
    results = []
    res = requests.get(BASE_URL+ 'projects/', headers = headers).json()
    results += res['results']
    while res['next'] is not None:
        res = requests.get(res['next'], headers = headers).json()
        results += res['results']

    return results

def get_project():
    res = requests.get(BASE_URL+ 'projects/', headers = headers).json()
    id = [i['id'] for i in res['results'] if i['title'].startswith("ASE_AUTO_")]
    return id

def remove_project(project_id):
    return requests.delete(BASE_URL + 'projects/'+str(project_id) +"/", headers = headers)

def check_if_project_exist(project_name):
    headers = {
        # 'Content-Type': 'application/json',
        'Authorization': TOKEN
    }
    r = requests.get(BASE_URL+"projects/", headers = headers)
    for i in r.json()['results']:
        if i['title'] == project_name:
            return i['id']
    return False

def create_project(project_name, data=None):
    if data is None:
        data = {
            "title": project_name,
            "description": "",
            'label_config': '<View>\n  <Labels name="label" toName="text">\n    <Label value="GPE"/>\n    <Label value="PERSON"/>\n    <Label value="DATE"/>\n    <Label value="ORG"/>\n    <Label value="CARDINAL"/>\n    <Label value="NORP"/>\n    <Label value="LOC"/>\n    <Label value="TIME"/>\n    <Label value="FAC"/>\n    <Label value="MONEY"/>\n    <Label value="ORDINAL"/>\n    <Label value="EVENT-OTHER"/>\n    <Label value="WORK_OF_ART"/>\n    <Label value="QUANTITY"/>\n    <Label value="PERCENT"/>\n    <Label value="LANGUAGE"/>\n    <Label value="LAW"/>\n    <Label value="EVENT-MandA"/>\n    <Label value="EVENT-Financing"/>\n    <Label value="EVENT-CapitalIncrease"/>\n    <Label value="EVENT-Redirect"/>\n    <Label value="EVENT-OutOfStock"/>\n    <Label value="EVENT-PriceHikes"/>\n    <Label value="EVENT-PriceCut"/>\n    <Label value="EVENT-Policy"/>\n    <Label value="EVENT-Inflation"/>\n    <Label value="EVENT-PowerShortage"/>\n    <Label value="EVENT-PowerOutage"/>\n    <Label value="EVENT-Strike"/>\n    <Label value="EVENT-War"/>\n    <Label value="EVENT-Lawsuit"/>\n    <Label value="PRODUCT"/>\n    <Label value="TECH"/>\n    <Label value="EQPT"/>\n    <Label value="MATL"/>\n  </Labels>\n  <Text name="text" value="$text"/>\n</View>',
            "expert_instruction": "",
            "show_instruction": False,
            "show_skip_button": True,
            "enable_empty_annotation": True,
            "show_annotation_history": True,
            "organization": 1,
            'color': '#FFFFFF',
            "maximum_annotations": 1,
            "is_published": False,
            "model_version": "LighrNER1220",
            "is_draft": False,
            "created_by": {'id': 2,
                'first_name': '',
                'last_name': '',
                'email': 'neverleave0916@gmail.com',
                'avatar': None},
            "min_annotations_to_start_training": 0,
            "show_collab_predictions": True,
            "sampling": "Sequential sampling",
            "show_ground_truth_first": False,
            "show_overlap_first": False,
            "overlap_cohort_percentage": 100,
            "task_data_login": None,
            "task_data_password": None,
            "control_weights": { },
            "evaluate_predictions_automatically": False,
            "skip_queue": "REQUEUE_FOR_OTHERS",
            "reveal_preannotations_interactively": False,
            "pinned_at": None
        }
    # Create project
    headers = {'Authorization': TOKEN}
    r = requests.post(BASE_URL+"projects/", headers = headers, data = data)
    return r

# ========================
# Import Export
# ========================

def import_data(project_id, data):
    # Import Data
    headers = {
        'Content-Type': 'application/json',
        'Authorization': TOKEN
    }
    res = requests.post(BASE_URL+"projects/"+str(project_id)+'/import', headers = headers, data=data)
    if res.status_code == 201:
        print("Imported data to project: " + project_id)
        print("Tasks imported: " + str(res.json()['task_count']))
    # {'task_count': 94, 'annotation_count': 0, 'prediction_count': 94, 'duration': 0.0929405689239502, 'file_upload_ids': [], 'could_be_tasks_list': False, 'found_formats': [], 'data_columns': []}
    return project_id, res.json()
from pathlib import Path
import os
def export_data(project_id, exportType='JSON_MIN', save_path = None):
    # Import Data
    headers = {
        'Content-Type': 'application/json',
        'Authorization': TOKEN
    }
    params = {
        'exportType':exportType
    }
    res = requests.get(BASE_URL+"projects/"+str(project_id)+'/export', headers = headers, params=params)
    if save_path is not None:

        Path(os.path.dirname(save_path)).mkdir(parents=True, exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(res.content)
    return res.json()

headers = {
        'Content-Type': 'application/json',
        'Authorization': TOKEN
}
def import_to_labelstudio(project_name,f, create_if_not_exist = True, headers=headers):
    def check_if_exist(project_name):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': TOKEN
        }
        r = requests.get('https://labelstudio.tarflow.com/api/projects/', headers = headers)
        # print (r.json())
        for i in r.json()['results']:
            if i['title'] == project_name:
                return i['id']
        return None
    def create_project(project_name):
        dat = {"title": project_name,
        "description": "",
        'label_config': '<View>\n  <Labels name="label" toName="text">\n    <Label value="GPE"/>\n    <Label value="PERSON"/>\n    <Label value="DATE"/>\n    <Label value="ORG"/>\n    <Label value="CARDINAL"/>\n    <Label value="NORP"/>\n    <Label value="LOC"/>\n    <Label value="TIME"/>\n    <Label value="FAC"/>\n    <Label value="MONEY"/>\n    <Label value="ORDINAL"/>\n    <Label value="EVENT-OTHER"/>\n    <Label value="WORK_OF_ART"/>\n    <Label value="QUANTITY"/>\n    <Label value="PERCENT"/>\n    <Label value="LANGUAGE"/>\n    <Label value="LAW"/>\n    <Label value="EVENT-MandA"/>\n    <Label value="EVENT-Financing"/>\n    <Label value="EVENT-CapitalIncrease"/>\n    <Label value="EVENT-Redirect"/>\n    <Label value="EVENT-OutOfStock"/>\n    <Label value="EVENT-PriceHikes"/>\n    <Label value="EVENT-PriceCut"/>\n    <Label value="EVENT-Policy"/>\n    <Label value="EVENT-Inflation"/>\n    <Label value="EVENT-PowerShortage"/>\n    <Label value="EVENT-PowerOutage"/>\n    <Label value="EVENT-Strike"/>\n    <Label value="EVENT-War"/>\n    <Label value="EVENT-Lawsuit"/>\n    <Label value="PRODUCT"/>\n    <Label value="TECH"/>\n    <Label value="EQPT"/>\n    <Label value="MATL"/>\n  </Labels>\n  <Text name="text" value="$text"/>\n</View>',
        "expert_instruction": "",
        "show_instruction": False,
        "show_skip_button": True,
        "enable_empty_annotation": True,
        "show_annotation_history": True,
        "organization": 1,
        'color': '#FFFFFF',
        "maximum_annotations": 1,
        "is_published": False,
        "model_version": "LighrNER1220",
        "is_draft": False,
        "created_by": {'id': 2,
            'first_name': '',
            'last_name': '',
            'email': 'neverleave0916@gmail.com',
            'avatar': None},
        "min_annotations_to_start_training": 0,
        "show_collab_predictions": True,
        "sampling": "Sequential sampling",
        "show_ground_truth_first": False,
        "show_overlap_first": False,
        "overlap_cohort_percentage": 100,
        "task_data_login": None,
        "task_data_password": None,
        "control_weights": { },
        "evaluate_predictions_automatically": False,
        "skip_queue": "REQUEUE_FOR_OTHERS",
        "reveal_preannotations_interactively": False,
        "pinned_at": None
        }
        # print(dat)
        # Create project
        headers = {'Authorization': TOKEN}
        r = requests.post(BASE_URL+"projects/", headers = headers, data = dat)
        return r

    exist_result = check_if_exist(project_name)
    if exist_result is None:
        if create_if_not_exist:
            r = create_project(project_name)
            if r.status_code == 201:
                print ("Create project: " + project_name + "  ID: "+str(r.json()['id']))
                project_id = str(r.json()['id'])
            else:
                print(r.json())
        else:
            return "Project does not exist"
    else:
        print ("Project exist: " + project_name + "  ID: "+str(exist_result))
        project_id = str(exist_result)
    
    # Import Data
    headers = {
        'Content-Type': 'application/json',
        'Authorization': TOKEN
    }
    res = requests.post(BASE_URL+"projects/"+str(project_id)+'/import', headers = headers, data=f)
    if res.status_code == 201:
        print("Imported data to project: " + project_name)
        print("Tasks imported: " + str(res.json()['task_count']))
    # {'task_count': 94, 'annotation_count': 0, 'prediction_count': 94, 'duration': 0.0929405689239502, 'file_upload_ids': [], 'could_be_tasks_list': False, 'found_formats': [], 'data_columns': []}
    return project_id, res.json()
