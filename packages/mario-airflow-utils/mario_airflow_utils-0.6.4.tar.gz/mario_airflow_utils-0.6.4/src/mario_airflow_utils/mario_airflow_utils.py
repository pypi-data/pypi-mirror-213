"""mario_airflow_utils 모듈.

Please put in a description of the module.

Example:
    ``mario_airflow_utils`` 사용법은 아래와 같습니다.

        $ pip install ./
        $ mario_airflow_utils-ping

추가적인 설명은 여기에!

Attributes:
    nnn (int): ``사용되지 않는`` 시범용 변수

Todo:
    * 무한한 모듈의 발전 ``꿈``꾸며!
    * ``Dreaming`` of infinite module development!

"""
import sys
from airflow.operators.bash import BashOperator

nnn = 1

def hello():
    print("hi")
    return "hello"


def ping():
    """Example function with PEP 484 type annotations.

    Returns:
        리턴 없이 화면 print

    """
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
        print(f"{'p' * n}ong")
    else:
        print('pong')

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

if __name__ == "__main__":
    ping()
