#!/usr/bin/env Python
# coding=utf-8
# @Time : 2023/5/31 18:12
# @Author : ZhangYan
# @File : time_util.py
import pandas as pd
import numpy as np
from datetime import timedelta
import copy


def calculate_end_date(capacity_dict, s_t, l_t, reverse=False):
    """
    根据日历和加工时间推算完工时间
    :param capacity_dict:
    :param reverse:
    :param s_t:
    :param l_t:
    :return:
    """
    if l_t == timedelta():
        return [(s_t, s_t)]
    curr_d = pd.to_datetime(s_t.strftime("%Y-%m-%d"))
    result_list = []  # [(s_t, e_t)]
    while 1:
        last_d = curr_d - timedelta(days=1)
        # l_c_dict = capacity_dict.get(last_d, {
        #     'shift': timedelta(hours=24),
        #     "c_list": [
        #         {'s_t': last_d,
        #          'shift': timedelta(hours=24),
        #          "e_t": last_d + timedelta(hours=24)
        #          }
        #     ]
        # })
        # 获取当日产能
        c_dict = capacity_dict.get(
            curr_d,
            {
                "shift": timedelta(hours=24),
                "c_list": [{"s_t": curr_d, "shift": timedelta(hours=24), "e_t": curr_d + timedelta(hours=24)}],
            },
        )
        # c_list = l_c_dict["c_list"] + c_dict["c_list"]
        c_list = c_dict["c_list"]
        c_list = sorted([i for i in c_list if curr_d + timedelta(days=1) > i["s_t"] >= curr_d], key=lambda x: x["s_t"])
        # 如果当日有产能
        # if c_dict["shift"] != timedelta():
        if len(c_list) != 0:
            # for capacity in c_dict["c_list"][::(-1 if reverse else 1)]:
            for capacity in c_list[:: (-1 if reverse else 1)]:
                if (reverse and s_t <= capacity["s_t"]) or (not reverse and s_t >= capacity["e_t"]):
                    continue
                # 获取开始时间
                s_t = (
                    max(capacity["s_t"], min(s_t, capacity["e_t"]))
                    if reverse
                    else min(capacity["e_t"], max(s_t, capacity["s_t"]))
                )
                tmp = (s_t - l_t) if reverse else (s_t + l_t)
                # 如果当段时间产能不足
                if (reverse and tmp < capacity["s_t"]) or (not reverse and tmp > capacity["e_t"]):
                    e_t = capacity["s_t"] if reverse else capacity["e_t"]
                    l_t = (l_t - (s_t - e_t)) if reverse else (l_t - (e_t - s_t))
                    result_list.append((s_t, e_t))
                else:
                    e_t = (s_t - l_t) if reverse else (s_t + l_t)
                    l_t = timedelta()
                    result_list.append((s_t, e_t))
                    break
        curr_d += (-1 if reverse else 1) * timedelta(days=1)
        if l_t == timedelta():
            break
    return result_list


def generate_time_tag_by_type(fjsppool, currt_date, run_type=1, bottleneck=None):
    """
    1 为正排，2 为倒排，3为双向排， 4为check结果可行性
    :param fjsppool:
    :param currt_date:
    :param run_type:
    :return:
    """

    def generate_time_tag(fjsppool, currt_date, reverse=False, for_check=False, operations_done_dict=None):
        """
        给定machine上operation的顺序，为每个operation生成开始和结束时间，打时间戳支持三种方式：正向、倒向和正向check
        :param currt_date:
        :param operations_done_dict:
        :param for_check:
        :param fjsppool:
        :param reverse:
        :return:
        """
        if not for_check:
            start_time = pd.to_datetime(fjsppool.plan_start_date)
        else:
            start_time = pd.to_datetime(currt_date)
            reverse = False
        # 获取每个设备上opreation的顺序
        schedule_code = {
            m_id: (m.scheduled_ops if not reverse else m.scheduled_ops[::-1])
            for m_id, m in fjsppool.machine_dict.items()
            if len(m.scheduled_ops) > 0
        }
        # 标注每个设备当前遍历到的索引
        tmp_m_index = {m_id: 0 for m_id in schedule_code.keys()}
        # 标注设备上的op信息
        schedule_dict = {}  # {m_id: [op_id]}
        # 标注已经放到设备上的op的时间
        if operations_done_dict is None:
            operations_done_dict = {}  # {op_id: {s_t: ,e_t: }}
        while np.any([tmp_m_index[m_id] < len(scheduled_ops) for m_id, scheduled_ops in schedule_code.items()]):
            # 遍历每个设备
            for m_id, scheduled_op in schedule_code.items():
                if tmp_m_index[m_id] >= len(scheduled_op):
                    continue
                op_id = scheduled_op[tmp_m_index[m_id]]
                op = fjsppool.op_dict[op_id]
                if m_id not in schedule_dict:
                    schedule_dict[m_id] = []
                if op_id not in operations_done_dict:
                    operations_done_dict[op_id] = {}
                # 获取设备的上一个operation
                last_op_id = schedule_dict.get(m_id)[-1] if len(schedule_dict.get(m_id)) > 0 else None
                # 如果不是第一道工序且前置工序未完成
                if len(op.pre_ops if not reverse else op.next_ops) != 0 and np.any(
                    [len(operations_done_dict.get(op, {})) == 0 for op in (op.pre_ops if not reverse else op.next_ops)]
                ):
                    continue
                # 设备上一个op的结束时间和前置工序的最早结束时间（加了静置时间）
                tmp_m_t = start_time if last_op_id is None else operations_done_dict[last_op_id]["e_t"]
                tmp_job_t = (
                    [start_time]
                    if len(op.pre_ops if not reverse else op.next_ops) == 0
                    else [
                        operations_done_dict[last_op_id]["e_t"]
                        + timedelta(
                            seconds=fjsppool.standing_time.info.get(
                                (
                                    fjsppool.op_dict[last_op_id].product_id,
                                    fjsppool.op_dict[last_op_id].process_id,
                                )
                                if not reverse
                                else (op.product_id, op.process_id),
                            )
                            * (-1 if reverse else 1)
                        )
                        for last_op_id in (op.pre_ops if not reverse else op.next_ops)
                    ]
                )
                if reverse == False:
                    mad = pd.to_datetime(fjsppool.job_dict[fjsppool.op_dict[op_id].job_id].mad)
                    tmp_job_t.append(mad)
                else:
                    ots = pd.to_datetime(fjsppool.job_dict[fjsppool.op_dict[op_id].job_id].ots_time)
                    tmp_job_t.append(ots)
                # 如果是check，不允许开始时间比原始结果或当前时间或齐套时间更早
                if for_check:
                    mad = pd.to_datetime(fjsppool.job_dict[fjsppool.op_dict[op_id].job_id].mad)
                    tmp_job_t.append(max(fjsppool.op_dict[op_id].op_start, start_time, mad))
                # 换型时间
                change_time = timedelta(
                    seconds=(
                        fjsppool.changeover.info.get(
                            (
                                fjsppool.product_dict[fjsppool.op_dict[last_op_id].product_id].model,
                                fjsppool.op_dict[last_op_id].process_id,
                                fjsppool.product_dict[op.product_id].model,
                                op.process_id,
                                m_id,
                            )
                            if not reverse
                            else (
                                fjsppool.product_dict[op.product_id].model,
                                op.process_id,
                                fjsppool.product_dict[fjsppool.op_dict[last_op_id].product_id].model,
                                fjsppool.op_dict[last_op_id].process_id,
                                m_id,
                            ),
                            0,
                        )
                        if last_op_id is not None
                        else 0
                    )
                )
                min_start_change_t = tmp_m_t
                # min_start_change_t = min(tmp_m_t + tmp_job_t) if reverse else max(tmp_m_t + tmp_job_t)
                change_time_list = calculate_end_date(
                    fjsppool.machine_dict[m_id].calendar, min_start_change_t, change_time, reverse=reverse
                )
                min_s_t = (
                    min([change_time_list[-1][-1]] + tmp_job_t)
                    if reverse
                    else max([change_time_list[-1][-1]] + tmp_job_t)
                )
                lt = timedelta(seconds=op.machine_times[m_id])
                operation_time_list = calculate_end_date(
                    fjsppool.machine_dict[m_id].calendar, min_s_t, lt, reverse=reverse
                )
                s_t = operation_time_list[0][0]
                e_t = operation_time_list[-1][-1]
                if fjsppool.op_dict[op_id].op_start != min(s_t, e_t) or fjsppool.op_dict[op_id].op_end != max(s_t, e_t):
                    print(1)
                operations_done_dict[op_id].update({"s_t": s_t, "e_t": e_t})
                tmp_m_index[m_id] += 1
                schedule_dict[m_id].append(op_id)
        return operations_done_dict

    # 如果不是双向排程或者只是check结果合理性
    if run_type == 1:
        reverse = False
        operations_done_dict = generate_time_tag(fjsppool, currt_date, reverse=reverse)
    elif run_type == 2:
        reverse = True
        operations_done_dict = generate_time_tag(fjsppool, currt_date, reverse=reverse)
    elif run_type == 4:
        operations_done_dict = generate_time_tag(fjsppool, currt_date, for_check=True)
    elif run_type == 3 and bottleneck is not None:
        # 从瓶颈开始正向打时间
        reverse = False
        # 将pool的瓶颈工序置为第一道工序
        tmp_pool_1 = copy.deepcopy(fjsppool)
        for op_id, op in tmp_pool_1.op_dict.items():
            if op.process_id == bottleneck:
                # tmp_op_prcs_dict[op_id] = op.pre_ops
                op.pre_ops = []
        # TODO 推算瓶颈工序后面的工序
        for m_id, m in tmp_pool_1.machine_dict.items():
            m.scheduled_ops = [op_id for op_id in m.scheduled_ops if tmp_pool_1.op_dict[op_id].process_id >= bottleneck]
        operations_done_dict = generate_time_tag(tmp_pool_1, currt_date, reverse=reverse)

        # 开始从瓶颈倒向打时间
        reverse = True
        # 将pool的瓶颈工序置为第一道工序
        tmp_pool_2 = copy.deepcopy(fjsppool)
        tmp_pool_2.plan_start_date = max([j for i in operations_done_dict.values() for j in i.values()])
        for m_id, m in tmp_pool_2.machine_dict.items():
            m.scheduled_ops = [
                op_id for op_id in m.scheduled_ops[::-1] if tmp_pool_2.op_dict[op_id].process_id < bottleneck
            ]
        operations_done_dict = generate_time_tag(
            tmp_pool_2, currt_date, reverse=reverse, operations_done_dict=operations_done_dict
        )
    # 更新fjsppool中op的时间
    for op_id, d in operations_done_dict.items():
        fjsppool.op_dict[op_id].op_start = min(d["s_t"], d["e_t"])
        fjsppool.op_dict[op_id].op_end = max(d["s_t"], d["e_t"])
    # 如果是倒排或者双向排程，check开始时间是否超过当前时间，重新生成时间
    if run_type in [2, 3]:
        operations_done_dict = generate_time_tag(fjsppool, currt_date, reverse=False, for_check=True)
        for op_id, d in operations_done_dict.items():
            fjsppool.op_dict[op_id].op_start = min(d["s_t"], d["e_t"])
            fjsppool.op_dict[op_id].op_end = max(d["s_t"], d["e_t"])

    return fjsppool


if __name__ == "__main__":
    pass
