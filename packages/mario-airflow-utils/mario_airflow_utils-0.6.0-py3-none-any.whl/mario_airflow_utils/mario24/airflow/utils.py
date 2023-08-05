from airflow.operators.bash import BashOperator


def gen_bash_task(name: str, cmd: str, dag, trigger="all_success"):
    """airflow bash task 생성
        - trigger-rules : https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#trigger-rules
    """
    bash_task = BashOperator(
        task_id=name,
        bash_command=cmd,
        trigger_rule=trigger,
        dag=dag
    )
    return bash_task

def hello():
    print("hello")
    return "hello"
