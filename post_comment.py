import os
import requests
import json
import psycopg2
from psycopg2 import sql


def store_analysis_in_db(pr_number, branch_name, merge_status, analysis_text):
    conn = psycopg2.connect(
        dbname="sonarqube",
        user="sonar",
        password="sonarqube",
        host="65.1.55.202",
        port="5432"
    )
    cursor = conn.cursor()

    # Insert analysis results into PostgreSQL
    cursor.execute("""
        INSERT INTO analysis_results (pr_number, branch_name, merge_status, analysis_text)
        VALUES (%s, %s, %s, %s)
    """, (pr_number, branch_name, merge_status, analysis_text))

    conn.commit()
    conn.close()

def get_pull_request_number():
    # GitHub event data contains the pull request number
    with open(os.getenv('GITHUB_EVENT_PATH')) as f:
        event_data = json.load(f)
    return event_data['pull_request']['number']

def post_comment(comment):
    pr_number = get_pull_request_number()
    repo = os.getenv('GITHUB_REPOSITORY')
    token = os.getenv('TOKEN')  # Adjust the secret name as needed

    print(f"Repository: {repo}")
    print(f"Pull Request Number: {pr_number}")
    print(f"TOKEN: {token}")

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "body": comment
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 201:
        raise Exception(f"Error posting comment: {response.status_code}, {response.text}")

def main():
    pr_number = get_pull_request_number()
    branch_name = os.getenv('GITHUB_HEAD_REF')  # GitHub Actions environment variable
    merge_status = os.getenv('GITHUB_EVENT_NAME')  # Check if it's a pull_request event

    with open("analysis.txt", "r") as file:
        analysis = file.read()

    post_comment(analysis)
    store_analysis_in_db(pr_number, branch_name, merge_status, analysis)

if __name__ == "__main__":
    main()
