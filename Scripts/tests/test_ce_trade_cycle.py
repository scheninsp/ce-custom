"""离线验证贸易周期编排的条件核验、事件序号、阶段转换及失败关闭；不连接 CE。"""

import copy
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ce_trade_cycle as cycle


def event(sequence=1, kind='add', raw='750000'):
    """构造目标提交事件；入参为序号、种类及原始数量，返回事件字典。"""
    return {'sequence': sequence, 'kind': kind, 'key': kind + '_0', 'quantityRaw': raw,
            'goodsId': 10, 'tableAddress': '3A484D9F8E8', 'counted': True,
            'ip': '1000', 'sp': '2000', 'caller': '3000'}


def controller(phase='counting', events=None):
    """创建不连接 CE 的阶段测试对象；入参为阶段及事件，返回编排器与快照。"""
    subject = object.__new__(cycle.Controller)
    subject.evidence = {'continuations': []}
    subject.state = {'phase': phase, 'lastSequence': 0, 'pending': None}
    subject.persist = Mock()
    snapshot = {'context': {'RIP': '1000', 'RSP': '2000', 'R14': 'AA'},
                'addresses': {'diagnostic': '4000'}, 'state': 'AA',
                'watch': {'events': events or [], 'errors': 0}}
    return subject, snapshot


class TradeCycleTests(unittest.TestCase):
    def test_exact_integer_sums(self):
        """验证大整数商品量没有浮点损失；无入参，无返回值。"""
        result = cycle.summarize([event(raw='9007199254740993'), event(2, raw='7')], 0)
        self.assertEqual(result['add_0'], {'count': 2, 'quantityRaw': '9007199254741000'})

    def test_summary_rejects_errors_and_duplicates(self):
        """验证条件错误和重复事件不能形成可信统计；无入参，无返回值。"""
        for events, errors in (([event()], 1), ([event(), event()], 0)):
            with self.assertRaises(ValueError):
                cycle.summarize(events, errors)

    def test_summary_rejects_wrong_target_and_quantity(self):
        """验证错误商品、州表、方向和数量失败关闭；无入参，无返回值。"""
        for key, value in (('goodsId', 43), ('tableAddress', 'FF'), ('key', 'add_2'),
                           ('quantityRaw', '-1'), ('quantityRaw', '7.5'), ('sequence', True)):
            altered = event()
            altered[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                cycle.summarize([altered], 0)

    def test_identical_registers_with_new_sequence(self):
        """验证相同现场的新序号不丢失；无入参，无返回值。"""
        subject, snapshot = controller(events=[event()])
        self.assertEqual(subject.recognize(snapshot), 'add')
        snapshot['watch']['events'].append(event(2))
        self.assertEqual(subject.recognize(snapshot), 'add')
        self.assertEqual(subject.state['lastSequence'], 2)

    def test_repeat_snapshot_is_not_a_new_event(self):
        """验证重复采集不消费第二次事件；无入参，无返回值。"""
        subject, snapshot = controller(events=[event()])
        subject.recognize(snapshot)
        with self.assertRaises(ValueError):
            subject.recognize(snapshot)
        self.assertEqual(subject.state['lastSequence'], 1)

    def test_boundary_transitions(self):
        """验证首次边界等待日期、下一边界等待封存；无入参，无返回值。"""
        for phase, expected in (('prepared', 'start_wait'), ('counting', 'end_wait')):
            boundary = event(kind='boundary')
            boundary['counted'] = phase == 'counting'
            subject, snapshot = controller(phase, [boundary])
            self.assertEqual(subject.recognize(snapshot), 'boundary')
            self.assertEqual(subject.state['phase'], expected)

    def test_missing_events_and_wrong_context_stop(self):
        """验证漏停点、错现场和未知暂停立即失败；无入参，无返回值。"""
        for events in ([], [event(), event(2)], [event(2)]):
            subject, snapshot = controller(events=events)
            with self.assertRaises(ValueError):
                subject.recognize(snapshot)
        subject, snapshot = controller(events=[event()])
        snapshot['context']['RIP'] = 'FF'
        with self.assertRaises(ValueError):
            subject.recognize(snapshot)

    def test_diagnostic_validates_state(self):
        """验证已知诊断只允许正确州；无入参，无返回值。"""
        subject, snapshot = controller()
        snapshot['context']['RIP'] = '4000'
        self.assertEqual(subject.recognize(snapshot), 'diagnostic')
        snapshot['context']['R14'] = 'BB'
        with self.assertRaises(ValueError):
            subject.recognize(snapshot)

    def test_run_requires_explicit_authorization(self):
        """验证无授权标记不能 Run；无入参，无返回值。"""
        subject, _snapshot = controller()
        subject.args = SimpleNamespace(allow_run=False)
        subject.client = Mock()
        with self.assertRaises(ValueError):
            subject.run_loop()
        subject.client.call.assert_not_called()

    def test_uncertain_run_is_not_retried(self):
        """验证未确认的 Run 不能自动重试；无入参，无返回值。"""
        subject, _snapshot = controller()
        subject.state['pending'] = {'accepted': False}
        subject.client = Mock()
        with self.assertRaises(ValueError):
            subject.wait_new(100)
        subject.client.call.assert_not_called()

    def test_run_loop_stops_at_boundary(self):
        """验证只发一次 Run 到边界且不执行下一周；无入参，无返回值。"""
        subject, initial = controller('prepared')
        initial['context']['RIP'] = '4000'
        initial['watch']['armed'] = False
        subject.instance = 'test'
        subject.args = SimpleNamespace(allow_run=True, wait_seconds=5, max_stops=3)
        subject.client = Mock()
        subject.client.tools.return_value = {'debugger_continue': {'inputSchema': {'properties': {'instanceId': {}}}}}
        subject.client.call.return_value = {'continued': True, 'mode': 'run'}
        subject.snapshot = Mock(return_value=initial)
        subject.audit = Mock()
        _unused, boundary = controller('prepared', [event(kind='boundary')])
        boundary['watch']['events'][0]['counted'] = False
        subject.wait_new = Mock(return_value=boundary)
        subject.run_loop()
        self.assertEqual(subject.state['phase'], 'start_wait')
        subject.client.call.assert_called_once_with('debugger_continue', {'instanceId': 'test'})

    def test_rejected_run_does_not_retry(self):
        """验证 Run 未接受只留待核验状态、不重发；无入参，无返回值。"""
        subject, initial = controller('prepared')
        initial['context']['RIP'] = '4000'
        initial['watch']['armed'] = False
        subject.instance = 'test'
        subject.evidence = {'continuations': []}
        subject.args = SimpleNamespace(allow_run=True, wait_seconds=5, max_stops=3)
        subject.client = Mock()
        subject.client.tools.return_value = {'debugger_continue': {'inputSchema': {'properties': {'instanceId': {}}}}}
        subject.client.call.return_value = {'continued': False, 'mode': 'run'}
        subject.snapshot = Mock(return_value=initial)
        subject.audit = Mock()
        with self.assertRaises(ValueError):
            subject.run_loop()
        self.assertEqual(subject.client.call.call_count, 1)
        self.assertFalse(subject.state['pending']['accepted'])

    def test_failed_audit_never_runs(self):
        """验证条件检查失败不会继续目标；无入参，无返回值。"""
        subject, initial = controller('prepared')
        initial['context']['RIP'] = '4000'
        initial['watch']['armed'] = False
        subject.args = SimpleNamespace(allow_run=True, wait_seconds=5, max_stops=3)
        subject.client = Mock()
        subject.snapshot = Mock(return_value=initial)
        subject.audit = Mock(side_effect=ValueError('Condition changed'))
        with self.assertRaises(ValueError):
            subject.run_loop()
        subject.client.call.assert_not_called()

    def test_seven_days_required(self):
        """验证日期恰好七天才接受；无入参，无返回值。"""
        cycle.validate_dates('1884-08-25', '1884-09-01')
        for end in ('1884-08-25', '1884-08-31', '1884-09-02'):
            with self.assertRaises(ValueError):
                cycle.validate_dates('1884-08-25', end)

    def test_native_rows_fail_closed(self):
        """验证禁用、删除及非执行停下行不接受；无入参，无返回值。"""
        good = {'row': {'fields': ['1', 'On Execute', 'Hardware (0)', 'Break', 'Yes']}}
        cycle.validate_row(good)
        for index, value in ((1, 'Write'), (3, 'Find code'), (4, 'No')):
            altered = copy.deepcopy(good)
            altered['row']['fields'][index] = value
            with self.assertRaises(ValueError):
                cycle.validate_row(altered)
        good['row']['fields'].append('Yes (10)')
        with self.assertRaises(ValueError):
            cycle.validate_row(good)

    def test_lua_backend_safety_contract(self):
        """验证比较发生在写入前、无 callback 和游戏写入；无入参，无返回值。"""
        native = cycle.HERE.joinpath('ce_native_condition.lua').read_text(encoding='utf-8')
        watch = cycle.HERE.joinpath('ce_trade_watch.lua').read_text(encoding='utf-8')
        self.assertIn("if mode == 'add' then", native)
        self.assertIn('request.expectedCondition', native)
        self.assertLess(native.index('normalizeCondition(previous.condition)'),
                        native.index("if mode ~= 'inspect' then"))
        for forbidden in ('debug_continueFromBreakpoint', 'debugger_onBreakpoint',
                          'debug_removeBreakpoint', 'writeInteger', 'writeQword'):
            self.assertNotIn(forbidden, native + watch)
        self.assertIn('watch.armed = false', watch)
        self.assertIn('watch.errors = watch.errors + 1', watch)


if __name__ == '__main__':
    unittest.main()
