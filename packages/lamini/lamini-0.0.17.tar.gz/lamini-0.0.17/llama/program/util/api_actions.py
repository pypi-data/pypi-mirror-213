from typing import List

from llama.program.util.run_ai import (
    query_run_program,
    query_submit_program_to_batch,
    query_check_llama_program_status,
    query_get_llama_program_result,
    query_cancel_llama_program,
    query_submit_finetune_job,
    query_submit_data,
    query_clear_data,
)
from llama.program.value import Value


def gen_queue_batch(values: List[Value]):
    # Assume that all values have the same program
    program = values[0]._function.program.to_dict()
    params = {
        "program": program,
        "requested_values": [v._index for v in values],
    }
    response = query_submit_program_to_batch(params)
    response.raise_for_status()
    return response.json()


def gen_submit_training_job(value, id, model_name, prompt_key):
    # Assume that all values have the same program
    program = value._function.program.to_dict()
    params = {
        "id": id,
        "model_name": model_name,
        "data": program["examples"],
        "prompt_key": prompt_key,
    }
    response = query_submit_finetune_job(params)
    response.raise_for_status()
    return response.json()


def gen_check_job_status(job_id: str):
    # Assume that all values have the same program
    params = {
        "job_id": job_id,
    }
    response = query_check_llama_program_status(params)
    response.raise_for_status()
    return response.json()


def gen_job_results(job_id: str, output_type=None):
    # Assume that all values have the same program
    params = {
        "job_id": job_id,
    }
    response = query_get_llama_program_result(params)
    response.raise_for_status()
    response = response.json()
    if "Error" in response:
        return response
    if output_type is None:
        return response
    outputs = []
    for key, val in response.items():
        data = val["data"]
        for d in data:
            obj = output_type.parse_obj(d)
            outputs.append(obj)
    if len(outputs) == 1:
        return outputs[0]
    return outputs


def gen_cancel_job(job_id: str):
    # Assume that all values have the same program
    params = {
        "job_id": job_id,
    }
    response = query_cancel_llama_program(params)
    response.raise_for_status()
    return response.json()


def gen_submit_data(program, id):
    program = program.to_dict()
    params = {
        "id": id,
        "data": program["examples"],
    }
    response = query_submit_data(params)
    response.raise_for_status()
    return response.json()


def gen_clear_data(id):
    params = {
        "id": id,
    }
    response = query_clear_data(params)
    response.raise_for_status()
    return response.json()


def gen_multiple_values(values: List[Value]):
    # Assume that all values have the same program
    program = values[0]._function.program.to_dict()
    params = {
        "program": program,
        "requested_values": [v._index for v in values],
    }
    response = query_run_program(params)
    response.raise_for_status()
    for i, v in enumerate(values):
        index = v._index
        response_val = response.json()[str(index)]
        if isinstance(response_val["data"], list):
            v._data = []
            for d in response_val["data"]:
                v._data.append(v._type.parse_obj(d))
        else:
            v._data = v._type.parse_obj(response_val["data"])
    # Update cache once
    values[0]._function.program.builder.value_cache.update(response.json())
    return [value._data for value in values]


def gen_value(value: Value):
    value._compute_value()
    return value._data
