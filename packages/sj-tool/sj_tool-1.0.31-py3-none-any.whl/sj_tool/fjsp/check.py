from sj_tool.fjsp.entity.fjsp_pool import FjspPool
from datetime import timedelta


def find_op_machine(op_id: str, pool: FjspPool):
    avail_machine = pool.op_dict[op_id].available_machines
    for machine_id in avail_machine:
        if op_id in pool.machine_dict[machine_id].scheduled_ops:
            break

    return machine_id


def check_machine(pool: FjspPool):
    fail = False
    for machine_id in pool.machine_dict.keys():
        machine_object = pool.machine_dict[machine_id]
        m_scheduled_ops = machine_object.scheduled_ops
        for i in range(len(m_scheduled_ops)):
            op_id = m_scheduled_ops[i]
            op_available_machines = pool.op_dict[op_id].available_machines
            # 判断 是否能在 此机器上做
            if machine_id not in op_available_machines:
                fail = True
                break
            # 如果能做，判断与上个 operation 的交期
            else:
                if i == 0:
                    continue
                else:
                    cur_prcs_id = pool.op_dict[op_id].process_id
                    pre_prcs_id = pool.op_dict[m_scheduled_ops[i - 1]].process_id
                    cur_product = pool.op_dict[op_id].product_id
                    pre_product = pool.op_dict[m_scheduled_ops[i - 1]].product_id
                    cur_model = pool.product_dict[cur_product].model
                    pre_model = pool.product_dict[pre_product].model
                    changeover = timedelta(
                        seconds=pool.changeover.get(pre_model, pre_prcs_id, cur_model, cur_prcs_id, machine_id)
                    )
                    timecha = pool.op_dict[op_id].op_start - pool.op_dict[m_scheduled_ops[i - 1]].op_end
                    if timecha < changeover:
                        fail = True
                        break

        if fail:
            break

    return not fail


def check_job(pool: FjspPool):
    fail = False
    for op_id in pool.op_dict.keys():
        op_object = pool.op_dict[op_id]
        # 判断工时是否达标
        op_machine_id = find_op_machine(op_id, pool)
        operation_time = timedelta(seconds=op_object.machine_times[op_machine_id])
        timecha = op_object.op_start - op_object.op_end
        if operation_time != timecha:
            fail = True
            break
        # 如果工时达标，判断 静置时间是否符合
        else:
            pre_ops = op_object.pre_ops
            if len(pre_ops) == 0:
                continue
            else:
                fast_start = []
                for pre_op_id in pre_ops:
                    pre_op_end = pool.op_dict[pre_op_id].op_end
                    pre_process_id = pool.op_dict[pre_op_id].process_id
                    pre_product_id = pool.op_dict[pre_op_id].product_id
                    standing = pool.standing_time.get(pre_product_id, pre_process_id)
                    fast_start.append(pre_op_end + timedelta(seconds=standing))
                if max(fast_start) >= op_object.op_start:
                    fail = True
                    break

        if fail:
            break

    return not fail


def check_infeasibility(pool: FjspPool):
    pass_job = check_job(pool)
    pass_machine = check_machine(pool)

    if pass_job and pass_machine:
        return True
    else:
        return False
