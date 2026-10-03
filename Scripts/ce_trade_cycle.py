"""自动核验原生条件、编排 CE Run 与等待，统计九州木材一周的贸易提交；不写游戏内存。"""

import argparse
import json
import math
import sys
import time
import uuid
from datetime import date, datetime, timezone
from pathlib import Path

from ce_lua_common import execute_once, lua_quote, save_report, stopped_snapshot, validate_tools
from ce_mcp_client import McpClient
from get_stacktrace_register_at_breakpoint import (
    DEFAULT_GATEWAY, fingerprint, read_status, require_stopped, select_instance, validate_runtime,
)

HERE = Path(__file__).resolve().parent
KINDS = ('boundary', 'add', 'remove')
KEYS = ('add_0', 'remove_0', 'add_1', 'remove_1')
OLD_FILTER = """if RCX ~= 0x3A484D9F8E8 then return false end
assert(math.type(RDX) == 'integer' and RDX ~= 0, 'Invalid goods pointer')
local goodsId = readInteger(RDX + 0x10)
assert(goodsId ~= nil, 'Cannot read goods ID')
return goodsId == 10"""


def normalize(text):
    """统一原生条件换行；入参为字符串，返回不删除空白的文本。"""
    return text.replace('\r\n', '\n').replace('\r', '\n')


def lua_request(values):
    """编码固定后端请求；入参为字符串字典，返回 Lua 局部请求源码。"""
    return 'local request = {' + ','.join(key + '=' + lua_quote(value)
                                        for key, value in values.items()) + '}\n'


def validate_row(result):
    """校验安装版执行停下断点行；入参为原生回执，无返回值，未知格式失败关闭。"""
    fields = result.get('row', {}).get('fields', [])
    if (len(fields) not in (5, 6) or fields[0] != '1' or fields[1] != 'On Execute'
            or fields[3] != 'Break' or fields[4] != 'Yes'
            or (len(fields) == 6 and fields[5])):
        raise ValueError('Inactive, deleting, non-execute or unsupported native breakpoint row: ' + str(fields))


def summarize(events, errors):
    """精确求和并校验事件；入参为窗口提交事件及错误数，返回四类统计字典。"""
    if errors != 0:
        raise ValueError('Experiment contains condition errors')
    summary = {key: {'count': 0, 'quantityRaw': '0'} for key in KEYS}
    seen = set()
    for event in events:
        sequence = event['sequence']
        if type(sequence) is not int or sequence <= 0 or sequence in seen:
            raise ValueError('Invalid or duplicate event sequence')
        seen.add(sequence)
        key = event['key']
        raw_text = event['quantityRaw']
        if key not in summary or not isinstance(raw_text, str) or not raw_text.isdecimal():
            raise ValueError('Invalid event quantity or direction')
        if event.get('goodsId') != 10 or event.get('tableAddress') != '3A484D9F8E8':
            raise ValueError('Event target changed')
        summary[key]['count'] += 1
        summary[key]['quantityRaw'] = str(int(summary[key]['quantityRaw']) + int(raw_text))
    return summary


def validate_dates(start, end):
    """核验人工提供的周边界日期；入参为两个 ISO 日期，无返回值，非七天失败。"""
    if (date.fromisoformat(end) - date.fromisoformat(start)).days != 7:
        raise ValueError('Boundary dates must be exactly seven game days apart')


class Controller:
    def __init__(self, client, args, evidence):
        """建立编排器；入参为客户端、命令参数及证据字典，无返回值。"""
        self.client, self.args, self.evidence = client, args, evidence
        self.state = None
        self.instance = select_instance(client, args.instance_id)
        self.baseline = validate_runtime(client, self.instance)
        validate_tools(client.tools(), 'condition')
        process = self.baseline['overview']['process']
        if (process.get('processName', '').casefold() not in {'victoria3', 'victoria3.exe'}
                or process.get('pointerSize') != 8
                or self.baseline['info'].get('gates', {}).get('unsafeLua') is not True):
            raise ValueError('64-bit Victoria 3 and unsafeLua gate required')
        if self.baseline['fingerprint']['processId'] != 43884:
            raise ValueError('Confirmed target PID changed; re-identify the state before updating this script')
        evidence.update(instanceId=self.instance, baseline=self.baseline)

    def persist(self):
        """原子保存编排状态及当前证据；无入参，无返回值。"""
        if self.state is not None:
            save_report(self.args.state_file, self.state)
        save_report(Path(self.evidence['reportPath']), self.evidence)

    def check_identity(self):
        """核对目标会话未变化；无入参，无返回值。"""
        overview = self.client.call('runtime_get_overview', {'instanceId': self.instance})
        if fingerprint(overview) != self.baseline['fingerprint']:
            raise ValueError('Target session changed')
        if self.state is not None and (self.state['instanceId'] != self.instance
                or self.state['fingerprint'] != self.baseline['fingerprint']):
            raise ValueError('Saved experiment belongs to another target session')

    def lua(self, source, chunk):
        """执行一次固定 Lua 并先留证据；入参为源码及块名，返回唯一业务对象。"""
        self.check_identity()
        attempt = {'chunk': chunk, 'source': source, 'actionAttempted': False}
        self.evidence['requests'].append(attempt)
        self.persist()
        response = execute_once(self.client, self.instance, source, chunk, attempt)
        self.persist()
        values = response['returnValues']
        if len(values) != 1 or not isinstance(values[0], dict):
            raise ValueError('Expected one Lua object')
        self.check_identity()
        return values[0]

    def snapshot(self, action='snapshot'):
        """采集或启停实验并核对现场；入参为固定动作，返回完整快照。"""
        evidence = {}
        stopped_snapshot(self.client, self.instance, evidence)
        self.evidence['statuses'].append(evidence)
        request = {'action': action}
        if self.state is not None:
            request['id'] = self.state['id']
            if action == 'arm':
                request['expectedSequence'] = str(self.state['lastSequence'])
        before = evidence['context']['registers']
        result = self.lua(lua_request(request) + HERE.joinpath('ce_trade_watch.lua').read_text(encoding='utf-8'),
                          'trade_cycle_' + action)
        for register in ('RIP', 'RSP'):
            if result['context'][register] != before[register]:
                raise ValueError('Stopped context changed')
        if result['pid'] != self.baseline['fingerprint']['processId']:
            raise ValueError('Snapshot PID changed')
        if self.state is not None:
            if result['base'] != self.state['base']:
                raise ValueError('Module base changed')
            watch = result['watch']
            if not isinstance(watch, dict) or watch.get('id') != self.state['id']:
                raise ValueError('CE experiment missing or replaced')
            if watch['errors'] != 0:
                raise ValueError('Condition error: ' + watch['lastError'])
        self.evidence['snapshots'].append(result)
        self.persist()
        return result

    def native(self, kind, snapshot, mode='inspect', condition=None, old=None):
        """检查或比较更新一个既有条件；入参为种类、快照、模式、新旧文本，返回回执。"""
        request = {'mode': mode, 'address': snapshot['addresses'][kind],
                   'conditionType': 'complex', 'condition': condition or ''}
        if old is not None:
            request.update(expectedType=old['readbackConditionType'],
                           expectedCondition=normalize(old['readbackCondition']))
        result = self.lua(lua_request(request) + HERE.joinpath('ce_native_condition.lua').read_text(encoding='utf-8'),
                          'trade_native_' + mode)
        if result.get('ok') is not True or result.get('conditionReadbackMatched') is not True:
            raise ValueError('Native condition operation failed: ' + str(result))
        validate_row(result)
        if result['address'] != snapshot['addresses'][kind] or result.get('created') is not False:
            raise ValueError('Existing breakpoint receipt mismatch')
        if mode == 'update' and (result['readbackConditionType'] != 'complex'
                                or normalize(result['readbackCondition']) != condition):
            raise ValueError('Native condition readback mismatch')
        return result

    def audit(self, snapshot):
        """回读三个条件并核对原生配置；入参为快照，返回各地址回执字典。"""
        receipts = {kind: self.native(kind, snapshot) for kind in KINDS}
        if self.state is not None:
            for kind, result in receipts.items():
                if (result['readbackConditionType'] != 'complex'
                        or normalize(result['readbackCondition']) != self.state['conditions'][kind]):
                    raise ValueError('Experiment condition changed: ' + kind)
        return receipts

    def load(self):
        """读取持久化实验并验证会话；无入参，无返回值。"""
        self.state = json.loads(self.args.state_file.read_text(encoding='utf-8'))
        self.check_identity()
        if self.state['phase'] == 'preparing':
            raise ValueError('Preparation incomplete; inspect evidence before any retry')

    def prepare(self):
        """核验旧条件后创建并安装唯一实验；无入参，无返回值，不调用 Run。"""
        if self.args.state_file.exists():
            raise ValueError('State file already exists; do not replace an experiment')
        initial = self.snapshot()
        if initial['watch'] is not False:
            raise ValueError('CE already contains an experiment; do not replace it')
        old = self.audit(initial)
        if normalize(old['boundary']['readbackCondition']) not in {'', 'true', 'return true'}:
            raise ValueError('Unexpected boundary filter; refuse to overwrite')
        for kind in ('add', 'remove'):
            if (old[kind]['readbackConditionType'] != 'complex'
                    or normalize(old[kind]['readbackCondition']) != OLD_FILTER):
                raise ValueError('Unexpected target condition; refuse to overwrite')
        self.state = {'schemaVersion': 1, 'id': uuid.uuid4().hex, 'phase': 'preparing',
                      'instanceId': self.instance, 'fingerprint': self.baseline['fingerprint'],
                      'base': initial['base'], 'originalConditions': old, 'conditions': {},
                      'lastSequence': 0, 'pending': None, 'initial': initial}
        self.persist()
        initialized = self.snapshot('init')
        self.state['conditions'] = initialized['watch']['conditions']
        self.persist()
        for kind in KINDS:
            self.native(kind, initialized, 'update', self.state['conditions'][kind], old[kind])
        self.audit(initialized)
        self.state['phase'] = 'prepared'
        self.persist()

    def recognize(self, snapshot):
        """消费新暂停事件并转换阶段；入参为快照，返回停点种类，重复暂停不重复消费。"""
        watch = snapshot['watch']
        events = watch['events'] or []
        if not isinstance(events, list):
            raise ValueError('Invalid event list')
        if len(events) < self.state['lastSequence']:
            raise ValueError('Event sequence regressed')
        new = events[self.state['lastSequence']:]
        if len(new) > 1:
            raise ValueError('Multiple unobserved stops; external Run or coverage loss')
        if new:
            event = new[0]
            if event['sequence'] != self.state['lastSequence'] + 1:
                raise ValueError('Non-contiguous event sequence')
            if event['ip'] != snapshot['context']['RIP'] or event['sp'] != snapshot['context']['RSP']:
                raise ValueError('Event does not match stopped context')
            if event['kind'] == 'boundary':
                if event['counted'] != (self.state['phase'] == 'counting') or watch.get('armed', False):
                    raise ValueError('Boundary armed state does not match Python phase')
                if self.state['phase'] == 'prepared':
                    self.state.update(phase='start_wait', start=snapshot, startEvent=event)
                elif self.state['phase'] == 'counting':
                    self.state.update(phase='end_wait', end=snapshot, endEvent=event)
                else:
                    raise ValueError('Unexpected boundary in current phase')
                self.state['lastSequence'] = event['sequence']
                self.persist()
                return 'boundary'
            if event['kind'] not in ('add', 'remove'):
                raise ValueError('Unknown event kind')
            if event['counted'] != (self.state['phase'] == 'counting'):
                raise ValueError('Event armed state does not match Python phase')
            summarize([event], watch['errors'])
            self.state['lastSequence'] = event['sequence']
            self.persist()
            return event['kind']
        if snapshot['context']['RIP'] == snapshot['addresses']['diagnostic']:
            if snapshot['context']['R14'] != snapshot['state']:
                raise ValueError('Diagnostic breakpoint target changed')
            return 'diagnostic'
        raise ValueError('Unexpected or stale stop without a new experiment event')

    def wait_new(self, deadline):
        """等待已确认 Run 的新停止；入参为单调时间期限，返回快照，超时不再继续。"""
        pending = self.state['pending']
        if not pending or pending.get('accepted') is not True:
            raise ValueError('No confirmed Run to wait for; inspect uncertain action manually')
        while time.monotonic() < deadline:
            self.check_identity()
            status = read_status(self.client, self.instance, compat_available=True)
            if status.get('stateValid') is not True or status.get('attached') is not True or status.get('error'):
                raise ValueError('Invalid debugger state while waiting')
            if status.get('broken') is False:
                pending['observedRunning'] = True
                self.persist()
            else:
                require_stopped(status)
                snapshot = self.snapshot()
                events = snapshot['watch']['events'] or []
                if (len(events) > self.state['lastSequence'] or pending['observedRunning']
                        or snapshot['context'] != pending['context']):
                    self.state['pending'] = None
                    self.persist()
                    return snapshot
            time.sleep(self.args.poll_interval)
        raise TimeoutError('Wait expired; no further Run sent; target may still be running')

    def run_loop(self, wait_only=False):
        """逐次核验、Run、等待；入参为是否仅等待，无返回值，边界及异常停止推进。"""
        if self.state['phase'] not in {'prepared', 'counting'}:
            raise ValueError('Seek/advance require prepared/counting phase')
        if not wait_only and not self.args.allow_run:
            raise ValueError('Explicit --allow-run is required')
        deadline = time.monotonic() + self.args.wait_seconds
        if wait_only or self.state['pending'] is not None:
            current = self.wait_new(deadline)
            kind = self.recognize(current)
            if wait_only or kind == 'boundary':
                return
        else:
            current = self.snapshot()
            if len(current['watch']['events'] or []) != self.state['lastSequence']:
                raise ValueError('Unacknowledged events before Run; inspect external continuation')
            if current['context']['RIP'] != current['addresses']['diagnostic']:
                events = current['watch']['events'] or []
                if (not events or len(events) != self.state['lastSequence']
                        or events[-1]['ip'] != current['context']['RIP']):
                    raise ValueError('Starting stop is not an acknowledged experiment event')
            elif current['context']['R14'] != current['state']:
                raise ValueError('Starting diagnostic target changed')
        for _stop in range(self.args.max_stops):
            if time.monotonic() >= deadline:
                raise TimeoutError('Run loop deadline reached; target remains stopped')
            self.audit(current)
            verified = self.snapshot()
            if verified['context'] != current['context'] or verified['watch'] != current['watch']:
                raise ValueError('Context or watch changed before Run')
            if verified['watch']['armed'] != (self.state['phase'] == 'counting'):
                raise ValueError('Watch armed state does not match current phase')
            catalog = self.client.tools()
            schema = catalog.get('debugger_continue', {}).get('inputSchema', {})
            if 'instanceId' not in schema.get('properties', {}):
                raise ValueError('Continue tool schema unavailable or changed')
            self.state['pending'] = {'accepted': False, 'observedRunning': False,
                                     'context': current['context']}
            self.persist()
            receipt = self.client.call('debugger_continue', {'instanceId': self.instance})
            self.evidence['continuations'].append(receipt)
            if receipt.get('continued') is not True or receipt.get('mode') != 'run':
                raise ValueError('Run was not confirmed; do not retry automatically')
            self.state['pending']['accepted'] = True
            self.persist()
            current = self.wait_new(deadline)
            kind = self.recognize(current)
            if kind == 'boundary':
                self.audit(current)
                return
        raise ValueError('Stop limit reached; target remains stopped')

    def start(self):
        """在人工日期确认的边界启用窗口；无入参，无返回值，不调用 Run。"""
        if self.state['phase'] != 'start_wait' or not self.args.date:
            raise ValueError('Start requires start_wait and --date')
        date.fromisoformat(self.args.date)
        current = self.snapshot()
        if (current['context'] != self.state['start']['context']
                or current['watch'] != self.state['start']['watch']
                or len(current['watch']['events'] or []) != self.state['lastSequence']):
            raise ValueError('Start boundary changed')
        self.audit(current)
        armed = self.snapshot('arm')
        self.state.update(phase='counting', startDate=self.args.date, start=armed,
                          startSequence=self.state['lastSequence'])
        self.persist()

    def finish(self):
        """确认七天窗口并导出提交统计；无入参，无返回值，不把提交冒充实际写入。"""
        if self.state['phase'] != 'end_wait' or not self.args.date:
            raise ValueError('Finish requires end_wait and --date')
        validate_dates(self.state['startDate'], self.args.date)
        current = self.snapshot()
        if (current['context'] != self.state['end']['context'] or current['watch']['armed']
                or current['watch'] != self.state['end']['watch']
                or len(current['watch']['events'] or []) != self.state['lastSequence']):
            raise ValueError('End boundary changed or watch still armed')
        self.audit(current)
        if self.state['startEvent']['caller'] != self.state['endEvent']['caller']:
            raise ValueError('Boundary call source changed; investigate before reporting a week')
        events = [event for event in (current['watch']['events'] or [])
                  if event['sequence'] > self.state['startSequence'] and event['kind'] != 'boundary']
        if any(not event['counted'] for event in events):
            raise ValueError('Unarmed submit event inside the window')
        summary = summarize(events, current['watch']['errors'])
        counts = {key: summary[key]['count'] for key in KEYS}
        expected = 100000 * (-counts['add_0'] + counts['remove_0'] + counts['add_1'] - counts['remove_1'])
        actual = int(current['capacityRaw']) - int(self.state['start']['capacityRaw'])
        self.state.update(phase='complete', endDate=self.args.date, summary=summary, events=events,
                          reconciliation={'expectedCapacityDelta': str(expected), 'actualCapacityDelta': str(actual),
                                          'matched': expected == actual},
                          limitations=['Submit calls, not independently verified writes.',
                                       'Dates supplied by user; game sub-day phase not read.',
                                       'Thread restrictions are not exposed by the native breakpoint row.',
                                       'No positive target-submit hit is implied by a zero result.'])
        self.persist()


def main(argv=None):
    """运行一个可从 CMD 验证的编排阶段；入参为命令参数，返回退出码并保存证据。"""
    parser = argparse.ArgumentParser(description='Audit and orchestrate a CE trade-cycle experiment')
    parser.add_argument('command', choices=('inspect', 'selftest', 'prepare', 'seek', 'start', 'advance', 'wait', 'finish'))
    parser.add_argument('--state-file', type=Path, default=Path('Output/cycle_count/agent_state.json'))
    parser.add_argument('--output', type=Path, default=Path('Output/cycle_count/agent'))
    parser.add_argument('--instance-id')
    parser.add_argument('--gateway', type=Path, default=DEFAULT_GATEWAY)
    parser.add_argument('--timeout', type=float, default=30)
    parser.add_argument('--wait-seconds', type=float, default=180)
    parser.add_argument('--poll-interval', type=float, default=1)
    parser.add_argument('--max-stops', type=int, default=100)
    parser.add_argument('--allow-run', action='store_true')
    parser.add_argument('--date')
    args = parser.parse_args(argv)
    if (any(not math.isfinite(value) or value <= 0 for value in
            (args.timeout, args.wait_seconds, args.poll_interval)) or args.max_stops <= 0):
        parser.error('timeouts, polling interval and stop limit must be positive and finite')
    if args.command in {'seek', 'advance'} and not args.allow_run:
        parser.error('seek/advance require explicit --allow-run')
    args.output.mkdir(parents=True, exist_ok=True)
    report_path = args.output / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '_' + args.command + '.json')
    evidence = {'command': args.command, 'reportPath': str(report_path), 'requests': [],
                'statuses': [], 'snapshots': [], 'continuations': [], 'ok': False}
    client = McpClient([str(args.gateway)], args.timeout, report_path.with_suffix('.gateway.log'))
    controller = None
    lock_handle = None
    lock_path = args.state_file.with_suffix(args.state_file.suffix + '.lock')
    exit_code = 3
    try:
        save_report(report_path, evidence)
        args.state_file.parent.mkdir(parents=True, exist_ok=True)
        lock_handle = lock_path.open('x', encoding='utf-8')
        lock_handle.write(str(report_path) + '\n')
        lock_handle.flush()
        client.start()
        controller = Controller(client, args, evidence)
        if args.command == 'selftest':
            stopped_snapshot(client, controller.instance, {})
            source = lua_request({'action': 'test'}) + HERE.joinpath('ce_trade_watch.lua').read_text(encoding='utf-8')
            evidence['selftest'] = controller.lua(source, 'trade_synthetic_selftest')
            if evidence['selftest'].get('ok') is not True:
                raise ValueError('Synthetic condition selftest failed')
        elif args.command == 'inspect':
            snapshot = controller.snapshot()
            evidence['conditions'] = controller.audit(snapshot)
        elif args.command == 'prepare':
            controller.prepare()
        else:
            controller.load()
            if args.command in {'seek', 'advance', 'wait'}:
                expected = 'prepared' if args.command == 'seek' else 'counting'
                if args.command != 'wait' and controller.state['phase'] != expected:
                    raise ValueError('Command does not match experiment phase')
                controller.run_loop(wait_only=args.command == 'wait')
            elif args.command == 'start':
                controller.start()
            else:
                controller.finish()
        evidence['ok'] = True
        exit_code = 0
    except KeyboardInterrupt:
        evidence['error'] = 'Interrupted; do not resend an uncertain Run'
        exit_code = 130
    except Exception as error:
        evidence['error'] = str(error)
        print('ERROR: ' + ascii(str(error)), file=sys.stderr)
    finally:
        try:
            client.close()
        except Exception as error:
            evidence['closeError'] = str(error)
            evidence['ok'] = False
            exit_code = 3
        try:
            if controller is not None and controller.state is not None:
                evidence['phase'] = controller.state['phase']
                controller.persist()
            else:
                save_report(report_path, evidence)
        finally:
            if lock_handle is not None:
                lock_handle.close()
                lock_path.unlink()
    print('INFO: Report: ' + str(report_path))
    if 'phase' in evidence:
        print('INFO: Phase: ' + evidence['phase'])
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
